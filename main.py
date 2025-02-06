import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from sklearn.datasets import fetch_california_housing
import folium
from folium import plugins

#- 1- visualisation price as color
#- 2- visualisation size of the bubble

data = fetch_california_housing(as_frame=True)

#exeplier map
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=6)

#make cheaper houses with green color and expensive house with red color

price_min, price_max = data['MedHouseVal'].min(), data['MedHouseVal'].max()
size_min, size_max = data['AveRooms'].min(), data['AveRooms'].max()

for _, row in data.iterrows():
    normalized_prise = (row['MedHouseVal'] - price_min)/(price_max-price_min)
    # color come from green to red
    color = plt.cm.RdYlGn(1-normalized_prise)

    normalized_rooms = (row['AveRooms'] - size_min)/(size_max-size_min)
    popup_info = f'''Median House Value: ${row['MedHouseVal']:.2f}<br>
    Average Rooms: {row['AveRooms']}<br>
    Population: {row['Population']}<br>
    Median Income: ${row['MedInc']:.2f}'''

    folium.CircleMarker(
        location = [row['Latitude'], row ['Longitude']],
        radius=5+20
    )