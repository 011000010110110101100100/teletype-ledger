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
* meta -> Object
*   meta.url = "localhost:8080/login"
*   meta.header = "Content-Type"
*   meta.value = "application/json"
*   meta.element = HTMLElement
*   meta.payload = Object
*/
async function getRequest(meta) {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", meta.url);
    xhr.addEventListener("load", (event) => {
        meta.element.innerHTML = event.target.responseText;
    });
    xhr.send();
    return xhr;
}


async function postRequest(meta) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", meta.url);
    xhr.setRequestHeader(meta.header, meta.value);
    xhr.addEventListener('load', (event) => {
        meta.element.innerHTML = event.target.responseText;
    });
    payload = JSON.stringify(meta.payload);
    xhr.send(payload);
    return xhr;
}
