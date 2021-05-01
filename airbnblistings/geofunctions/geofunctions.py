import math
from typing import Tuple


def offset(lat: float, lon: float, offset: int) -> Tuple[float, float]:
    """ Offsets both lat and long by the same distance in feet """
    original_lat = lat
    original_long = lon
    earth_radius_feet = 20925721.784777
    offset = offset
    radians_to_degrees = 180 / math.pi
    degrees_to_radians = math.pi / 180
    new_lat = original_lat + (offset / earth_radius_feet) * (radians_to_degrees)
    new_long = original_long + (offset / earth_radius_feet) * (
        radians_to_degrees
    ) / math.cos(original_lat * degrees_to_radians)
    return new_lat, new_long
