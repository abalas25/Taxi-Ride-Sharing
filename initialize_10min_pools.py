from datetime import datetime
from datetime import timedelta
from process_pools_from_laguardia import main_from
from process_pools_to_laguardia import main_to
import json


def initialize_pool_10_min(trips, direction):
    pool_10_min = {}
    pool_10_ongoing = False
    pool_10_index = 0
    pickup_coord_10 = []
    destination_coord_10 = []
    distance_10 = []
    i = 0

    while i < len(trips["vendorid"]):
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
            if datetime.strptime(current_time, "%H:%M") > datetime.strptime(start_10_min, "%H:%M") + timedelta(
                    minutes=10):
                pool_10_ongoing = False
                pool_10_min[pool_10_index]["pickup"] = pickup_coord_10
                pool_10_min[pool_10_index]["destination"] = destination_coord_10
                pool_10_min[pool_10_index]["distance"] = distance_10

                # Call max_from or max_to from here
                if direction == "to":
                    pool_info = main_to(pool_10_min, pool_10_index)

                    global_pool_info[pool_10_index] = pool_info[pool_10_index]
                    with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\10min_pools_info\\January\\pool_10min_to_laguardia.json", "w") as fp:
                        json.dump(global_pool_info, fp)
                else:
                    pool_info = main_from(pool_10_min, pool_10_index)
                    global_pool_info[pool_10_index] = pool_info[pool_10_index]

                    with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\10min_pools_info\\January\\pool_10min_from_laguardia.json", "w") as fp:
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
