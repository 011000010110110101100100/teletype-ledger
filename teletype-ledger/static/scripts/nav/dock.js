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
document.querySelector('#dock').onclick = function (event) {
    let div = event.target.closest('div');
    switch(div.id) {
        case 'dock-record':
            window.location = '/record';
            break;
        case 'dock-trade':
            window.location = '/trade';
            break;
        case 'dock-portfolio':
            window.location = '/portfolio';
            break;
        case 'dock-donate':
            window.location = '/donate';
            break;
        case 'dock-menu':
            window.location = '/menu';
            break;
        default:
            break;
    }
};
