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
class List extends Array {
    remove(index) {
        let array = this.splice(index);
        let element = array.shift();
        while (array.length) {
            this.push(array.shift());
        }
        return element;
    }

    insert(index, ...items) {
        let array = this.splice(index);
        array.unshift(...items);
        while (array.length) {
            this.push(array.shift());
        }
    }

    next(index, step=1) {
        return this[index + step];
    }

    prev(index, step=1) {
        return this[index - step];
    }

    peek(index=0, step=1) {  // start at the end of array
        return this[this.length - index - step];
    }

    clone() {
        return this.slice(0);
    }
}
