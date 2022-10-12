from qmi8658 import QMI8658
import busio
import board
import rtc

i2c_bus = busio.I2C(board.GP7, board.GP6)

imu = QMI8658(i2c_bus)

clock = rtc.RTC()

while True:
    time.sleep(0.5)
    print(clock.datetime)
    print(imu.xyz)
    # imu.xyz > 0 up
    # imu.xyz <= 0 down
    if (imu.xyz[0] > 0):
        print('down')
    if (imu.xyz[0] <= 0):
        print('up')
    print(imu.tap)