document.addEventListener("touchstart", function () {
    document.getElementsByClassName("container")[0].classList.toggle("hover")
});


// document.addEventListener("DOMContentLoaded", function () {
//     const userForm = document.getElementById("login-form");
//     const messageDiv = document.getElementById("message");

//     userForm.addEventListener("submit", function (event) {
//         event.preventDefault();

//         const userData = new FormData(userForm);

//         const userObject = {
//             email: userData.get("email"),
//             password: userData.get("password"),
//         };

//         fetch("http://127.0.0.1:8000/users/add", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//             },
//             body: JSON.stringify(userObject),
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error("Network response was not ok");
//             }
//             return response.json();
//         })
//         .then(data => {
//             messageDiv.textContent = "User added successfully.";
//             userForm.reset();
//         })
//         .catch(error => {
//             messageDiv.textContent = "Error adding user: " + error.message;
//             console.error(error);
//         });
//     });
// });