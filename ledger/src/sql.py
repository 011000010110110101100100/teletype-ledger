# Teletype - A web application for managing market based investments
# Copyright (C) 2020  Morgan Dark
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
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

DATABASE_PATH = 'db'
DATABASE_MASTER = 'sqlite_master'
DATABASE_DEFAULT_NAME = 'ledger'
DATABASE_DEFAULT_TABLE = 'user'


class SQLSchema(object):
    @staticmethod
    def user():
        return 'CREATE TABLE user (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'key TEXT NOT NULL, ' \
            'email TEXT NOT NULL, ' \
            'username TEXT NOT NULL, ' \
            'password BLOB NOT NULL, ' \
            'salt BLOB NOT NULL)'

    @staticmethod
    def broker():
        return 'CREATE TABLE broker (' \
            'id INTEGER PRIMARY KEY NOT NULL, ' \
            'platform TEXT NOT NULL, ' \
            'key TEXT NOT NULL, ' \
            'secret BLOB NOT NULL)'

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


class SQLMeta(object):
    def __init__(self):
        self._name = None
        self._schema = SQLSchema()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def schema(self):
        return self._schema

    @property
    def istable(self):
        return isinstance(self, SQLTable)

    @property
    def isdatabase(self):
        return isinstance(self, SQLDatabase)

    def use(self, name=None):
        self.name = name

    def connect(self):
        if self.isdatabase:
            return sqlite3.connect(self.path())
        elif self.istable:
            return sqlite3.connect(self.database.path())
        else:
            raise sqlite3.OperationalError(
                'QueryError: SQLMeta.connect: failed to connect to database')

    def execute(self, query):
        try:
            database = self.connect()
            database.execute(query)
            database.commit()
            database.close()
        except (sqlite3.OperationalError,) as e:
            print(f'QueryError: SQLMeta.execute: {e}')
            return None
        return True

    def cursor(self, query):
        result = None
        try:
            database = self.connect()
            cursor = database.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            database.close()
        except (sqlite3.OperationalError,) as e:
            print(f'QueryError: SQLMeta.cursor: {e}')
            return None
        return result

    def query(self, callback=None, *args, **kwargs):
        try:
            database = self.connect()
            result = callback(database, *args, **kwargs)
            database.close()
        except (sqlite3.OperationalError,) as e:
            print(f'QueryError: SQLMeta.query: {e}')
            return None
        return result

    def create(self, schema=None, name=None):
        query = None, None
        schema = {
            'broker': self.schema.broker,
            'record': self.schema.record,
            'asset': self.schema.asset,
            'setting': self.schema.setting
        }.get(schema, self.schema.record)
        if name is None:
            query = schema()
        else:
            query = schema(name)
        print(query)
        return self.execute(query)

    def select(self, name=None, cols=None, cond=None):
        query = None
        if name is None:
            name = self.name
        if cols is None:
            cols = '*'
        if cond is None:
            query = f'SELECT {cols} FROM {name}'
        else:
            query = f'SELECT {cols} FROM {name} where {cond}'
        return self.cursor(query)


class SQLTable(SQLMeta):
    def __init__(self, name=None, database=None):
        super(SQLTable, self).__init__()
        self.name = name
        self.database = database

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = DATABASE_DEFAULT_TABLE
        else:
            self._name = value

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        if value is None:
            self._database = SQLDatabase()
        elif isinstance(value, SQLDatabase):
            self._database = value
        else:
            raise TypeError('object "value" must be of type SQLDatabase')

    def list(self):
        return self.database.tables()

    def insert(self, vals, cols=None, table=None):
        query = None
        if table is None:
            table = self.name
        if cols is None:
            query = f'INSERT INTO {table} VALUES {vals}'
        else:
            query = f'INSERT INTO {table} {cols} VALUES {vals}'
        return self.execute(query)

    def update(self, name, set, cond=None):
        if cond is None:
            query = f'UPDATE {name} SET {set}'
        else:
            query = f'UPDATE {name} SET {set} WHERE {cond}'
        return self.execute(query)

    def drop(self, name=None):
        if name is None:
            name = self.name
        return self.execute(f'DROP TABLE {name}')

    def delete(self, cond=None):
        if cond is None:
            raise sqlite3.OperationalError('object "cond" is required to delete a row')
        return self.execute(f'DELETE FROM {self.name} WHERE {cond}')


class SQLDatabase(SQLMeta):
    def __init__(self, name=None):
        super(SQLDatabase, self).__init__()
        self.name = name
        self.master = DATABASE_MASTER
        self.table_name = DATABASE_DEFAULT_TABLE

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None:
            self._name = DATABASE_DEFAULT_NAME
        else:
            self._name = value

    def path(self, name=None):
        if name is None:
            return f'{DATABASE_PATH}/{self.name}.db'
        return f'{DATABASE_PATH}/{name}.db'

    def drop(self, name=None):
        try:
            os.remove(self.path(name))
        except (FileNotFoundError,):
            return False
        return True

    def list(self):
        contents = []
        for entry in os.scandir(DATABASE_PATH):
            if entry.is_file():
                name = entry.name.split('.')[0]
                contents.append(name)
        return contents

    def tables(self):
        result = []
        tables = self.select(self.master, 'tbl_name', 'type = "table"')
        for row in tables:
            result.append(row[0])
        return result


class SQL(object):
    def __init__(self):
        self.database = SQLDatabase()
        self.table = SQLTable(database=self.database)
