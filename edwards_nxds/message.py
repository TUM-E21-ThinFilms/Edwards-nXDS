# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from e21_util.error import CommunicationError

class Message(object):

    TERMINAL = chr(13) # Carriage return \r

    PRECEDING_QUERY = '?'
    PRECEDING_COMMAND = '!'
    PRECEDING_REPLY = '*'
    PRECEDING_RESPONSE = '='

    PRECEDINGS = [PRECEDING_QUERY, PRECEDING_COMMAND, PRECEDING_REPLY, PRECEDING_RESPONSE]

    TYPE_COMMAND = 'C'
    TYPE_VOLATILE = 'V'
    TYPE_STATIC = 'S'

    TYPES = [TYPE_VOLATILE, TYPE_STATIC, TYPE_COMMAND]

    SEPARATOR = ' '

    def __init__(self):
        self._preceding = ''
        self._type = ''
        self._object = ''
        self._data = None

    def set_preceding(self, preceding):
        if not preceding in self.PRECEDINGS:
            raise ValueError("Unknown preceding given")

        self._preceding = preceding

    def set_type(self, type):
        if not type in self.TYPES:
            raise ValueError("Unknown type given")

        self._type = type

    def set_object(self, object):

        object = str(int(object))

        if not len(object) == 3:
            raise ValueError("Unknown object given, length must be equal to three")

        self._object = object

    def set_data(self, data):
        if not isinstance(data, basestring) and not data is None:
            raise ValueError("Data must be of type string")

        self._data = data

    def get_data(self):
        return self._data

    def get_raw(self):
        if not self._data is None:
            return "".join([self._preceding, self._type, self._object, self.SEPARATOR, self._data, self.TERMINAL])
        else:
            return "".join([self._preceding, self._type, self._object, self.TERMINAL])

    def __str__(self):
        return "MESSAGE: "+repr(self.get_raw())

class Query(Message):
    def __init__(self, type, object):
        super(Query, self).__init__()
        self.set_preceding(Message.PRECEDING_QUERY)
        self.set_type(type)
        self.set_object(object)

class Command(Message):
    def __init__(self, type, object, data):
        super(Command, self).__init__()
        self.set_preceding(Message.PRECEDING_COMMAND)
        self.set_type(type)
        self.set_object(object)
        self.set_data(data)

class Parser(object):
    def __init__(self):
        pass

    def parse(self, raw_message):
        msg = Message()

        preceding = raw_message[0]
        type = raw_message[1]
        object = raw_message[2:5]
        data = str(raw_message[5:-1])
        terminal = raw_message[-1]

        if not terminal == Message.TERMINAL:
            raise CommunicationError("Invalid message given. Terminal did not match")

        # ignore the leading whitespace
        if data[0] == Message.SEPARATOR:
            data = data[1:]

        if data == '':
            data = None

        try:
            msg.set_preceding(preceding)
            msg.set_type(type)
            msg.set_object(object)
            msg.set_data(data)
        except ValueError as e:
            raise CommunicationError("Invalid message given" + str(e))

        return msg


