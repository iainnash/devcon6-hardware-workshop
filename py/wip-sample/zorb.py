from display import display
import displayio
import adafruit_imageload
import time

# Make the display context
splash = displayio.Group()

image, palette = adafruit_imageload.load("/images/z1.bmp")
# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(image, pixel_shader=palette, tile_width=240, tile_height=240, width=1, height=1)

# Add the TileGrid to the Group
splash.append(tile_grid)

display.show(splash)



while True:
    pass