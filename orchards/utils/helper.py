from itertools import count, takewhile
from math import sin, cos, pi, atan2

from constance import config

import numpy as np


def set_value(key, value):
    """
    update constance settings
    :param key
    :param value
    :return: None
    """
    setattr(config, key, value)


def get_value(key):
    """
    get constance settings
    :param key
    :return: value
    """
    return getattr(config, key)


def is_inside_polygon(polygon, point):
    '''
    Checks whether a geometric point is bounded by a polygon

    Parameters:
      - polygon: Polygon - geometric feature. imported from shapely library
      - point: Point - geometric feature. imported from shapely library

    Returns:
      bool: Either true if found else false
    '''
    try:
        return point.within(polygon)
    except:
        return False


def all_range(start=0, stop=None, step=1, round_by=0):
    '''
    Creates a sequence of integers/decimals from start (inclusive) to stop (exclusive) by step. range(i, j) 
    
    produces i, i+1, i+2, ..., j-1. start defaults to 0, and stop is omitted! 
    
    all_range(4) produces 0, 1, 2, 3. These are exactly the valid indices for a list of 4 elements. When step is given, it specifies the increment (or decrement)

    Parameters:
      - start: int or float - indicates the beginning value
      - stop:  int or float - indicates where the list should end. 
                note - this value will not be returned in the list.
      - step: int or float - indicates the beginning value
      - round_by: int or float - indicates rounded val

    Returns:
      list: sequence of integers/floats
    '''
    if step == 0:
        raise ValueError("Step cannot be NULL")

    if stop is None:
        start, stop = 0, start

    return list(takewhile(lambda x: x < stop, (round(start + i * step, round_by) for i in count())))


def get_direction(lat1: float, lon1: float, lat2: float, lon2: float):
    '''
    Calculates the azimuth/bearing/direction between two points.
    Latitude and longitude values must be in decimal degrees

    Parameters:
      - lat1: int or float - latitude for the first point
      - lon1: int or float - longitude for the first point
      - lat2: int or float - latitude for the second point
      - lon2: int or float - longitude for the second point

    Returns:
      float: the bearing value in degrees 
    '''
    lat1 = np.deg2rad(lat1)
    lat2 = np.deg2rad(lat2)
    dLon = lon2 - lon1
    # dLon = np.deg2rad(lon2) - np.deg2rad(lon1)
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)
    bearing = np.rad2deg(atan2(y, x))

    return (bearing + 360) % 360


def add_distance(direction: int, dist_in_km: float, lat: float, lon: float):
    '''
    Adds the azimuth/bearing/direction in kilometers to a coordinate point.
    Latitude and longitude values must be in decimal degrees

    toRadians(45 * (2 * n - 1)); | where n = [1, 2, 3, 4] 
    
    Note: 1->North, 2->East, 3->South, 4->West

    Parameters:
      - direction: int between 1 and 4 (inclusive)
      - dist_in_km: int or float - distance in kilometers
      - lat1: int or float - latitude for the first point
      - lon1: int or float - longitude for the first point

    Returns:
      float: new latitude - new_lat
      float: new longitude - new_lat
    '''

    if direction <= 0 or direction > 4:
        raise ValueError("Direction value needs to be either 1, 2, 3 or 4. 1->North, 2->East, 3->South, 4->West")

    #  The correct calculation would be 
    a = np.deg2rad(45 * (2 * direction - 1));  # degrees

    r_earth = 6371 # in km

    lat0 = cos(pi / 180.0 * lat)

    new_lat = lat + (180/pi) * (dist_in_km / r_earth) * sin(a)
    new_lon = lon + (180/pi) * (dist_in_km / r_earth) / cos(lat0) * cos(a)
    
    return new_lat, new_lon


def binary_search(item_to_search, search_list: list):
    '''
    Search through a list for a value recurively

    Parameters:
      - item_to_search: item to search
      - search_list: sorted list which will be traversed

    Returns:
      bool: true if item is found else false
    '''
    max_length = len(search_list) - 1
    mid = max_length//2
    
    if max_length+1 == 0:
        return False
    elif item_to_search == search_list[mid]:
        return True
    else:
        if item_to_search > search_list[mid]:
            return binary_search(item_to_search, search_list[mid+1:max_length+1])
        else:
            return binary_search(item_to_search, search_list[0:mid])
