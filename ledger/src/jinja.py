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
import bottle
import jinja2


jinja = jinja2.Environment(
    trim_blocks=True,
    keep_trailing_newline=True,
    loader=jinja2.FileSystemLoader(bottle.TEMPLATE_PATH),
    autoescape=jinja2.select_autoescape(['html', 'xml']),
    cache_size=0,
    auto_reload=True
)

jinja.globals.update(zip=zip)


def render(filename, *args, **kwargs):
    template = jinja.get_template(filename)
    return template.render(*args, **kwargs)
