import struct
from adafruit_register.i2c_struct import ROUnaryStruct, Struct
from adafruit_register.i2c_bits import RWBits
from adafruit_register.i2c_bit import RWBit, ROBit
from adafruit_bus_device import i2c_device


_QMI8685_WHOAMI = const(0x0)
_QMI8685_WHOAMI_VALUE = const(0x05)
_QMI8685_CTRL1 = const(0x2)
_QMI8685_CTRL2 = const(0x3)
_QMI8685_CTRL3 = const(0x4)
_QMI8685_CTRL4 = const(0x5)
_QMI8685_CTRL5 = const(0x6)
_QMI8685_CTRL6 = const(0x7)
_QMI8685_CTRL7 = const(0x8)
_QMI8685_RAW_OUT_XYZ_ACCEL = const(0x35)
_QMI8685_RAW_OUT_XYZ_GYRO = const(0x3b)

class QMI8685(object):
    _chip_id = ROUnaryStruct(_QMI8685_WHOAMI, "<b")
    
    _ctrl1_mode = RWBits(8, _QMI8685_CTRL1, 0)
    _ctrl2_mode = RWBits(8, _QMI8685_CTRL2, 0)
    _ctrl3_mode = RWBits(8, _QMI8685_CTRL3, 0)
    _ctrl4_mode = RWBits(8, _QMI8685_CTRL4, 0)
    _ctrl5_mode = RWBits(8, _QMI8685_CTRL5, 0)
    _ctrl6_mode = RWBits(8, _QMI8685_CTRL6, 0)

    _ctrl7_mode = RWBits(8, _QMI8685_CTRL7, 0)

    _raw_accel_data = Struct(_QMI8685_RAW_OUT_XYZ_ACCEL, '<hhh')
    _raw_gyro_xyz_data = Struct(_QMI8685_RAW_OUT_XYZ_GYRO, '<hhh')


    def __init__(self, bus, address = 0x6b):
        self._address = address
        self.i2c_device = i2c_device.I2CDevice(bus, address)
        if self._chip_id != _QMI8685_WHOAMI_VALUE:
            raise RuntimeError('Chip ID is wrong')    
        self._ctrl1_mode = 0x60
        self._ctrl2_mode = 0x23
        self._ctrl3_mode = 0x53
        self._ctrl4_mode = 0x00
        self._ctrl5_mode = 0x11
        self._ctrl6_mode = 0x00
        self._ctrl7_mode = 0x03
    
    def _scale_x1_data(self, data):
        return data

    @property
    def acceleration(self):
        d = self._raw_accel_data
        return (
            self._scale_x1_data(d[0]),
            self._scale_x1_data(d[1]),
            self._scale_x1_data(d[2])
        )


    