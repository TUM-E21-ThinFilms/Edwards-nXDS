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
from message import Message


class Status(object):
    def __init__(self, status_message):
        data = status_message.split(Message.DATA_SEPARATOR)
        self._speed_in_hz = data[0]
        self._register1 = SystemRegister1(data[1])
        self._register2 = SystemRegister2(data[2])
        self._warning = WarningRegister(data[3])
        self._fault = FaultRegister(data[4])

    def get_rotation(self):
        return self._speed_in_hz

    def get_register1(self):
        return self._register1

    def get_register2(self):
        return self._register2

    def get_warning(self):
        return self._warning

    def get_fault(self):
        return self._fault


class StatusRegister(object):
    BIT_0 = 1
    BIT_1 = 1 << 1
    BIT_2 = 1 << 2
    BIT_3 = 1 << 3
    BIT_4 = 1 << 4
    BIT_5 = 1 << 5
    BIT_6 = 1 << 6
    BIT_7 = 1 << 7
    BIT_8 = 1 << 8
    BIT_9 = 1 << 9
    BIT_10 = 1 << 10
    BIT_11 = 1 << 11
    BIT_12 = 1 << 12
    BIT_13 = 1 << 13
    BIT_14 = 1 << 14
    BIT_15 = 1 << 15

    def __init__(self, hex_register):
        if not len(hex_register) == 4:
            raise ValueError("Given hexadecimal register must be of length 4")

        self._hex_register = hex_register
        self._reg1 = int(self._hex_register[0], 16)
        self._reg2 = int(self._hex_register[0], 16)
        self._reg3 = int(self._hex_register[0], 16)
        self._reg4 = int(self._hex_register[0], 16)

        self._register = self._reg1 + self._reg2 << 4 + self._reg3 << 8 + self._reg4 << 12

    def get_register(self):
        return self._register

    def __and__(self, bits):
        return self._register & bits

    def __or__(self, bits):
        return self._register | bits

    def __xor__(self, other):
        return self._register ^ other


class SystemRegister1(StatusRegister):
    FLAG_DECELERATION = StatusRegister.BIT_0
    FLAG_ACCELERACTION_RUNNING = StatusRegister.BIT_1
    FLAG_STANDBY_SPEED = StatusRegister.BIT_2
    FLAG_NORMAL_SPEED = StatusRegister.BIT_3
    FLAG_ABOVE_RAMP_SPEED = StatusRegister.BIT_4
    FLAG_ABOVE_OVERLOAD_SPEED = StatusRegister.BIT_5
    FLAG_CONTROL_MODE = StatusRegister.BIT_6 | StatusRegister.BIT_7 | StatusRegister.BIT_13
    FLAG_SERIAL_ENABLE = StatusRegister.BIT_10

    CONTROL_MODE_NONE = 0
    CONTROL_MODE_SERIAL = 1
    CONTROL_MODEL_PARALLEL = 2
    CONTROL_MODE_MANUAL = 4
    CONTROL_MODE_RESERVED = 8

    def flag_deceleration(self):
        return self._register & self.FLAG_DECELERATION

    def flag_acceleration(self):
        return self._register & self.FLAG_ACCELERACTION_RUNNING

    def flag_running(self):
        return self._register & self.FLAG_ACCELERACTION_RUNNING

    def flag_standby_speed(self):
        return self._register & self.FLAG_STANDBY_SPEED

    def flag_normal_speed(self):
        return self._register & self.FLAG_NORMAL_SPEED

    def flag_above_ramp_speed(self):
        return self._register & self.FLAG_ABOVE_RAMP_SPEED

    def flag_above_overload_speed(self):
        return self._register & self.FLAG_ABOVE_OVERLOAD_SPEED

    def flag_serial_enable(self):
        return self._register & self.FLAG_SERIAL_ENABLE

    def get_control_mode(self):
        mode = self._register & self.FLAG_CONTROL_MODE
        if mode == 0:
            return self.CONTROL_MODE_NONE
        elif mode == 1:
            return self.CONTROL_MODE_SERIAL
        elif mode == 2:
            return self.CONTROL_MODEL_PARALLEL
        elif mode == 3:
            return self.CONTROL_MODE_MANUAL
        else:
            return self.CONTROL_MODE_RESERVED


