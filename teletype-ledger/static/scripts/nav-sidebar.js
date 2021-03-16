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
const toggleSidebarSubmenu = function (element) {
    let container = element.nextElementSibling;    

    if (container.className === 'display') {
        container.className = 'display-none';
    } else {
        container.className = 'display';
    }
};

const toggleSidebarBurger = function (sidebar) {
    let labels = sidebar.element.querySelectorAll('span');

    if (sidebar.element.classList.contains('sidebar-collapse')) {
        for (let label of labels) {
            label.className = 'label';
        }

        sidebar.element.classList.remove('sidebar-collapse');
    } else {
        for (let label of labels) {
            label.className = 'display-none';
        }

        sidebar.element.classList.add('sidebar-collapse');
    }
};

class Sidebar {
    constructor() {
        let burger = document.querySelector('#sidebar-burger');
        let asset = document.querySelector('#sidebar-asset');
        let broker = document.querySelector('#sidebar-broker');
        let csv = document.querySelector('#sidebar-csv');
        let theme = document.querySelector('#sidebar-theme');
        
        let containers = [asset, broker, csv, theme];

        for (let container of containers) {
            toggleSidebarSubmenu(container);
        }

        this.element = document.querySelector('#sidebar'); 
        this.burger = burger;
        this.asset = asset;
        this.broker = broker;
        this.csv = csv;
        this.theme = theme;

        toggleSidebarBurger(this);
    }
}

const sidebar = new Sidebar();

sidebar.element.onclick = function (event) {
    let button = event.target.closest('a');
    switch (button.id) {
        case 'sidebar-burger':
            toggleSidebarBurger(sidebar);
            break;
        case 'sidebar-asset':
        case 'sidebar-broker':
        case 'sidebar-csv':
        case 'sidebar-theme':
            toggleSidebarSubmenu(button);
            break;
    }
    console.log('button.id:', button.id);
};
