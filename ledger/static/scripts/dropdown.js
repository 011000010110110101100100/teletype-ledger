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
/************
 * Dropdown *
 ************/
class FormDropdownItem {
    constructor(element) {
        let item = element.querySelector(".item");
        let icon = new StateElement(item.querySelector(".icon"));

        this.element = item;
        this.value = item.querySelector(".value");
        this.icon = icon;
        this.icon.showClassName = "icon fas fa-chevron-up";
        this.icon.hideClassName = "icon fas fa-chevron-down";

        item.addEventListener("click", () => {
            icon.toggle();
        });
    }
}


class FormDropdownSelect {
    constructor(element) {
        let select = element.querySelector(".select");
        
        this.element = select;
        this.list = new StateElement(select);

        this.list.showClassName = "select";
        this.list.hideClassName = "display-none";

        this.options = new List();

        for (let option of this.list.element.children) {
            this.options.push(option);
        }
    }
}


class FormDropdown {
    constructor(element) {
        this.element = element;

        let item = new FormDropdownItem(element);
        let select = new FormDropdownSelect(element);

        this.item = item; 
        this.select = select;

        function dropdownOptionSwitch(e) {
            let target = e.target;
            item.value.innerText = target.innerText;
            item.icon.toggle();
            select.list.toggle();
        }

        this.item.element.addEventListener("click", () => {
            select.list.toggle();
        });

        for (let option of select.options) {
            option.addEventListener("click", dropdownOptionSwitch);
        }
    }

    show() {
        this.item.icon.show();
        this.select.list.show();
    }

    hide() {
        this.item.icon.hide();
        this.select.list.hide();
    }

    toggle() {
        this.item.icon.toggle();
        this.select.list.toggle();
    }

    get value() {
        return this.item.value.innerText;
    }
}
