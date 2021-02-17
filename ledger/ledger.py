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
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import render_template

from markupsafe import escape

from src import generate

app = Flask(__name__)
app.secret_key = generate.random_bytes(64)


@app.route('/')
def root():
    return render_template('root.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/password-reset')
def password_reset():
    return render_template('password-reset.html')
