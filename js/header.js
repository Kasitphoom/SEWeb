function changeToResponsive() {
    var x = document.getElementById("navRight");
    if (x.className === "nav-right") {
        x.className += " responsive";
    } else {
        x.className = "nav-right";
    }
}