class SystemRegister2(StatusRegister):
    FLAG_UPPER_POWER_REGULATOR_ACTIVE = StatusRegister.BIT_0
    FLAG_LOWER_POWER_REGULATOR_ACTIVE = StatusRegister.BIT_1
    FLAG_UPPER_VOLTAGE_REGULATOR_ACTIVE = StatusRegister.BIT_2
    FLAG_SERVICE_DUE = StatusRegister.BIT_4
    FLAG_WARNING = StatusRegister.BIT_6
    FLAG_ALARM = StatusRegister.BIT_7

    def flag_upper_power_regulator_active(self):
        return self._register & self.FLAG_UPPER_POWER_REGULATOR_ACTIVE

    def flag_lower_power_regulator_active(self):
        return self._register & self.FLAG_LOWER_POWER_REGULATOR_ACTIVE

    def flag_upper_voltage_regulator_active(self):
        return self._register & self.FLAG_UPPER_VOLTAGE_REGULATOR_ACTIVE

    def flag_service_due(self):
        return self._register & self.FLAG_SERVICE_DUE

    def flag_warning(self):
        return self._register & self.FLAG_WARNING

    def flag_alarm(self):
        return self._register & self.FLAG_ALARM


class WarningRegister(StatusRegister):
    FLAG_LOW_TEMPERATURE = StatusRegister.BIT_1
    FLAG_TEMPERATURE_REGULATOR_ACTIVE = StatusRegister.BIT_6
    FLAG_HIGH_TEMPERATURE = StatusRegister.BIT_10
    FLAG_SELF_TEST_WARNING = StatusRegister.BIT_15

    def flag_low_temperature(self):
        return self._register & self.FLAG_LOW_TEMPERATURE

    def flag_temperature_regulator_active(self):
        return self._register & self.FLAG_TEMPERATURE_REGULATOR_ACTIVE

    def flag_high_temperature(self):
        return self._register & self.FLAG_HIGH_TEMPERATURE

    def flag_self_test_warning(self):
        return self._register & self.FLAG_SELF_TEST_WARNING


class FaultRegister(StatusRegister):
    FLAG_OVER_VOLTAGE_TRIP = StatusRegister.BIT_1
    FLAG_OVER_CURRENT_TRIP = StatusRegister.BIT_2
    FLAG_OVER_TEMPERATURE_TRIP = StatusRegister.BIT_3
    FLAG_UNDER_TEMPERATURE_TRIP = StatusRegister.BIT_4
    FLAG_POWER_STAGE_FAULT = StatusRegister.BIT_5
    FLAG_HW_FAULT_LATCH_SET = StatusRegister.BIT_8
    FLAG_EEPROM_FAULT = StatusRegister.BIT_9
    FLAG_NO_PARAMETER_SET = StatusRegister.BIT_11
    FLAG_SELF_TEST_FAULT = StatusRegister.BIT_12
    FLAG_SERIAL_CONTROL_MODE_INTERLOCK = StatusRegister.BIT_13
    FLAG_OVERLOAD_TIMEOUT = StatusRegister.BIT_14
    FLAG_ACCELERATION_TIMEOUT = StatusRegister.BIT_15


class ServiceRegister(StatusRegister):
    FLAG_TIP_SEAL_SERVICE_DUE = StatusRegister.BIT_0
    FLAG_BEARING_SERVICE_DUE = StatusRegister.BIT_1
    FLAG_CONTROLLER_SERVICE_DUE = StatusRegister.BIT_3
    FLAG_SERVICE_DUE = StatusRegister.BIT_7

    def flag_service_due(self):
        return self._register & self.FLAG_SERVICE_DUE

    def flag_tip_seal_service_due(self):
        return self._register & self.FLAG_TIP_SEAL_SERVICE_DUE

    def flag_bearig_service_due(self):
        return self._register & self.FLAG_BEARING_SERVICE_DUE

    def flag_controller_service_due(self):
        return self._register & self.FLAG_CONTROLLER_SERVICE_DUE
