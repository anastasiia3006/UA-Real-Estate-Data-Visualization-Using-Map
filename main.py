import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pandas.core.config_init import max_cols
from sklearn.datasets import fetch_california_housing
import folium
from folium import plugins

#- 1- visualisation price as color
#- 2- visualisation size of the bubble

#load data
data = fetch_california_housing(as_frame=True).frame

#create map
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=6)

#Data preparation for normalization
price_min, price_max = data['MedHouseVal'].min(), data['MedHouseVal'].max()
size_min, size_max = data['AveRooms'].min(), data['AveRooms'].max()

#add marker to map
for _, row in data.iterrows():
    normalized_prise = (row['MedHouseVal'] - price_min)/(price_max-price_min)
    # color come from green to red
    color = plt.cm.RdYlGn(1-normalized_prise)

#normalisatoin of rooms
    normalized_rooms = (row['AveRooms'] - size_min)/(size_max-size_min)

# information in popup window
    popup_info = f'''Median House Value: ${row['MedHouseVal']:.2f}<br>
    Average Rooms: {row['AveRooms']}<br>
    Population: {row['Population']}<br>
    Median Income: ${row['MedInc']:.2f}'''


    folium.CircleMarker(
        location = [row['Latitude'], row ['Longitude']],
        radius=5+20*normalized_rooms,
        color = mcolors.to_hex(color[:3]),
        fill=True,
        fill_color = mcolors.to_hex(color[:3]),
        fill_opacity=0.7,
        popup=folium.Popup(popup_info, max_width=300)
    ).add_to(m)

# make mini-map
plugins.MiniMap().add_to(m)

#save to html
m.save('real_state.html')