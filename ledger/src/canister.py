# The MIT License (MIT)
#
# Copyright (c) 2016
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Source: https://github.com/dagnelies/canister.git
"""
Canister is a simple plugin for bottle, providing:
- formatted logs
- url and form params unpacking
- sessions (server side) based on a `session_id` cookie
- authentication through basic auth or bearer token (OAuth2)
- CORS for cross-domain REST APIs
"""
import bottle
import inspect
import logging
import logging.handlers
import math
import os
import os.path
import sys
import time
import threading

from src import generate

from src.constant import constant
from src.singleton import Singleton

from jwcrypto import jwk
from jwcrypto import jws
from jwcrypto.common import json_encode
from jwcrypto.common import json_decode

session = threading.local()


class Log(Singleton):
    def __init__(self, app):
        super(Log, self).__init__()
        self._log = None
        self.config(app)

    @property
    def log(self):
        return self._log

    def config(self, app):
        self._path = app.config.get('canister.log.path', None)
        self._level = app.config.get('canister.log.level', 'DEBUG')
        self._days = int(app.config.get('canister.log.days', '30'))
        self._log = logging.getLogger('canister.log')

    def build(self):
        if 'DISABLED' == self._level:
            return self._log
        if self._path is None:
            handler = logging.StreamHandler()
        else:
            os.makedirs(self._path, exist_ok=True)
            handler = logging.handlers.TimedRotatingFileHandler(
                os.path.join(self._path, 'log'),
                when='midnight',
                backupCount=int(self._days)
            )
        self._log.setLevel(self._level)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s [%(threadName)s]   %(message)s'
        )
        handler.setFormatter(formatter)
        self._log.addHandler(handler)
        return self._log


class Cookie(object):
    def __init__(self):
        self.__key = 'sid'
        self.__secret = generate.random_bytes()
        self.__response = bottle.response
        self.__request = bottle.request

    @property
    def secret(self):
        return self.__secret

    @property
    def key(self):
        return self.__key

    def get(self):
        return self.__request.get_cookie(self.__key, secret=self.secret)

    def set(self, value):
        self.__response.set_cookie(self.__key, value, secret=self.secret)


