from datetime import datetime
from datetime import timedelta
from process_pools_from_laguardia import main_from
from process_pools_to_laguardia import main_to
import json


def get_date(date_string):
    try:
        date = datetime.strptime(date_string, '%m/%d/%Y')
    except ValueError:
        date = datetime.strptime(date_string, '%Y-%m-%d')
    return date


def get_time(time_string):
    try:
        time = datetime.strptime(time_string, '%H:%M')
    except ValueError:
        time = datetime.strptime(time_string, '%H:%M:%S')
    return time


def initialize_pool_10_min(trips, direction):
    pool_10_min = {}
    pool_10_ongoing = False
    pool_10_index = 0
    pickup_coord_10 = []
    destination_coord_10 = []
    distance_10 = []
    i = 0
    start_date = None

    while i < len(trips["vendorid"]):
        if start_date is None:
            start_date = get_date(trips["tpep_pickup_datetime"][i].split()[0])
        else:
            current_date = get_date(trips["tpep_pickup_datetime"][i].split()[0])
            if current_date > start_date:
                start_date = get_date(trips["tpep_pickup_datetime"][i].split()[0])
                pool_10_ongoing = False

        if not pool_10_ongoing:
            pool_10_ongoing = True
            pool_10_index += 1
            pool_10_min[pool_10_index] = {}
            pickup_coord_10 = [(trips["pickup_longitude"][i], trips["pickup_latitude"][i])]
            destination_coord_10 = [(trips["dropoff_longitude"][i], trips["dropoff_latitude"][i])]
            distance_10 = [trips["trip_distance"][i]]
            start_10_min = trips["tpep_pickup_datetime"][i].split()[1]

        else:

            current_time = trips["tpep_pickup_datetime"][i].split()[1]
            if get_time(current_time) > (get_time(start_10_min) + timedelta(
                    minutes=10)):
                pool_10_ongoing = False
                pool_10_min[pool_10_index]["pickup"] = pickup_coord_10
                pool_10_min[pool_10_index]["destination"] = destination_coord_10
                pool_10_min[pool_10_index]["distance"] = distance_10

                # Call main_from or main_to from here
                if direction == "to":
                    # If you are just starting to process a month from the 1st day, then change the condition to ' >= 0 '
                    if pool_10_index >= 0: # If program stopped for some reason, change this number to be the next pool after the last pool number processed

                        pool_info = main_to(pool_10_min, pool_10_index)

                        global_pool_info[pool_10_index] = pool_info[pool_10_index]

                        # Create the month's folder inside the folder 5min_pools_info (or whatever folder name you are using)
                        # and save the file inside that folder
                        with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\10min_pools_info\\January\\pool_10min_to_laguardia.json", "w") as fp:
                            json.dump(global_pool_info, fp)
                else:
                    # If you are just starting to process a month from the 1st day, then change the condition to ' >= 0 '
                    if pool_10_index >= 0: # If program stopped for some reason, change this number to be the next pool after the last pool number processed
                        pool_info = main_from(pool_10_min, pool_10_index)
                        global_pool_info[pool_10_index] = pool_info[pool_10_index]

                        # Create the month's folder inside the folder 5min_pools_info (or whatever folder name you are using)
                        # and save the file inside that folder
                        with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\10min_pools_info\\January\\pool_10min_from_laguardia_optimized.json", "w") as fp:
                            json.dump(global_pool_info, fp)
                continue

            else:
                pickup_coord_10.append((trips["pickup_longitude"][i], trips["pickup_latitude"][i]))
                destination_coord_10.append((trips["dropoff_longitude"][i], trips["dropoff_latitude"][i]))
                distance_10.append(trips["trip_distance"][i])
        i += 1

        if pool_10_ongoing:
            pool_10_min[pool_10_index]["pickup"] = pickup_coord_10
            pool_10_min[pool_10_index]["destination"] = destination_coord_10
            pool_10_min[pool_10_index]["distance"] = distance_10


global_pool_info = {}
