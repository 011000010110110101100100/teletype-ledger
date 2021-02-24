import os
import base64
import random

from src import constant


def random_bytes(size=None):
    body = str()

    if size is None:
        body = base64.urlsafe_b64encode(
            os.urandom(constant.SIZE)
        ).decode(constant.ENCODING)
    elif isinstance(size, int):
        body = base64.urlsafe_b64encode(
            os.urandom(size)
        ).decode(constant.ENCODING)
    else:
        raise ValueError('size must be type int')

    return body


def random_str(size=None):
    body = str()
    prefix = random.SystemRandom().choice(constant.LETTERS)

    if size is None:
        body = ''.join(
            random.SystemRandom().choice(constant.SYMBOLS)
            for _ in range(constant.SIZE - 1)
        )
    elif isinstance(size, int):
        body = ''.join(
            random.SystemRandom().choice(constant.SYMBOLS)
            for _ in range(size - 1)
        )
    else:
        raise ValueError('size must be type int')

    return prefix + body
