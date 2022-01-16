import os

from .errors import ModuleNameMissingError

if os.name == 'nt':
    PIP = "pip"
    CLEAR = "cls"
    PYTHON = "python"
    SLASH = "\\"
else:
    PIP = "pip3"
    CLEAR = "cls"
    PYTHON = "python3"
    SLASH = "/"

__LOGO__ = r"""
 _______  _____ _____   _____           _ 
| ____\ \/ /_ _|  ___| |_   _|__   ___ | |
|  _|  \  / | || |_ _____| |/ _ \ / _ \| |
| |___ /  \ | ||  _|_____| | (_) | (_) | |
|_____/_/\_\___|_|       |_|\___/ \___/|_|
"""


def pip_install(module_name: str = None):
    if module_name is None:
        raise ModuleNameMissingError(
            message="No module name is given to install")

    os.system(PYTHON + " -m" + PIP + " install" + module_name)


def convert_decimal_degrees(degree, minutes, seconds, direction):
    """
    We use DRY principles and create a seperate function for this

    Args:
        degree (int | float): Degree
        minutes (int | float): Minutes
        seconds (int | float): Seconds
        direction (str): Direction

    Returns:
        int: Decimal Degrees
    """
    decimal_degrees = degree + minutes / 60 + seconds / 3600

    if direction == "S" or direction == "W":
        decimal_degrees *= -1

    return decimal_degrees


def create_google_maps_url(gps_coords):
    """
    Exif data stores coordinates in degree/minutes/seconds format. 
    To convert to decimal degrees.
        1. We extract the data from the dictionary we sent to this function for latitudinal data.
        2. We extract the data from the dictionary we sent to this function for longitudinal data.

    Args:
        gps_coords (dict)

    Returns:
        str: a Google Maps link
    """
    dec_deg_lat = convert_decimal_degrees(
        float(gps_coords["lat"][0]),
        float(gps_coords["lat"][1]),
        float(gps_coords["lat"][2]),
        gps_coords["lat_ref"])

    dec_deg_lon = convert_decimal_degrees(
        float(gps_coords["lon"][0]),
        float(gps_coords["lon"][1]),
        float(gps_coords["lon"][2]),
        gps_coords["lon_ref"])

    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"
