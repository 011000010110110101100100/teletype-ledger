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
import base64
import random

from src.constant import constant


def random_bytes(size=None):
    body = str()

    if size is None:
        body = base64.urlsafe_b64encode(
            os.urandom(constant.BYTE_SIZE)
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
            for _ in range(constant.BYTE_SIZE - 1)
        )
    elif isinstance(size, int):
        body = ''.join(
            random.SystemRandom().choice(constant.SYMBOLS)
            for _ in range(size - 1)
        )
    else:
        raise ValueError('size must be type int')

    return prefix + body
