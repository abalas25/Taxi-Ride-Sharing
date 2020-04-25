from datetime import datetime
from datetime import timedelta
from process_pools_from_laguardia import main_from
from process_pools_to_laguardia import main_to


def initialize_pool_5_min(trips, direction):
    pools = {}
    pool_5_ongoing = False
    pool_5_index = 0
    pickup_coord_5 = []
    destination_coord_5 = []
    distance_5 = []
    i = 0

    while i < len(trips["VendorID"]):

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
                    main_to(pools, pool_5_index)
                else:
                    main_from(pools, pool_5_index)

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