class Cache(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except (KeyError,):
            return self.__dict__[name]

    def __setattr__(self, name, value):
        try:
            self[name] = value
        except (KeyError,):
            self.__dict__[name] = value

    def __delitem__(self, key):
        try:
            del self[key]
        except (KeyError,):
            pass


class Policy(object):
    """JSON Web Token: https://tools.ietf.org/html/rfc7519"""

    def __init__(self, iss=None, sub=None, aud=None):
        self.__iss = 'teletype' if iss is None else iss
        self.__sub = 'ledger' if sub is None else sub
        self.__aud = generate.random_str() if aud is None else aud
        self.__jti = generate.random_bytes()
        self.__iat = int(time.time())
        self.__exp = self.__iat + constant.TIMEOUT

    @property
    def iss(self):
        return self.__iss

    @property
    def sub(self):
        return self.__sub

    @property
    def aud(self):
        return self.__aud

    @aud.setter
    def aud(self, value):
        assert isinstance(value, str)
        self.__aud = value

    @property
    def jti(self):
        return self.__jti

    @property
    def iat(self):
        return self.__iat

    @property
    def exp(self):
        return self.__exp

    @property
    def claims(self):
        return {
            'iss': self.iss,
            'sub': self.sub,
            'aud': self.aud,
            'jti': self.jti,
            'iat': self.iat,
            'exp': self.exp
        }

    @property
    def expired(self):
        now = int(time.time())
        if (now - self.iat) < constant.TIMEOUT:
            return False
        return True

    def verify(self, claims):
        return claims == self.claims


class Auth(object):
    def __init__(self, kty=None, size=None, alg=None):
        self.__kty = 'oct' if kty is None else kty
        self.__size = 256 if size is None else size
        self.__alg = 'HS256' if alg is None else alg
        self.__key = jwk.JWK.generate(kty=self.__kty, size=self.__size)
        self.__header = {'alg': self.__alg, 'kid': self.__key.thumbprint()}
        self.__tok = None
        self.__sig = None
        self.__hdr = None
        self.__pol = None

    @property
    def tok(self):
        return self.__tok

    @property
    def sig(self):
        return self.__sig

    @property
    def hdr(self):
        return self.__hdr

    @property
    def pol(self):
        return self.__pol

    @staticmethod
    def serialize(sig):
        """return a JWT header token"""
        hdr = json_decode(sig)
        return f'{hdr["protected"]}.{hdr["payload"]}.{hdr["signature"]}'

    @staticmethod
    def deserialize(hdr):
        """return a JWT signature"""
        try:
            protected, payload, signature = hdr.split('.')
            sig = json_encode({
                'payload': payload,
                'protected': protected,
                'signature': signature
            })
            return sig
        except (ValueError,):
            return str()

    def sign(self):
        """return a signed JWT header token"""
        self.__pol = Policy()
        self.__tok = jws.JWS(json_encode(self.__pol.claims))
        self.__tok.add_signature(
            self.__key, alg=None, protected=json_encode(self.__header)
        )
        self.__sig = self.__tok.serialize()
        self.__hdr = self.serialize(self.__sig)
        return self.__hdr

    def verify(self, hdr):
        """return JWT header verification as a bool"""
        try:
            sig = self.deserialize(hdr)
            self.__tok.deserialize(sig)
            self.__tok.verify(self.__key)
            return True
        except (jws.InvalidJWSSignature, jws.InvalidJWSObject,):
            return False


class SessionCache(object):
    '''A thread safe session cache with a cleanup thread'''

    def __init__(self):
        log = logging.getLogger('canister.log')
        self.__lock = threading.Lock()
        self.__cache = Cache()

        if 0 >= constant.TIMEOUT:
            log.warn('Sessions kept indefinitely! (session timeout is <= 0)')
            return

        interval = int(math.sqrt(constant.TIMEOUT))

        log.info(
            f'Session timeout is {constant.TIMEOUT} seconds. '
            f'Checking for expired sessions every {interval} seconds. '
        )

        def prune():
            while True:
                time.sleep(interval)

                with self.__lock:
                    survivors = Cache()

                    for sid, auth in self.__cache.items():
                        if not auth.pol or (auth.pol and not auth.pol.expired):
                            survivors[sid] = auth

                    n = len(self.__cache) - len(survivors)
                    self.__cache = survivors
                    log.debug(f'{n} expired sessions pruned')

        # NOTE: Daemon threads are abruptly stopped at shutdown.
        # Their resources (such as open files, database transactions, etc.)
        # may not be released properly.
        # Since these are "in memory" sessions, we don't care ...just be
        # aware of it if you want to change that.
        cleaner = threading.Thread(name="SessionCleaner", target=prune)
        cleaner.daemon = True
        cleaner.start()

    def __contains__(self, sid):
        return sid in self.__cache

    def get(self, sid):
        with self.__lock:
            return self.__cache.get(sid)

    def set(self, sid, auth=None):
        with self.__lock:
            self.__cache[sid] = Auth() if auth is None else auth

    def create(self, sid, auth=None):
        with self.__lock:
            self.__cache[sid] = Auth() if auth is None else auth
            return self.__cache.get(sid)

    def delete(self, sid):
        with self.__lock:
            del self.__cache[sid]


class Canister(object):
    name = 'canister'
    api = 2

    def __init__(self):
        pass

    def setup(self, app):
        log = Log(app)

        self.app = app
        self.log = log.build()

        self.log.info('============')
        self.log.info('Initializing')
        self.log.info('============')
        self.log.info('python version: ' + sys.version)
        self.log.info('bottle version: ' + bottle.__version__)
        self.log.info('------------------------------------------')
        for k, v in app.config.items():
            self.log.info('%-30s = %s' % (k, v))
        self.log.info('------------------------------------------')

        self.app.log = log

        self.cookie = Cookie()
        self.cache = SessionCache()
        self.cors = app.config.get('canister.cors', None)

    def apply(self, callback, route):
        log = self.log

        def wrapper(*args, **kwargs):
            start = time.time()

            request = bottle.request
            response = bottle.response

            # thread name = <ip>-...
            threading.current_thread().name = request.remote_addr + '-...'
            log.info(request.method + ' ' + request.url)

            if self.cors:
                response.headers['Access-Control-Allow-Origin'] = self.cors

            # session
            sid = self.cookie.get()
            self.log.info(f'Cookie SID: {sid}')

            if sid and sid in self.cache:
                auth = self.cache.get(sid)
                log.info(f'Session found: {sid}')
            else:
                # avoid session id collisions
                sid = generate.random_bytes()
                while sid in self.cache:
                    sid = generate.random_bytes()

                # create session id
                self.cookie.set(sid)
                auth = self.cache.create(sid)
                log.info(f'Session created: {sid}')

            session.sid = sid
            session.auth = auth
            session.user = False

            # thread name = <ip>-<sid[0:6]>
            threading.current_thread().name = request.remote_addr + '-' + sid[0:6]

            # user
            header = request.headers.get('Authorization')
            self.log.info(f'Header: {header}')

            if header:
                bearer = None
                http = header.split()

                if 2 == len(http):
                    typ, cred = http
                    self.log.info(f'Authorization: {typ} {cred}')
                else:
                    self.log.warning(f'Invalid Authorization: {header}')
                    return None

                if (typ and cred) and typ == 'Bearer':
                    bearer = cred

                if bearer and session.auth.verify(bearer):
                    session.user = True
                    self.cache.set(sid, auth)
                    self.log.info(f'Logged in as: {bearer}')
                else:
                    self.log.error(f'Invalid Bearer Token: {bearer}')
                    return None

            if session.sid != sid or session.auth is not auth:
                self.cache.set(session.sid, session.auth)

            # args unpacking
            sig = inspect.getargspec(callback)

            for a in sig.args:
                if a in request.params:
                    kwargs[a] = request.params[a]

            result = callback(*args, **kwargs)

            elapsed = time.time() - start

            if elapsed > 1:
                log.warn('Response: %d (%dms !!!)' % (response.status_code, 1000 * elapsed))
            else:
                log.info('Response: %d (%dms)' % (response.status_code, 1000 * elapsed))

            return result

        return wrapper

    def close(self):
        pass
