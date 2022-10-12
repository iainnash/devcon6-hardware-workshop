# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This is an animation to demonstrate the use of Circle Setter Attribute.
"""

import time
import gc
import displayio
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label
from display import display
import terminalio


# Make the display context
main_group = displayio.Group()

# Make a background color fill
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)

# Setting up the Circle starting position
posx = 120
posy = 120

# Define Circle characteristics
circle_radius = 20
circle = Circle(posx, posy, circle_radius, fill=0x00FF00, outline=0xFF00FF)
main_group.append(circle)

text_area_middle_middle = label.Label(terminalio.FONT, text=str(block_number))
text_area_middle_middle.anchor_point = (0.5, 0.5)
text_area_middle_middle.anchored_position = (display.width / 2, display.height / 2)
main_group.append(text_area_middle_middle)

block_number = 10001

# Showing the items on the screen
display.show(main_group)

going_up = True

while True:
    if going_up:
        circle_radius += 0.1
    else:
        circle_radius -= 0.1
    if not going_up and circle_radius == 0:
        going_up = True
    if going_up and circle_radius == 240:
        going_up = False
    
    circle2 = Circle(posx, posy, int(circle_radius), fill=0x00FF00, outline=0xFF00FF)
    main_group.append(circle2)
    #main_group.remove(circle)
    
    display.refresh()

    time.sleep(0.1)
    gc.collect()
