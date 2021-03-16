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
class StateElement {
    constructor(element, state=false, callback=null) {
        this.element = element;
        this.state = state;
        this.callback = callback;

        this.showClassName = null;
        this.hideClassName = null;

        if (this.element && this.callback) {
            this.element.addEventListener('click', callback);
        }
    }

    show() {
        this.element.className = this.showClassName;
        this.state = true;
    }

    hide() {
        this.element.className = this.hideClassName;
        this.state = false;
    }

    toggle() {
        this.state = !this.state;

        if (this.state) {
            this.element.className = this.showClassName;
        } else {
            this.element.className = this.hideClassName;
        }
    }
}


class State {
    show(state, icon) {
        state.show();
        icon.show();
    }

    hide(state, icon) {
        state.hide();
        icon.hide();
    }

    toggle(state, icon) {
        state.toggle();
        if (state.state) {
            icon.show();
        } else {
            icon.hide();
        }
    }
}
