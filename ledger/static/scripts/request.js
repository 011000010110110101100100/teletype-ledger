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
*
* You should have received a copy of the GNU Affero General Public License
*/
/*
* NOTE: all request functions should return a promise...
* async should be used to gaurentee the promise.
*
* NOTE: generic objects named meta are used for simple requests
* that expect a json response.
*
* meta -> Object
*   meta.url = "localhost:8080/login"
*   meta.header = "Content-Type"
*   meta.value = "application/json"
*   meta.element = HTMLElement
*   meta.payload = Object
*/
async function getRequest(meta) {
    let request = new XMLHttpRequest();

    request.open('GET', meta.url);
    request.addEventListener('load', (event) => {
        meta.element.innerHTML = event.target.responseText;
    });
    request.send();

    return request;
}


async function postRequest(meta) {
    let request = new XMLHttpRequest();
    let payload = JSON.stringify(meta.payload);

    request.open('POST', meta.url);
    request.setRequestHeader(meta.headerKey, meta.headerValue);
    request.addEventListener('load', (event) => {
        meta.element.innerHTML = event.target.responseText;
    });
    request.send(payload);

    return request;
}


async function postRequestSession(path, element, payload) {
    const request = new XMLHttpRequest();

    request.open('POST', path);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onload = function (event) {
        try {
            let response = JSON.parse(event.target.responseText);
            element.innerHTML = response.view;
            setTimeout(() => { window.location = response.path; }, 3000);
        } catch(e) {
            console.log(e);
        }
    };
    request.send(payload);

    return request;
}
