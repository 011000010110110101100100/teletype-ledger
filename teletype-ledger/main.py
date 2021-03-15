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
import os

from functools import wraps

from bottle import Bottle
from bottle import request
from bottle import response
from bottle import redirect
from bottle import static_file

from src import generate
from src import scrypt

from src.jinja import render
from src.sqlite import SQLSchema
from src.sqlite import SQLite
from src.canister import Canister
from src.canister import session

try:
    os.mkdir('db')
except (FileExistsError,):
    pass

try:
    os.mkdir('csv')
except (FileExistsError,):
    pass

app = Bottle()
app.config.update('canister', log_level='DEBUG')
app.install(Canister())

schema = SQLSchema()

sql = SQLite()
sql.set_registrar()
sql.execute(schema.user())


def payload(view, path, data, status):
    return {
        "status": status,
        "view": view,
        "path": path,
        "data": data
    }


# generate a status page
def flash(title, body):
    return render('flash.html', title=title, body=body)


def set_session(email, key):
    global session
    global schema

    session.email = email
    session.schema = SQLSchema()
    session.sql = SQLite()
    session.sql.database_name = key
    session.key = key


# redirect the user if they are not logged in
def auth_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.user:
            redirect('/login')
        return view(**kwargs)
    return wrapped_view


# redirect the user if they are logged in
def auth_redirect(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if session.user:
            redirect('/')
        return view(**kwargs)
    return wrapped_view


@app.route('/static/<filepath:path>', name='static')
def static(filepath):
    return static_file(filepath, root='static')


@app.route('/')
@auth_required
def index():
    return render('index.html', session=session)


@app.route('/record')
@auth_required
def record():
    return render('record/menu.html', session=session)


@app.route('/record/broker')
@auth_required
def broker():
    return render('record/broker.html', session=session)


@app.route('/record/asset')
@auth_required
def asset():
    return render('record/asset.html', session=session)


@app.route('/logout')
@auth_required
def logout():
    session.cookie.set('ttysid', '')
    session.cookie.set('ttyhdr', '')
    app.log.info('Logout: session destroyed')
    redirect('/login')


@app.route('/login', ['GET', 'POST'])
@auth_redirect
def login():
    global schema
    global sql
    global session

    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        app.log.debug(f'Login: email: {email}')
        app.log.debug(f'Login: password: {password}')

        sql.set_registrar()
        app.log.debug(f'Login: database: {sql.database_name}')

        register = sql.select('user', 'key, password, salt', f'email = "{email}"')
        app.log.debug(f'Login: register: {register}')

        if not register:
            view = flash('Error', f'{email} does not exist')
            return payload(view, '/login', {}, False)

        db_key, db_passwd, db_salt = register[0]
        app.log.debug(f'Login: key, pass, salt: {db_key}, {db_passwd}, {db_salt}')
        result = scrypt.verify(password, db_passwd, db_salt)
        app.log.debug(f'Login: result: {result}')
        if not result:
            view = flash('Error', 'invalid password was given')
            return payload(view, '/login', {}, False)

        set_session(email, db_key)
        hdr = session.auth.sign()
        session.cookie.set('ttyhdr', hdr)
        app.log.info('Login: user session created')

        view = flash('Redirect', f'logged in as {email}')
        return payload(view, '/', {}, True)

    return render('session/login.html', session=session)


@app.route('/register', ['GET', 'POST'])
@auth_redirect
def register():
    global schema
    global sql
    global session

    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        repeat = request.json.get('repeat')
        app.log.debug(f'Register: email: {email}')
        app.log.debug(f'Register: password: {password}')
        app.log.debug(f'Register: repeat: {repeat}')

        sql.set_registrar()
        app.log.debug(f'Register: database: {sql.database_name}')

        register = sql.select('user', 'email', f'email = "{email}"')
        app.log.debug(f'Register: register: {register}')

        if register:
            view = flash('Error', f'{email} is already registered')
            return payload(view, '/register', {}, False)

        if password != repeat:
            view = flash('Error', 'passwords do not match')
            return payload(view, '/register', {}, False)

        key = generate.random_str()
        app.log.debug(f'Register: key: {key}')

        while sql.select('user', 'key', f'key = "{key}"'):
            key = generate.random_str()

        hashed, salt = scrypt.derive(password)
        app.log.debug(f'Register: hashed, salt: {hashed}, {salt}')

        vals = key, email, hashed, salt
        cols = '(key, email, password, salt)'
        sql.insert('user', vals, cols)

        set_session(email, key)
        schemas = schema.broker(), schema.record(), schema.setting()
        for query in schemas:
            session.sql.execute(query)

        hdr = session.auth.sign()
        session.cookie.set('ttyhdr', hdr)
        app.log.info('Register: user session created')

        view = flash('Redirect', f'logged in as {email}')
        return payload(view, '/', {}, True)

    return render('session/register.html', session=session)


# TODO
@app.route('/password-reset', ['GET', 'POST'])
@auth_redirect
def password_reset():
    if request.method == 'POST':
        view = flash('Response', f'This is a dummy response.')
        return payload(view, '/password-reset', {}, False)
    return render('session/reset.html', session=session)


app.run(host='localhost', port=8080, debug=True, reloader=True)
