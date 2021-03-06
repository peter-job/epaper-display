#!/usr/bin/env python

import os
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from datetime import datetime
import random
import glob
import socket
import time


print("""
C A R D B O A R D   C A F E
---- inky phat display ----
""")

# Get the current path
PATH = os.path.dirname(__file__)


# Set up the Inky display
try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

try:
    inky_display.set_border(inky_display.BLACK)
except NotImplementedError:
    pass

# Setup display font 
fnt = ImageFont.truetype(os.path.join(PATH, "resources/SF-Mono-Medium.otf"), 20)

while(1):

    # Create Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)

    # Connect to MC01
    minecraft_status = "MC01:"
    result = sock.connect_ex(('minecraft.cardboard.cafe', 25565))
    if result == 0:
        minecraft_status += "O.K."
    else:
        minecraft_status += "DOWN"

    # Connect to Cardboard Cafe
    cafe_status = "CAFE:"
    result = sock.connect_ex(('cardboard.cafe', 443))
    if result == 0:
        cafe_status += "O.K."
    else:
        cafe_status += "DOWN"

    # Draw Image
    img = Image.open(os.path.join(PATH, "resources/background.png"))
    draw = ImageDraw.Draw(img)
    draw.text((120, 66), minecraft_status, font=fnt, fill=inky_display.BLACK)
    draw.text((120, 90), cafe_status, font=fnt, fill=inky_display.BLACK)

    # Display 
    inky_display.h_flip = True
    inky_display.v_flip = True
    inky_display.set_image(img)
    inky_display.show()

    # Create Output Directory If Not Exists
    try:
        os.makedirs(os.path.join(PATH, "output"))
    except OSError:
        if not os.path.isdir(os.path.join(PATH, "output")):
            raise
    
    # Save Image
    img.save(os.path.join(PATH, "output/latest.png"))

    # Print Timestamp
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    print "updated @ " + current_time

    # Sleep
    time.sleep(300)


def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
        """Create a transparency mask.

        Takes a paletized source image and converts it into a mask
        permitting all the colours supported by Inky pHAT (0, 1, 2)
        or an optional list of allowed colours.

        :param mask: Optional list of Inky pHAT colours to allow.

        """
        mask_image = Image.new("1", source.size)
        w, h = source.size
        for x in range(w):
            for y in range(h):
                p = source.getpixel((x, y))
                if p in mask:
                    print p
                    mask_image.putpixel((x, y), 255)
                else:
                    print p
        return mask_image

def invert_image(source):
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p == inky_display.WHITE:
                source.putpixel((x, y), inky_display.BLACK)
            if p == inky_display.BLACK:
                source.putpixel((x, y), inky_display.WHITE)

    return source

def swap_colour(source, a, b):
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p == a:
                source.putpixel((x, y), b)

    return source