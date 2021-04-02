function validate() {
    var Password = document.getElementById("Confirm-password").value;
    if (Password == (document.getElementById("Password").value)) {
        alert("login successful");



    } else {
        alert("login failed");
    }
}