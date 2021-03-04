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

app = Bottle()
app.install(Canister())

schema = SQLSchema()

sql = SQLite()
sql.set_registrar()
sql.execute(schema.user())


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


@app.route('/broker')
@auth_required
def broker():
    return render('broker.html', session=session)


@app.route('/record')
@auth_required
def record():
    return render('record.html', session=session)


@app.route('/asset')
@auth_required
def asset():
    return render('asset.html', session=session)


@app.route('/logout')
@auth_required
def logout():
    session.cookie.set('ttyhdr', '')
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

        sql.set_registrar()

        register = sql.select('user', 'key, password, salt', f'email = "{email}"')
        if not register:
            return {
                "status": False,
                "message": render('flash.html', title='Error', body=f'{email} does not exist'),
                "path": "/login",
                "payload": {}
            }

        db_key, db_passwd, db_salt = register[0]
        result = scrypt.verify(password, db_passwd, db_salt)
        if not result:
            return {
                "status": False,
                "message": render('flash.html', title='Error', body=f'invalid password was given'),
                "path": "/login",
                "payload": {}
            }

        session.email = email

        session.schema = schema
        session.sql = SQLite()
        session.sql.database_name = db_key
        session.key = db_key

        hdr = session.auth.sign()
        session.cookie.set('ttyhdr', hdr)

        return {
            "status": True,
            "message": render('flash.html', title='Redirect', body=f'logged in as {email}'),
            "path": "/",
            "payload": {}
        }

    return render('user/login.html', session=session)


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

        sql.set_registrar()

        register = sql.select('user', 'email', f'email = "{email}"')
        print(register)
        if register:
            return {
                "status": False,
                "message": render('flash.html', title='Error', body=f'{email} is already registered'),
                "path": "/register",
                "payload": {}
            }

        if password != repeat:
            return {
                "status": False,
                "message": render('flash.html', title='Error', body=f'passwords do not match'),
                "path": "/register",
                "payload": {}
            }

        key = generate.random_str()
        while sql.select('user', 'key', f'key = "{key}"'):
            key = generate.random_str()

        hashed, salt = scrypt.derive(password)
        vals = key, email, hashed, salt
        cols = '(key, email, password, salt)'
        sql.insert('user', vals, cols)

        session.email = email

        session.schema = schema
        session.sql = SQLite()
        session.sql.database_name = key
        session.key = key

        schemas = schema.broker, schema.record, schema.setting
        for query in schemas:
            session.sql.execute(query())

        hdr = session.auth.sign()
        session.cookie.set('ttyhdr', hdr)

        return {
            "status": True,
            "message": render('flash.html', title='Redirect', body=f'logged in as {email}'),
            "path": "/",
            "payload": {}
        }

    return render('user/register.html', session=session)


# TODO
@app.route('/password-reset', ['GET', 'POST'])
@auth_redirect
def password_reset():
    return render('user/password-reset.html', session=session)


app.run(host='localhost', port=8080, debug=True, reloader=True)
