from os import urandom
from hashlib import scrypt


def derive(password):
    salt = urandom(32)
    key = scrypt(
        password.encode(),
        salt=salt,
        n=2**14, r=8, p=1,
        dklen=32
    )
    return key.hex(), salt.hex()


def verify(password, hashed, salt):
    key = scrypt(
        password.encode(),
        salt=bytes.fromhex(salt),
        n=2**14, r=8, p=1,
        dklen=32
    )
    return True if key.hex() == hashed else False
