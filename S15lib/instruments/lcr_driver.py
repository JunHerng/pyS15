"""
Created on 8 July 2020
by Chin Chean Lim, Mathias Seidler
"""

from . import serial_connection
# import time


class LCRDriver(object):
    """Module for communicating with the liquid crystal variable phase retarder"""

    DEVICE_IDENTIFIER = 'LCD cell driver'

    def __init__(self, device_path=''):
        # if no path is indicated it tries to init the first power_meter device
        if device_path == '':
            device_path = (serial_connection.search_for_serial_devices(
                self.DEVICE_IDENTIFIER))[0]
            print('Connected to', device_path)
        self._com = serial_connection.SerialConnection(device_path)

    def reset(self):
        '''Resets the device.

        Returns:
            str: Response of the device after.
        '''
        return self._com.write(b'*RST')

    def all_channels_on(self):
        """Switches all channels on, to a frequency of 2000 and switches off the LED.
        """        
        self._com.write(b'ON\r\n')
        self._com.write(b'DARK\r\n')
        self._com.write(b'FREQ 2000\r\n')

    def set_voltage(self, channel: int, voltage: float):
        """Sets the voltage of an output channel.

        Args:
            channel (int): channel number. Select from 1 to 4.
            voltage (float): Set voltage in volts.

        Raises:
            Exception: When the voltage is below 0 volts or higher than 10 volts.
        """
        if voltage < 10 and voltage >= 0:
            self._com.write(('AMPLITUDE {} {}\r\n'.format(channel, voltage)).encode())
        else:
            raise Exception('Voltage to high')

    def read_voltage(self, channel: int) -> float:
        """Returns voltage of a channel

        Args:
            channel (int): Select from 1 to 4.

        Returns:
            float: Voltage of the selected channel.
        """
        cmd = 'AMP? ' + str(channel)
        return float(self._com._getresponse(cmd))

    @property
    def V1(self):
        """Property which shows voltage of channel 1.

        Returns:
            float: voltage in volts
        """        
        return float(self._com._getresponse_1l('AMP? 1'))

    @V1.setter
    def V1(self, V1: float):
        """Property setter of the voltage of channel 1.

        Args:
            V1 (float): Voltage in volts.
        """
        self._com.write(('AMPLITUDE 1 {}\r\n'.format(V1)).encode())

    @property
    def V2(self):
        return self._com._getresponse_1l('AMP? 2')

    @V2.setter
    def V2(self, value):
        self._com.write(('AMPLITUDE 2 {}\r\n'.format(value)).encode())

    @property
    def V3(self):
        return self._com._getresponse_1l('AMP? 3')

    @V3.setter
    def V3(self, value):
        self._com.write(('AMPLITUDE 3 {}\r\n'.format(value)).encode())

    @property
    def V4(self):
        return self._com._getresponse_1l('AMP? 4')

    @V4.setter
    def V4(self, value):
        self._com.write(('AMPLITUDE 4 {}\r\n'.format(value)).encode())

    @property
    def identity(self) -> str:
        """Returns identy string. Contains information about the device.

        Returns:
            str: Identity string.
        """
        return self._com._getresponse_1l('*idn?')

    def help(self):
        return self._com.help()
