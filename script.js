async function bookService() {

    const name = document.getElementById("name").value;
    const service = document.getElementById("service").value;
    const phone = document.getElementById("phone").value;

    if (!name || !service || !phone) {
        alert("Please fill all fields");
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/book", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, service, phone })
        });

        const data = await response.json();
        alert(data.message);

        // Clear fields
        document.getElementById("name").value = "";
        document.getElementById("service").value = "";
        document.getElementById("phone").value = "";

    } catch (error) {
        alert("Error connecting to backend");
        console.error(error);
    }
}