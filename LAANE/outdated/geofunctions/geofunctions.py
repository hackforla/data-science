import math
from typing import Tuple, List


def offset(lat: float, lon: float, distance: int) -> Tuple[float, float]:
    """ Offsets both lat and long by the same distance in feet """
    original_lat = lat
    original_long = lon
    earth_radius_feet = 20925721.784777
    distance = distance
    radians_to_degrees = 180 / math.pi
    degrees_to_radians = math.pi / 180
    new_lat = original_lat + (distance / earth_radius_feet) * (radians_to_degrees)
    new_long = original_long + (distance / earth_radius_feet) * (
        radians_to_degrees
    ) / math.cos(original_lat * degrees_to_radians)
    return new_lat, new_long

def bbox(lat: float, lon: float, distance: int) -> List[offset]:
    second_distance = distance * -1
    bbox_coordinates = map(lambda x: offset(lat=lat, lon=lon, distance=x), (distance, second_distance))
    return bbox_coordinates
