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
import sqlite3


class SQLSchema(object):
    @staticmethod
    def user():
        return 'CREATE TABLE user (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'key TEXT NOT NULL, ' \
            'email TEXT NOT NULL, ' \
            'password TEXT NOT NULL, ' \
            'salt TEXT NOT NULL)'

    @staticmethod
    def broker():
        return 'CREATE TABLE broker (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'platform TEXT NOT NULL, ' \
            'key TEXT NOT NULL, ' \
            'secret TEXT NOT NULL)'

    @staticmethod
    def record():
        return 'CREATE TABLE record (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'key TEXT NOT NULL, ' \
            'name TEXT NOT NULL, ' \
            'strategy TEXT NOT NULL, ' \
            'platform TEXT NOT NULL,' \
            'period TEXT NOT NULL)'

    @staticmethod
    def asset(name):
        return f'CREATE TABLE {name} (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'date DATE NOT NULL, ' \
            'market_value REAL NOT NULL, ' \
            'target_value REAL, ' \
            'current_value REAL NOT NULL, ' \
            'fiat_diff REAL NOT NULL, ' \
            'fiat_total REAL, ' \
            'share_diff REAL NOT NULL, ' \
            'share_total REAL, ' \
            'period INTEGER NOT NULL)'

    @staticmethod
    def setting():
        return 'CREATE TABLE settings (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'email TEXT NOT NULL, ' \
            'password BLOB NOT NULL, ' \
            'theme TEXT NOT NULL)'


class SQLite(object):
    def __init__(self):
        self.__master = 'sqlite_master'
        self.__database_path = 'db'
        self.__database_name = 'registrar'

    @property
    def master(self):
        return self.__master

    @property
    def database_path(self):
        return self.__database_path

    @database_path.setter
    def database_path(self, value):
        self.__database_path = value

    @property
    def database_name(self):
        return self.__database_name

    @database_name.setter
    def database_name(self, value):
        self.__database_name = value

    def set_registrar(self):
        self.__database_name = 'registrar'

    def connect(self):
        return sqlite3.connect(f'{self.database_path}/{self.database_name}.db')

    def execute(self, query):
        try:
            database = self.connect()
            database.execute(query)
            database.commit()
            database.close()
        except (sqlite3.OperationalError,) as e:
            print(f'Error: SQLite.execute: {e}')
            return None
        return True

    def cursor(self, query):
        try:
            database = self.connect()
            cursor = database.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            database.close()
            return result
        except (sqlite3.OperationalError,) as e:
            print(f'Error: SQLite.cursor: {e}')
            return None

    def query(self, callback=None, *args, **kwargs):
        try:
            database = self.connect()
            result = callback(database, *args, **kwargs)
            database.close()
        except (sqlite3.OperationalError,) as e:
            print(f'Error: SQLite.query: {e}')
            return None
        return result

    def select(self, table, cols=None, cond=None):
        query = None
        if cols is None:
            cols = '*'
        if cond is None:
            query = f'SELECT {cols} FROM {table}'
        else:
            query = f'SELECT {cols} FROM {table} where {cond}'
        return self.cursor(query)

    def insert(self, table, vals, cols=None):
        query = None
        if cols is None:
            query = f'INSERT INTO {table} VALUES {vals}'
        else:
            query = f'INSERT INTO {table} {cols} VALUES {vals}'
        return self.execute(query)

    def update(self, table, vals, cond=None):
        if cond is None:
            query = f'UPDATE {table} SET {vals}'
        else:
            query = f'UPDATE {table} SET {vals} WHERE {cond}'
        return self.execute(query)

    def drop_row(self, table, cond):
        return self.execute(f'DELETE FROM {table} WHERE {cond}')

    def drop_table(self, name):
        return self.execute(f'DROP TABLE {name}')

    def drop_database(self, name):
        try:
            os.remove(f'{self.database_path}/{name}.db')
        except (FileNotFoundError,):
            return False
        return True

    def list_tables(self):
        result = []
        tables = self.select(self.master, 'tbl_name', 'type = "table"')
        for row in tables:
            result.append(row[0])
        return result

    def list_databases(self):
        contents = []
        for entry in os.scandir(f'{self.database_path}'):
            if entry.is_file():
                name = entry.name.split('.')[0]
                contents.append(name)
        return contents
