function goToHome() {
    window.location = "http://127.0.0.1:8000/";
}

function login() {
    window.location = "http://127.0.0.1:8000/login";
}

function signout() {
    window.location = "http://127.0.0.1:8000/signout";
}

function reference() {
    window.location = "http://127.0.0.1:8000/student/reference";
}

function material(id) {
    window.location = "http://127.0.0.1:8000/student/reference/"+id;
}

function quiz(id) {
    window.location = "http://127.0.0.1:8000/student/quiz_detail/"+id;
}

function edit() {
    window.location = "http://127.0.0.1:8000/student/edit";
}

function change() {
    window.location = "http://127.0.0.1:8000/student/change";
}