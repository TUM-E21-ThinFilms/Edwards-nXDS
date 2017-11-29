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

from slave.driver import Driver, Command
from slave.types import Mapping, Float, String, Integer, Boolean, SingleType
from protocol import EdwardsNXDSProtocol
from message import Query, Command, Message
from status import Status, ServiceRegister

class EdwardsNXDSDriver(Driver):

    def __init__(self, transport, protocol):

        assert isinstance(protocol, EdwardsNXDSProtocol)
        self.thread = None
        super(EdwardsNXDSDriver, self).__init__(transport, protocol)

    def send(self, message):
        if not isinstance(message, Message):
            raise ValueError("Given message is not an instance of Message")

        if isinstance(message, Query):
            return self._protocol.query(self._transport, message)

        if isinstance(message, Command):
            return self._protocol.write(self._transport, message)

        return self._protocol.query(self._transport, message)

    def clear(self):
        self._protocol.clear(self._transport)

    def get_pump_type(self):
        return self.send(Query(Query.TYPE_STATIC, 801))

    def start_pump(self):
        return self.send(Command(Query.TYPE_COMMAND, 802, '1'))

    def stop_pump(self):
        return self.send(Command(Query.TYPE_COMMAND, 802, '0'))

    def get_status(self):
        return self.send(Query(Query.TYPE_VOLATILE, 802))

    def speed_control(self, full_speed=True):
        if full_speed:
            speed = "0"
        else:
            speed = "1"

        return self.send(Command(Query.TYPE_STATIC, 803, speed))

    def get_normal_speed(self):
        return self.send(Query(Query.TYPE_STATIC, 804))

    def set_normal_speed(self, speed):
        speed = int(speed)
        if not(50 <= speed <= 100):
            raise ValueError("Given speed must be in [50, 100]")

        return self.send(Command(Command.TYPE_STATIC, 804, str(speed)))

    def get_standby_speed(self):
        return self.send(Query(Query.TYPE_STATIC, 805))

    def set_standby_speed(self, speed, volatile=False):
        type = Command.TYPE_STATIC

        if volatile:
            type = Command.TYPE_COMMAND

        speed = int(speed)
        if not (66 <= speed <= 100):
            raise ValueError("Given speed must be in [66, 100]")

        return self.send(Command(type, 805, str(speed)))

    def get_autorun(self):
        return self.send(Query(Query.TYPE_STATIC, 806))

    def set_autorun(self, enable):
        if enable:
            enable = '1'
        else:
            enable = '0'

        return self.send(Command(Command.TYPE_STATIC, 806, enable))

    def get_temperature(self):
        return self.send(Query(Query.TYPE_VOLATILE, 808))

    def get_run_hours(self):
        return self.send(Query(Query.TYPE_VOLATILE, 810))

    def get_pump_cycles(self):
        return self.send(Query(Query.TYPE_VOLATILE, 811))

    def get_service_status(self):
        return ServiceRegister(self.send(Query(Query.TYPE_VOLATILE, 826)).get_data())

    def get_status(self):
        return Status(self.send(Query(Query.TYPE_VOLATILE, 802)))
