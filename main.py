#!/usr/bin/env python3

# This program is for .JPG and .TIFF format files.
# The program could be extended to support .HEIC, .PNG and other formats.
# Note most social media sites strip exif data from uploaded photos.

# python3 -m pip install --upgrade pip
# python3 -m pip install --upgrade Pillow
# 2. Add .jpg images downloaded from Flickr to subfolder ./images from where the script is stored.

from src.utils import __LOGO__, create_google_maps_url, pip_install

import csv
import os

try:
    from PIL.ExifTags import GPSTAGS, TAGS
    from PIL import Image
except ImportError:
    pip_install("Pillow")
    from PIL.ExifTags import GPSTAGS, TAGS
    from PIL import Image

print(__LOGO__)
