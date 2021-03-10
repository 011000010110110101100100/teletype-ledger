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
import string

from src.singleton import Singleton


class Constant(Singleton):
    def __init__(self):
        super().__init__()

    @property
    def DIGITS(self):
        return string.digits

    @property
    def LETTERS(self):
        return string.ascii_letters

    @property
    def SYMBOLS(self):
        return self.DIGITS + self.LETTERS + '_'

    @property
    def ENCODING(self):
        return 'utf-8'

    @property
    def TIMEOUT(self):
        return 0  # 3600

    @property
    def BYTE_SIZE(self):
        return 64


constant = Constant()
