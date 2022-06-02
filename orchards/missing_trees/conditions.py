from utils.helper import all_range, binary_search, get_direction


def verify_if_point_exists(trees_dictionary: dict, parent_id: int, point: list, nearest_neighbours: list):
    '''
    Verifies whether point exists within a list of neighbours before declaring it as missing. 
    
    Because we are working with latitude and longitude values, 
    a special case is used with an offset tolerance of 5 decimal places, i.e 0.00005
    - rounds off the value to 5 decimal places
    - creates a latitude list ranging between (lat-0.00005, lat+0.00005) 
    - creates a longitude list ranging between (lon-0.00005, lon+0.00005) 
    - search for lat and lon through created ranges

    Parameters:
      - trees_dictionary: dict - dictionary of points
      - parent_id: int - id of the original point (parent)
      - point: list - potentially missing (lat, lon)
      - search_list: list of neighbour ids belonging to the original point

    Returns:
      bool: true if point is found else false meaning its missing
    '''

    parent_id = str(parent_id)
    
    assume_left_and_right_exists_count = 0
    result = True

    for neighbour in nearest_neighbours:

        neighbour = str(neighbour)

        # Because we are assuming the points are in a grid, 
        # check if neighbour is to the left or right of parent
        direction = get_direction(
            trees_dictionary[parent_id]['lat'], trees_dictionary[parent_id]['lng'],
            trees_dictionary[neighbour]['lat'], trees_dictionary[neighbour]['lng']
        )
        
        # Special case - to left of parent point - direction == 270
        # Special case - to right of parent point - direction == 90
        
        if (direction//1 == 270) or (direction//1 == 90):

            assume_left_and_right_exists_count += 1

            # add/subtract tolerance value to neighbour latitude value to get min and max 
            lat_min_range = round(trees_dictionary[neighbour]['lat'], 5) - 0.00005
            lat_max_range = round(trees_dictionary[neighbour]['lat'], 5) + 0.00005

            # create neighbour latitude range list
            # this range helps check for trees that are not equally spaced
            lat_list = all_range(start=lat_min_range, stop=lat_max_range+0.00001, step=0.00001, round_by=5)

            # search for potentially missing latitude in range list
            approx_lat = binary_search(round(point[0], 5) , lat_list)

            if approx_lat:
                # add/subtract toletance value to neighbour longitude to get min and max 
                lon_min_range = round(trees_dictionary[neighbour]['lng'], 5) - 0.00005
                lon_max_range = round(trees_dictionary[neighbour]['lng'], 5) + 0.00005

                # create neighbour longitude range list
                # this range helps check for trees that are not equally spaced
                lon_list = all_range(start=lon_min_range, stop=lon_max_range+0.00001, step=0.00001, round_by=5)

                # search for potentially missing longitude in range list
                approx_lng = binary_search(round(point[1], 5), lon_list)

                if approx_lng: 
                    # point already exists == not missing
                    return True

            # point does not exist == (potentially) missing
            result = False
    
    if assume_left_and_right_exists_count > 1 and assume_left_and_right_exists_count < 2:
        result = False

    return result
