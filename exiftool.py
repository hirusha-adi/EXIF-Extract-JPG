#!/usr/bin/env python3

import csv
import os
import sys
from datetime import datetime

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

    notSlient = not(silentMode)
    if notSlient:
        if showLogo:
            print(__LOGO__)
            if debug:
                print(f"DEBUG: {datetime.now()}: Printed logo")

    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, "images"))

    if notSlient:
        if debug:
            print(
                f"DEBUG: {datetime.now()}: using images folder at {os.path.join(cwd, 'images')}")

        if verbosity:
            print(f"+ Selecting image folder at {os.path.join(cwd, 'images')}")

    files = os.listdir()  # in ./images

    if len(files) == 0:
        if notSlient:
            print("You don't have have files in the ./images folder.")
        sys.exit()

    if notSlient:
        if verbosity:
            print(f"+ Found {len(files)} in the images folder")

        if debug:
            print(
                f"DEBUG: {datetime.now()}: Found {len(files)} in the images folder")

    with open(f"..{SLASH}{outputFileName}", "a", newline="") as csv_file:
        writer = csv.writer(csv_file)

        if notSlient:
            if verbosity:
                print(f"+ Opened ..{SLASH}{outputFileName} in append mode")

            if debug:
                print(
                    f"DEBUG: {datetime.now()}: Opened ..{SLASH}{outputFileName} in append-text mode")

        for file in files:
            try:
                if notSlient:
                    if debug:
                        print(
                            f"DEBUG: {datetime.now()}: Trying to open image: {file}")

                image = Image.open(file)  # opening in binary format

                if notSlient:
                    if verbosity:
                        print(f"+ Opened image: {image}")

                    if debug:
                        print(
                            f"DEBUG: {datetime.now()}: Opened image successfully")

                print(
                    f"_______________________________________________________________{file}_______________________________________________________________")
                gps_coords = {}

                writer.writerow(("Filename", file))

                if notSlient:
                    if debug:
                        print(
                            f"DEBUG: {datetime.now()}: Wrote 'Filename': {file} to csv")

                # The ._getexif() method returns a dictionary. .items() method returns a list of all dictionary keys and values.
                if image._getexif() == None:
                    writer.writerow((file, "Contains no exif data."))

                    if notSlient:
                        if verbosity:
                            print("Contains no exif data.")

                        if debug:
                            print(
                                f"DEBUG: {datetime.now()}: Unable to find any metadata in the current image ({file})")

                else:  # exif data exists

                    if notSlient:
                        if verbosity:
                            print("+ Found existing metadata")

                        if debug:
                            print(
                                f"DEBUG: {datetime.now()}: Found metadata in the current image ({image})")

                    for tag, value in image._getexif().items():

                        # decimal number in exif standard - https://exiv2.org/tags.html
                        # we use get to make it human readable
                        tag_name = TAGS.get(tag)

                        if notSlient:
                            if debug:
                                print(
                                    f"DEBUG: {datetime.now()}: Converted the tag name to a human understanble form")

                        if tag_name == "GPSInfo":

                            if notSlient:
                                if verbosity:
                                    print("+ found GPS Information")

                                if debug:
                                    print(
                                        f"DEBUG: {datetime.now()}: Found GPS information")

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

                            if notSlient:
                                if verbosity:
                                    print(f"+ {tag_name}: {value}")

                                if debug:
                                    print(
                                        f"DEBUG: {datetime.now()}: Wrote '{tag_name}:{value}' to the opened csv file")

                    if gps_coords:
                        google_maps_url = create_google_maps_url(gps_coords)

                        if notSlient:
                            if verbosity:
                                print(f"+ Good Maps Link: {google_maps_url}")

                            if debug:
                                print(
                                    f"DEBUG: {datetime.now()}: Sucessfully created a Google Maps URL for the image location: {google_maps_url}")

                        writer.writerow(
                            ("Google Maps Link", google_maps_url))

                        if notSlient:
                            if debug:
                                print(
                                    f"DEBUG: {datetime.now()}: Wrote 'Google Maps Link:{google_maps_url}' to the opened csv file")

            except IOError:

                if notSlient:
                    if debug:
                        print(
                            f"DEBUG: {datetime.now()}: Image.open() raised IOError. Unsupported file types")

                    print("File format not supported!")

    os.chdir(cwd)


if __name__ == "__main__":

    import argparse

    # https://docs.python.org/3/howto/argparse.html

    parser = argparse.ArgumentParser(
        description='Extract EXIF data from images. This program is for .JPG and .TIFF format files. \nThe program coule be extended to support .HEUI, .PNG and other formats. \nNote that most social media sities strip exif data from uploaded photos')

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

    parser.add_argument("-s", "--silent",
                        help="dont print the logo of the script",
                        action="store_true")

    args = parser.parse_args()

    verbosity = None
    if args.verbose:
        verbosity = True
        debugmode = False
        silentMode = False

    debugmode = None
    if args.debug:
        debugmode = True
        verbosity = False
        silentMode = False

    silentMode = None
    if args.silent:
        silentMode = True
        verbosity = False
        debugmode = False

    showLogo = None
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
