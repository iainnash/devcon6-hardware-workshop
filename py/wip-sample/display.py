import board
import displayio
import busio
from gc9a01 import GC9A01

displayio.release_displays()

spi = busio.SPI(board.GP10, board.GP11)
while not spi.try_lock():
    pass
spi.configure(baudrate=80000000)  # Configure SPI for 24MHz
spi.unlock()

cs = board.GP9
dc = board.GP8
reset = board.GP12


display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=reset)

bl = board.GP25
display = GC9A01(display_bus, width=240, height=240, backlight_pin=bl)
