/* jshint esversion: 8 */
/*
* A web application implementing investment strategies
* Copyright (C) 2021 011000010110110101100100
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.
*/
const platform = document.querySelector('#platform');
const dropdown = new FormDropdown(platform);
dropdown.hide();

document.querySelector('form').onsubmit = function (event) {
    const request = new XMLHttpRequest();
    const section = document.querySelector('section');
    const payload = JSON.stringify({
        "platform": dropdown.value,
        "key": form.key.value,
        "secret": form.secret.value
    });
    console.log(payload);

    request.open('POST', '/broker');
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
