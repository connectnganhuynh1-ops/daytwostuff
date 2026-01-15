# %% 
import pandas as pd
import numpy as np  
from sodapy import Socrata 
import folium
from folium import plugins
# %%
# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cityofnewyork.us", None)

# Example authenticated client (needed for non-public datasets):
#client = Socrata(data.cityofnewyork.us,
#                  "insert key",
#                 username="brianwright@virginia.edu",
#                 password= "RoseRivers@301")

# %%
# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("vfnx-vebw", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

#%%
# Convert x and y columns to numeric
results_df['x'] = pd.to_numeric(results_df['x'], errors='coerce')
results_df['y'] = pd.to_numeric(results_df['y'], errors='coerce')

# Create a map visualization with Leaflet (folium)

#%%
# Extract latitude and longitude columns and remove null values
map_data = results_df[['x', 'y', 'unique_squirrel_id']].dropna()

# Create a folium map centered on NYC
m = folium.Map(
    location=[40.7580, -73.9855],
    zoom_start=11,
    tiles='OpenStreetMap'
)

#%%
# Add markers for each squirrel sighting
for idx, row in map_data.iterrows():
    folium.Marker(
        location=[row['y'], row['x']],
        popup=f"Squirrel ID: {row['unique_squirrel_id']}",
        tooltip=row['unique_squirrel_id']
    ).add_to(m)

#%%    

# Display the map
m.save('squirrel_map.html')
m
# %%
results_df.info()
# %%

