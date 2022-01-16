#!/usr/bin/env python3

# This program is for .JPG and .TIFF format files.
# The program could be extended to support .HEIC, .PNG and other formats.
# Note most social media sites strip exif data from uploaded photos.

# 2. Add .jpg images downloaded from Flickr to subfolder ./images from where the script is stored.


import csv
from enum import Flag
import os
from re import T
import sys

from src.utils import __LOGO__, SLASH, create_google_maps_url, pip_install

try:
    from PIL import Image
    from PIL.ExifTags import GPSTAGS, TAGS
except ImportError:
    pip_install("Pillow")
    from PIL import Image
    from PIL.ExifTags import GPSTAGS, TAGS


def EXIF_TOOL(showLogo: bool = True,
              debug: bool = False,
              verbosity: bool = False,
              silentMode: bool = False,
              outputFileName: str = "output.csv"):
    print(__LOGO__)

    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, "images"))
    files = os.listdir()  # in ./images

    if len(files) == 0:
        print("You don't have have files in the ./images folder.")
        sys.exit()

    with open(f"..{SLASH}exif_data.csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file)  # CSV Writer

        for file in files:
            try:
                image = Image.open(file)  # opening in binary format
                print(
                    f"_______________________________________________________________{file}_______________________________________________________________")
                gps_coords = {}

                writer.writerow(("Filename", file))

                # The ._getexif() method returns a dictionary. .items() method returns a list of all dictionary keys and values.
                if image._getexif() == None:
                    writer.writerow((file, "Contains no exif data."))
                else:  # exif data exists
                    for tag, value in image._getexif().items():
                        # decimal number in exif standard - https://exiv2.org/tags.html
                        # we use get to make it human readable
                        tag_name = TAGS.get(tag)
                        if tag_name == "GPSInfo":
                            for key, val in value.items():
                                writer.writerow((GPSTAGS.get(key), {val}))
                                if GPSTAGS.get(key) == "GPSLatitude":
                                    gps_coords["lat"] = val
                                elif GPSTAGS.get(key) == "GPSLongitude":
                                    gps_coords["lon"] = val
                                elif GPSTAGS.get(key) == "GPSLatitudeRef":
                                    gps_coords["lat_ref"] = val
                                elif GPSTAGS.get(key) == "GPSLongitudeRef":
                                    gps_coords["lon_ref"] = val
                        else:
                            writer.writerow((tag_name, value))
                    if gps_coords:
                        writer.writerow(
                            ("Google Maps Link", create_google_maps_url(gps_coords)))
            except IOError:
                print("File format not supported!")

    os.chdir(cwd)


if __name__ == "__main__":

    import argparse
    # https://docs.python.org/3/howto/argparse.html

    parser = argparse.ArgumentParser(
        description='extract EXIF data from images')

    parser.add_argument("-o", "--output",
                        help="display a square of a given number",
                        default="output.csv")

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-d", "--debug",
                        help="print everything happening to the user",
                        action="store_true")

    parser.add_argument("-nl", "--nologo",
                        help="dont print the logo of the script",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        verbosity = True
        debugmode = False
        silentMode = False

    if args.debug:
        debugmode = True
        verbosity = False
        silentMode = False

    if args.silent:
        silentMode = True
        verbosity = False
        debugmode = False

    if args.nologo:
        showLogo = False

    if str(args.output).endswith(".csv"):
        outputFileName = str(args.output)
    else:
        outputFileName = str(args.output) + ".csv"

    try:
        EXIF_TOOL(showLogo=showLogo,
                  debug=debugmode,
                  verbosity=verbosity,
                  silentMode=silentMode,
                  outputFileName=outputFileName)
    except Exception as e:
        print("Error:", e)
