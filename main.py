import pandas as pd
import initialize_5min_pools
import initialize_10min_pools

# Set direction to either from / to.
# Open the correct trips csv file
direction = "to"
trips = pd.read_csv("../Yellow Tripdata 2016 (Till May)/trips_{}_laguardia_jan_2016.csv".format(direction))

# Call either initialize_5min_pools() or initialize_10min_pools()

# initialize_5min_pools.initialize_pool_5_min(trips, direction)
# initialize_10min_pools.initialize_pool_10_min(trips, direction)
