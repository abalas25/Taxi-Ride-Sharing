import pandas as pd
import initialize_10min_pools

# Open correct trips csv here and send from/to to initialize_10min_pools function
trips = pd.read_csv("../Yellow Tripdata 2016 (Till May)/trips_to_laguardia_jan_2016.csv")
initialize_10min_pools.initialize_pool_10_min(trips, "to")
