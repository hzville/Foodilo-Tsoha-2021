function confirmDelete() {
    var x = document.getElementById("second-form");
    var y = document.getElementById("first-form")
    if (x.style.display == "none") {

        x.style.display = "block";
        y.style.display = "none"
    } else {
        x.style.display = "none";
        y.style.display = "block"

    }
}

function cancelDelete() {
    var x = document.getElementById("second-form");
    var y = document.getElementById("first-form")
    if (x.style.display == "none") {

        x.style.display = "block";
        y.style.display = "none"
    } else {
        x.style.display = "none";
        y.style.display = "block"

    }
}

function showPasswordForm() {
    var x = document.getElementById("password-form")

    if (x.style.display == "none") {

        x.style.display = "block";
    } else {
        x.style.display = "none";

    }
}

function editRestaurantInfo() {
    var form = document.getElementById("restaurant-info-form");
    var elements = form.elements;
    console.log(elements)

    for (i = 0; i < elements.length; i++) {
        console.log(elements[i])
        console.log(elements[i].disabled)
        elements[i].disabled = false;
    }
}