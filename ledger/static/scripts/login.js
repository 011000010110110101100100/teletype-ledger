/* jshint esversion: 8 */
document.querySelector('form').onsubmit = function (event) {
    const request = new XMLHttpRequest();
    const section = document.querySelector('section');
    const email = event.target.elements[0];
    const password = event.target.elements[1];
    const payload = JSON.stringify({
        "email": email.value,
        "password": password.value
    });

    request.open('POST', '/login');
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
