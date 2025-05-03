async function loginUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem("token", data.token);
        window.location.href = "/dashboard.html";
    } else {
        alert("Invalid credentials");
    }
}

async function signupUser() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.querySelector("input[name='role']:checked").value;

    const response = await fetch("/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, role })
    });

    const data = await response.json();
    if (response.ok) {
        alert("Account created! You can now log in.");
        window.location.href = "/login.html";
    } else {
        alert("Error creating account");
    }
}