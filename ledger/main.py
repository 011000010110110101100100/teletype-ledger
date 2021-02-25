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
import bottle
import functools

from src import generate

from src.constant import constant
from src.jinja import render
from src.canister import session
from src.canister import Canister
from src.sql import SQL

ledger = bottle.Bottle()
ledger.install(Canister())


def auth_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.user:
            bottle.redirect('/login')
        return view(**kwargs)
    return wrapped_view


@ledger.route('/static/<filepath:path>', name='static')
def static(filepath):
    return bottle.static_file(filepath, root='static')


@ledger.route('/')
@auth_required
def index():
    return render('index.html', session=session)


@ledger.route('/login', ['GET', 'POST'])
def login():
    return render('login.html', session=session)


@ledger.route('/register', ['GET', 'POST'])
def register():
    return render('register.html', session=session)


@ledger.route('/password-reset', ['GET', 'POST'])
def password_reset():
    return render('password-reset.html', session=session)


ledger.run(host='localhost', port=8080, debug=True, reloader=True)
