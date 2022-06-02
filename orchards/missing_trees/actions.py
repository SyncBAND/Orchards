import plotly.express as px
import plotly.graph_objects as go
import requests, json

from math import floor

from shapely.geometry import Point

from utils.helper import add_distance, get_value, is_inside_polygon
from missing_trees.conditions import verify_if_point_exists


def draw(orchard_id, trees, lat_trees, lon_trees):
    '''
    Draws and plots points on basic map for visual representation

    Parameters:
      - list: list of tree ids - trees
      - list: list of latitude values - lat_trees
      - list: list of longitude values - lon_trees

    Returns:
      none
    '''
    
    try:

        URL = f'{get_value("BASE_ENDPOINT")}orchards/{orchard_id}'
        API_TOKEN = get_value("API_TOKEN")

        headers = {'Content-Type':'application/json', 'Authorization': f'{API_TOKEN}'}
        response = requests.get(URL, timeout=5, headers=headers)

        data = json.loads(response.content)

        lon_polygon = []
        lat_polygon = []

        polygon = data['polygon'].split(' ')
        lis = []

        for points in polygon:
            lon_polygon.append(float(points.split(',')[0]))
            lat_polygon.append(float(points.split(',')[1]))

            lis.append((float(points.split(',')[0]), float(points.split(',')[1])))

        figure_line = px.line_geo(lon=lon_polygon, lat=lat_polygon)
        figure_scatter = px.scatter_geo(lat=lat_trees,lon=lon_trees, hover_name=trees)

        figure = go.Figure(data=figure_scatter.data + figure_line.data)
        figure.update_layout(title = 'World map', title_x=0.5)
        figure.show()

    except Exception as e:
        # fail silently
        print(e)


def find_missing_trees(trees_dictionary, trees_polygon, dataframe):
    '''
    Finds potentially missing trees

    Parameters:
      - trees_dictionary: dict - dictionary of points
      - trees_polygon: list - list of tuples with points, i.e (lon, lat)
      - dataframe: Dataframe - pandas

    Returns:
      list: potentially missing trees - [{'lat': lat1, 'lng': lat22}]
    '''
    missing = {}
    
    try:
      trees_dictionary = json.loads(trees_dictionary)
    except:
      pass
    
    # assume equal space between each tree by using shortest distance positioned at index 0 | make this value the mean
    mean = floor(dataframe['nearest_distances'][0][0] * 1000)/1000.0

    # iterate through all trees using nearest distance list
    for idx_nearest, nearest_distance in enumerate(dataframe['nearest_distances']):
        
        # iterate through list of nearest_distances around a tree/parent
        for idx_distance, distance in enumerate(nearest_distance):

            # ignore parent
            if idx_distance != 0:

                # based on the assumption that each tree is equally spaced,
                # track potentially missing trees between parent and
                # trees 2 times the distance away or more from parent
                missing_points = round(distance, 3)//mean
                
                # if the space between is greater than the mean
                if missing_points > 1:

                    # check to see if tree does not already exist at all the missings points before tracking the coordinate
                    for missing_point in range(1, int(missing_points)):

                        # add (mean * space between missing_point) to the left of parent
                        lat_left_direction, lon_left_direction = add_distance(direction=2, dist_in_km=mean*missing_point, lat=dataframe['lat'][idx_nearest], lon=dataframe['lon'][idx_nearest])
                        
                        left_direction_point = Point(lon_left_direction, lat_left_direction)

                        # check if the retuned point is within the bounds before continuing 
                        if is_inside_polygon(trees_polygon, left_direction_point) or left_direction_point.distance(trees_polygon) <= 0.00002:

                            # check if point is potentially missing on the left of parent
                            if not verify_if_point_exists(trees_dictionary, dataframe['id'][idx_nearest], [lat_left_direction, lon_left_direction], dataframe['nearest_neighbours'][idx_nearest]) :

                                missing['{},{}'.format(round(lat_left_direction, 5), round(lon_left_direction, 5))] = {'lat': lat_left_direction, 'lng':lon_left_direction}

                        # add (mean * space between missing_point) to the right of tree at hand
                        lat_right_direction, lon_right_direction = add_distance(direction=4, dist_in_km=mean*missing_point, lat=dataframe['lat'][idx_nearest], lon=dataframe['lon'][idx_nearest])
                        
                        right_direction_point = Point(lon_right_direction, lat_right_direction)

                        # check if the retuned point is within the bounds before continuing 
                        if is_inside_polygon(trees_polygon, right_direction_point) or right_direction_point.distance(trees_polygon) <= 0.00002:

                            # check if point is potentially missing on the right of parent
                            if not verify_if_point_exists(trees_dictionary, dataframe['id'][idx_nearest], [lat_right_direction, lon_right_direction], dataframe['nearest_neighbours'][idx_nearest]):

                                missing['{},{}'.format(round(lat_right_direction, 5), round(lon_right_direction, 5))] = {'lat': lat_right_direction, 'lng': lon_right_direction}
                    
    
    return list(missing.values())