from adafruit_register.i2c_struct import ROUnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits
from adafruit_bus_device import i2c_device


_QMI8658_WHOAMI = const(0x0)
_QMI8658_WHOAMI_VALUE = const(0x5)
_QMI8658_CTRL1 = const(0x2)
_QMI8658_CTRL2 = const(0x3)
_QMI8658_CTRL3 = const(0x4)
_QMI8658_CTRL4 = const(0x5)
_QMI8658_CTRL5 = const(0x6)
_QMI8658_CTRL6 = const(0x7)
_QMI8658_CTRL7 = const(0x8)
_QMI8658_CTRL8 = const(0x9)
_QMI8658_OUT_ACCEL_XYZ = const(0x35)
_QMI8658_TEMP = const(0x33)
_QMI8658_TAP_DATA = const(0x2f)

def convert_16bit_2s_compliment(data):
    if data > 32767:
        return data - 65535
    return data

class QMI8658(object):
    _chip_id = ROUnaryStruct(_QMI8658_WHOAMI, '<b')
    
    _ctrl1_mode = RWBits(8, _QMI8658_CTRL1, 0)
    _ctrl2_mode = RWBits(8, _QMI8658_CTRL2, 0)
    _ctrl3_mode = RWBits(8, _QMI8658_CTRL3, 0)
    _ctrl4_mode = RWBits(8, _QMI8658_CTRL4, 0)
    _ctrl5_mode = RWBits(8, _QMI8658_CTRL5, 0)
    _ctrl6_mode = RWBits(8, _QMI8658_CTRL6, 0)

    _ctrl7_mode = RWBits(8, _QMI8658_CTRL7, 0)
    _ctrl8_mode = RWBits(8, _QMI8658_CTRL8, 0)

    _xyz_data = Struct(_QMI8658_OUT_ACCEL_XYZ, '<HHH')
    _temp_data = Struct(_QMI8658_TEMP, '<H')

    _tap_data = ROUnaryStruct(_QMI8658_TAP_DATA, '<bb')

    def __init__(self, bus, address = 0x6b):
        self._address = address
        self.i2c_device = i2c_device.I2CDevice(bus, address)
        if self._chip_id != _QMI8658_WHOAMI_VALUE:
            raise RuntimeError('Chip ID is wrong')    
        self._ctrl1_mode = 0x60
        self._ctrl2_mode = 0x23
        self._ctrl3_mode = 0x53
        self._ctrl4_mode = 0x00
        self._ctrl5_mode = 0x11
        self._ctrl6_mode = 0x00
        self._ctrl7_mode = 0x03
        self._ctrl8_mode = 0x1
    
    def _scale_x1_data(self, data):
        return data
    
    @property
    def temp(self):
      print(bin(self._temp_data[0]))
      return convert_16bit_2s_compliment(self._temp_data[0]) / 256

    @property
    def xyz(self):
        d = self._xyz_data
        out = [0, 0, 0]
        for i in range(3):
            out[i] = float(convert_16bit_2s_compliment(d[i])) / float(1<<12)
        return out
    
    # todo
    @property
    def tap(self):
        return self._tap_data[1] == 0x1

