import board
import displayio
import busio
import pwmio
import os
import gc
from gc9a01 import GC9A01
# from qmi8685 import QMI8685
import time
# import adafruit_imageload
from qmi8658 import QMI8658

i2c_bus = busio.I2C(board.GP7, board.GP6)

imu = QMI8658(i2c_bus)

useOnDisk = True

displayio.release_displays()

spi = busio.SPI(board.GP10, board.GP11)
while not spi.try_lock():
    pass
spi.configure(baudrate=24000000)  # Configure SPI for 24MHz
spi.unlock()

cs = board.GP9
dc = board.GP8
reset = board.GP12

display_bus = displayio.FourWire(spi, command=dc, chip_select=cs, reset=reset)

bl = board.GP25
display = GC9A01(display_bus, width=240, height=240, backlight_pin=bl)

display.brightness = 0

def fade_up_backlight():
  for i in range(100):
    display.brightness = i / 100.0
    time.sleep(0.01)
def fade_down_backlight():
  for i in range(100):
    display.brightness = (100-i) / 100.0
    time.sleep(0.01)


# Make the display context
splash = displayio.Group()

# image, palette = adafruit_imageload.load("/4x.bmp")
# Create a TileGrid to hold the bitmap

#image, palette = adafruit_imageload.load("img/zorb.bmp")
#tile_grid = displayio.TileGrid(image, pixel_shader=palette)
# bitmap = displayio.OnDiskBitmap("/img/zorb.bmp")
# tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

# Add the TileGrid to the Group
#splash.append(tile_grid)

display.show(splash)


file_names = os.listdir('img/slides')
print(file_names)
at_file = 0

def isUp():
    return imu.xyz[0] < 0
image = None
palette = None

is_zorb = True

splash.append(displayio.Group())  # placeholder, will be replaced w/ screen[0] below
while True:
  file_name = 'img/zorb.bmp'
  if isUp():
    is_zorb = False
    print('slideshow')
    file_name = '/img/slides/{}'.format(file_names[at_file % len(file_names)])
    at_file += 1
  else:
    is_zorb = True

  fade_down_backlight()
  splash.pop()
  time.sleep(0.2)
  
  print(file_name)
  
  print(gc.mem_free())
  gc.collect()
  time.sleep(0.2)
  print(gc.mem_free())
  
  if not useOnDisk:
    image, palette = adafruit_imageload.load(file_name)
    splash.append(displayio.TileGrid(image, pixel_shader=palette))
  else:
    image = displayio.OnDiskBitmap(file_name)
    splash.append(displayio.TileGrid(image, pixel_shader=image.pixel_shader))
  display.refresh()
  time.sleep(0.5)
  fade_up_backlight()
  time.sleep(4)
  while not isUp() and is_zorb:
      print(imu.xyz)
      print('waiting to go down')
      time.sleep(1)
