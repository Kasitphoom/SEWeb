isPageOnTop = true;

function changeToResponsive() {
    var x = document.getElementById("navRight");
    if (x.className === "nav-right") {
        x.className += " responsive";
    } else {
        x.className = "nav-right";
    }
}

// check if scrolled?
window.addEventListener("scroll", scrollFunction);

function scrollFunction() {
    const accentBar = document.getElementById("accent-bar");
    const spacer = document.getElementById("spacer");
    if (window.scrollY > 0) {
        accentBar.classList.add("small-bar");
        spacer.classList.add("small-bar");
    } else {
        accentBar.classList.remove("small-bar");
        spacer.classList.remove("small-bar");
    }
}