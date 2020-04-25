from datetime import datetime
from datetime import timedelta
from process_pools_from_laguardia import main_from
from process_pools_to_laguardia import main_to
import json


def initialize_pool_5_min(trips, direction):
    pools = {}
    pool_5_ongoing = False
    pool_5_index = 0
    pickup_coord_5 = []
    destination_coord_5 = []
    distance_5 = []
    i = 0

    while i < len(trips["vendorid"]):

        if not pool_5_ongoing:
            pool_5_ongoing = True
            pool_5_index += 1
            pools[pool_5_index] = {}
            pickup_coord_5 = [(trips["pickup_longitude"][i], trips["pickup_latitude"][i])]
            destination_coord_5 = [(trips["dropoff_longitude"][i], trips["dropoff_latitude"][i])]
            distance_5 = [trips["trip_distance"][i]]
            start_5_min = trips["tpep_pickup_datetime"][i].split()[1]

        else:
            current_time = trips["tpep_pickup_datetime"][i].split()[1]
            if datetime.strptime(current_time, "%H:%M") > datetime.strptime(start_5_min, "%H:%M") + timedelta(
                    minutes=5):
                print("Pool {0} obtained".format(pool_5_index))

                pool_5_ongoing = False
                pools[pool_5_index]["pickup"] = pickup_coord_5
                pools[pool_5_index]["destination"] = destination_coord_5
                pools[pool_5_index]["distance"] = distance_5

                # Call max_from or max_to from here
                if direction == "to":
                    pool_info = main_to(pools, pool_5_index)
                    global_pool_info[pool_5_index] = pool_info[pool_5_index]

                    # Create the month's folder inside the folder 5min_pools_info (or whatever folder name you are using)
                    # and save the file inside that folder
                    with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\5min_pools_info\\January\\pool_5min_to_laguardia.json", "w") as fp:
                        json.dump(global_pool_info, fp)
                else:
                    pool_info = main_from(pools, pool_5_index)
                    global_pool_info[pool_5_index] = pool_info[pool_5_index]

                    # Create the month's folder inside the folder 5min_pools_info (or whatever folder name you are using)
                    # and save the file inside that folder
                    with open("D:\\UIC\\Database Management Systems\\Taxi Ridesharing\\5min_pools_info\\January\\pool_5min_from_laguardia.json", "w") as fp:
                        json.dump(global_pool_info, fp)
                continue

            else:
                pickup_coord_5.append((trips["pickup_longitude"][i], trips["pickup_latitude"][i]))
                destination_coord_5.append((trips["dropoff_longitude"][i], trips["dropoff_latitude"][i]))
                distance_5.append(trips["trip_distance"][i])
        i += 1
        if pool_5_ongoing:
            pools[pool_5_index]["pickup"] = pickup_coord_5
            pools[pool_5_index]["destination"] = destination_coord_5
            pools[pool_5_index]["distance"] = distance_5


global_pool_info = {}
