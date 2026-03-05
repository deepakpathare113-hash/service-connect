"""
Service Connect Backend
A professional service booking platform with SQLite database
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Database configuration
DB_PATH = os.path.join(os.path.dirname(__file__), 'service_connect.db')

def get_db_connection():
    """Get a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            role TEXT DEFAULT 'customer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            service TEXT NOT NULL,
            description TEXT,
            date TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")

# Routes

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Service Connect Backend is Running",
        "endpoints": {
            "register": "/register",
            "login": "/login",
            "bookings": "/api/bookings",
            "service_list": "/api/services"
        }
    }), 200

@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.json
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        phone = data.get("phone", "").strip()
        role = data.get("role", "customer")
        
        # Validation
        if not all([name, email, password, phone]):
            return jsonify({"error": "Please fill all required fields"}), 400
        
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters"}), 400
        
        if "@" not in email:
            return jsonify({"error": "Invalid email address"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (name, email, password, phone, role) VALUES (?, ?, ?, ?, ?)',
                (name, email, password, phone, role)
            )
            conn.commit()
            return jsonify({"message": "Registration successful! Please login."}), 201
        
        except sqlite3.IntegrityError:
            return jsonify({"error": "Email already registered"}), 400
        
        finally:
            conn.close()
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    """Login a user"""
    try:
        data = request.json
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        
        if not email or not password:
            return jsonify({"error": "Please provide email and password"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({
                "message": "Login successful!",
                "user": {
                    "id": user['id'],
                    "name": user['name'],
                    "email": user['email'],
                    "role": user['role']
                }
            }), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/bookings", methods=["POST"])
def create_booking():
    """Create a new service booking"""
    try:
        data = request.json
        name = data.get("name", "").strip()
        phone = data.get("phone", "").strip()
        service = data.get("service", "").strip()
        description = data.get("description", "").strip()
        date = data.get("date", "").strip()
        
        # Validation
        if not all([name, phone, service]):
            return jsonify({"error": "Name, phone, and service are required"}), 400
        
        # Basic phone validation
        if len(phone) < 10:
            return jsonify({"error": "Please provide a valid phone number"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO bookings (name, phone, service, description, date) VALUES (?, ?, ?, ?, ?)',
            (name, phone, service, description, date)
        )
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "message": "Booking confirmed successfully!",
            "booking_id": booking_id,
            "details": {
                "name": name,
                "phone": phone,
                "service": service,
                "date": date or "ASAP"
            }
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/bookings", methods=["GET"])
def get_bookings():
    """Get all bookings (for admin/service providers)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM bookings ORDER BY created_at DESC')
        bookings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            "total": len(bookings),
            "bookings": bookings
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/services", methods=["GET"])
def get_services():
    """Get list of available services"""
    services = [
        {"name": "Doctor", "icon": "👨‍⚕️", "description": "Online and in-person consultations"},
        {"name": "Plumber", "icon": "🔧", "description": "Water and fitting services"},
        {"name": "Electrician", "icon": "⚡", "description": "Electrical repair & installation"},
        {"name": "Carpenter", "icon": "🪑", "description": "Furniture repair & making"},
        {"name": "Salon", "icon": "💇‍♀️", "description": "Hair styling and makeup"},
        {"name": "Cleaning", "icon": "🧹", "description": "Professional cleaning services"},
        {"name": "AC Repair", "icon": "❄️", "description": "AC repair and maintenance"},
        {"name": "Other", "icon": "✋", "description": "Other services"}
    ]
    return jsonify({"services": services}), 200

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get booking statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as count FROM bookings')
        total_bookings = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM users')
        total_users = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM bookings WHERE status = "pending"')
        pending_bookings = cursor.fetchone()['count']
        
        conn.close()
        
        return jsonify({
            "total_bookings": total_bookings,
            "total_users": total_users,
            "pending_bookings": pending_bookings,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Initialize database
    init_db()
    
    # Start Flask app
    print("\n" + "="*50)
    print("🚀 Service Connect Backend")
    print("="*50)
    print("✓ Server running on http://localhost:5000")
    print("✓ Database: service_connect.db")
    print("="*50 + "\n")
    
    app.run(host='localhost', port=5000, debug=True)