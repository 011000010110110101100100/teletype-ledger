/* jshint esversion: 8 */
document.querySelector('form').onsubmit = function (event) {
    const request = new XMLHttpRequest();
    const section = document.querySelector('section');
    const email = event.target.elements[0];
    const password = event.target.elements[1];
    const repeat = event.target.elements[2];
    const payload = JSON.stringify({
        "email": email.value,
        "password": password.value,
        "repeat": repeat.value
    });

    request.open('POST', '/register');
    request.setRequestHeader('Content-Type', 'application/json');

    request.onload = function (event) {
        try {
            let body = JSON.parse(event.target.responseText);
            section.innerHTML = body.message;
            setTimeout(() => { window.location = body.path; }, 3000);
        } catch(e) {
            console.log(e);
        }
    };

    request.send(payload);

    return false;
};
