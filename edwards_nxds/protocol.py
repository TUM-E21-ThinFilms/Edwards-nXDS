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

from edwards_nxds.message import Message, Parser

from e21_util.serial_connection import AbstractTransport, SerialTimeoutException
from e21_util.interface import Loggable


class EdwardsNXDSProtocol(Loggable):
    def __init__(self, transport, logger):
        super(EdwardsNXDSProtocol, self).__init__(logger)
        assert isinstance(transport, AbstractTransport)

        self._transport = transport
        self._parser = Parser()

    def get_response(self):
        raw_response = self._transport.read_until(Message.TERMINAL)

        # convert byte-array to string
        raw_resp = "".join([chr(x) for x in raw_response])

        self._logger.debug('Received message "{}"'.format(raw_resp))
        return self._parser.parse(raw_resp)

    def send_message(self, msg):
        raw = msg.get_raw()
        self._transport.write(raw)

    def query(self, msg):
        if not isinstance(msg, Message):
            raise TypeError("message must be an instance of Message")

        with self._transport:
            self._logger.debug('Sending message {}'.format(msg))

            self.send_message(self._transport, msg)

            return self.get_response()

    def clear(self):
        with self._transport:
            self._logger.debug("Clearing buffer ...")
            try:
                while True:
                    self._transport.read_bytes(25)
            except SerialTimeoutException:
                pass

    def write(self, message):
        return self.query(message)
