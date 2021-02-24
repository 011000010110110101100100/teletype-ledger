#!/usr/bin/env python3
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
