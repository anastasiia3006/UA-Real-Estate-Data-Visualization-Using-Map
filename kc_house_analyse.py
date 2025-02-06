import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import folium
from folium import plugins

#- 1- visualisation price as color
#- 2- visualisation size of the bubble

#load data
data = pd.read_csv('kc_house_data.csv')

#create map
m = folium.Map(location=[data['lat'].mean(), data['long'].mean()], zoom_start=10)

#Preparation of data to normalize
price_min, price_max = data['price'].min(), data['price'].max()
size_min, size_max = data['sqft_living'].min(), data['sqft_living'].max()

#Adding markers to the map
for _, row in data.iterrows():
    normalized_prise = (row['price'] - price_min)/(price_max-price_min)
    # color come from green to red
    color = plt.cm.RdYlGn(1-normalized_prise)

#Normalization of a residential part area to determine the size of a marker
    normalized_rooms = (row['sqft_living'] - size_min)/(size_max-size_min)

#The information that will be displayed in the pop -up window
    popup_info = \
    f'''Price: ${row['price']:,}<br>
    Sqft Living: {row['sqft_living']}<br>
    Bedrooms: {row['bedrooms']}<br>
    Bathrooms: ${row['bathrooms']}'''

    folium.CircleMarker(
        location = [row['lat'], row ['long']],
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
m.save('house_sales_kc.html')