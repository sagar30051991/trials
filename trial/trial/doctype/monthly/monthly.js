
function validateForm() {
    var x = document.forms["Monthly"]["Amount"].value;
    if (x == null || x == "") {
        alert("Name must be filled out");
        return false;
    }
}