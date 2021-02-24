#!/usr/bin/env python3
# A web application implementing investment strategies
# Copyright (C) 2021 011000010110110101100100
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from src import generate
from src import constant

from src.jinja import render
from src.canister import session
from src.canister import Canister
from src.sql import SQL

import bottle

ledger = bottle.Bottle()
ledger.install(Canister())

session = constant.SESSION


@ledger.route('/static/<filepath:path>', name='static')
def static(filepath):
    return bottle.static_file(filepath, root='static')


@ledger.route('/')
def index():
    if session.sid:
        return render('index.html', session=session)
    return bottle.redirect('/login')


@ledger.route('/login', ['GET', 'POST'])
def login():
    return render('login.html')


@ledger.route('/register', ['GET', 'POST'])
def register():
    return render('register.html')


@ledger.route('/password-reset', ['GET', 'POST'])
def password_reset():
    return render('password-reset.html')


ledger.run(host='localhost', port=8080, debug=True, reloader=True)
