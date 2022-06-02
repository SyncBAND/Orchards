

import pandas as pd
import numpy as np
import requests, json

from django.core.exceptions import ValidationError
from collections import defaultdict

from shapely.geometry import Polygon

from sklearn.neighbors import BallTree

from missing_trees.actions import draw
from utils.helper import get_value


def initialise_data(data):
    '''
    Initialise data

    Parameters:
      - data: json data with coordinate information

    Returns:
      list: list of tree ids - trees
      list: list of latitude values - lat_trees
      list: list of longitude values - lon_trees
      list: list of tuples latlng values (longitude, latitude) - lat_lng_trees
      dict: dictionary of points with their id as the key, i.e {id: {'lat': val1, 'lng': val2}} - trees_dictionary
    '''
    
    trees_dictionary = defaultdict(dict)

    trees = []
    lat_trees = []
    lon_trees = []
    lat_lng_trees = []

    try:
        for tree in data['results']:
            trees.append(tree['id'])
            lat_trees.append(tree['latitude'])
            lon_trees.append(tree['longitude'])
            lat_lng_trees.append((tree['longitude'], tree['latitude']))

            trees_dictionary[tree['id']].update({"lat": tree['latitude'], "lng": tree['longitude']})
        
        return json.dumps(trees_dictionary), trees, lat_trees, lon_trees, lat_lng_trees
    except Exception as e:
        raise ValidationError(e)


def setup_dataframe(orchard_id='', draw_tree=False):
    '''
    Setup dataframe using tree data. The dataframe sets 
    
    - gets nearest trees nearest_distances with their distance for each tree
    - latitude and longitude coordinates
    - creates a longitude list ranging between (lon-0.00005, lon+0.00005) 
    - search for lat and lon through created ranges

    Parameters:
      - orchard_id: int - draw tree, default=false 
      - draw_tree: bool - draw tree, default=false 

    Returns:
      dict: trees_dictionary - dictionary of points
      list: trees_polygon
      dataframe: pandas dataframe
    '''

    try:
        # call api
        URL = f'{get_value("BASE_ENDPOINT")}treesurveys/?survey__orchard_id={orchard_id}'
        API_TOKEN = get_value("API_TOKEN")

        if len(URL) == 0:
            raise ValidationError('BASE_ENDPOINT URL is empty')

        if len(API_TOKEN) == 0:
            raise ValidationError('API_TOKEN is empty')

        headers = {'Content-Type':'application/json', 'Authorization': f'{API_TOKEN}'}
        response = requests.get(URL, timeout=5, headers=headers)

        if response.status_code != 200:
            raise ValidationError(str(response.text))

        data = json.loads(response.content)

        trees_dictionary, trees, lat_trees, lon_trees, lat_lng_trees = initialise_data(data)

    except Exception as e:
        if 'Expecting value: line' in str(e):
            e = 'Probaly your API Token or BASE_ENDPOINT url is incorrect - {}'.format(e)
            
        raise ValidationError(e)
    
    trees_polygon = Polygon(lat_lng_trees)

    dataframe = pd.DataFrame()
    dataframe['lat'] = lat_trees
    dataframe['lon'] = lon_trees
    dataframe['id'] = trees

    # the formula requires rad instead of degree
    dataframe[["lat_rad", "lon_rad"]] = np.deg2rad(dataframe[["lat", "lon"]])

    ball_tree = BallTree(dataframe[["lat_rad", "lon_rad"]], metric="haversine")

    '''
    because we assuming the data is in a grid, we using 9 as a square number 
    (with optimal case of point in the middle of square)

    * * *
    * o *
    * * *

    neighbours_to_return = number of neighbours to return.
    '''
    neighbours_to_return = len(trees)
    if neighbours_to_return >= 9:
        neighbours_to_return = 9

    # returns nearest neighbours and their distances
    distances, neighbours = ball_tree.query(
        dataframe[["lat_rad", "lon_rad"]],
        k=neighbours_to_return,  # number of neighbours to return
        return_distance=True,  # choose whether you also want to return the distance
        sort_results=True,
    )

    # remove the address/point itself from the arrays because it itself is its nearest neighbour and distance
    neighbours = neighbours[:, 1:]
    distances = distances[:, 1:]

    # factor in earth_radius_in_km to distances
    earth_radius_in_km = 6371
    dataframe["nearest_distances"] = [
        d*earth_radius_in_km for d in distances
    ]

    # select the nearest addresses by position index
    dataframe["nearest_neighbours"] = [
        dataframe["id"].iloc[n].to_list() for n in neighbours
    ]

    # pd.set_option('display.max_colwidth', None)
    # print(dataframe)

    if draw_tree:
        draw(orchard_id, trees, lat_trees, lon_trees)

    return trees_dictionary, trees_polygon, dataframe