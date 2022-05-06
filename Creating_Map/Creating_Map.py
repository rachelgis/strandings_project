#Creating map branch of my marine mammals stranding project
#importing the files i will use

import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches
import rasterio as rst
from rasterio.crs import CRS
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import rioxarray
from shapely.geometry import MultiPoint

#load the data
outline = gpd.read_file('Data_Files/Scotland_boundary/Scotland boundary.shp') #outline of Scotland
strandings = pd.read_csv('Data_Files/Strandings_SMASS _data1992_2021_utf8.txt') #importing strandings for conversion
beach_substrate = gpd.read_file('Data_Files/Intertidal+Substrate+Foreshore+(England+and+Scotland)'
                                '/Intertidal Substrate Foreshore (England and Scotland)/DEFR00000009.shp')
waterways = gpd.read_file('Data_Files/DS_10283_2387/OSM_Scotland_OSGB/waterways.shp')
settlements = gpd.read_file('Data_Files/Settlements2020centroids/Settlements2020centroids/Settlements2020_Centroids.shp')
counties = gpd.read_file('Data_Files/bdline_essh_gb/Data/GB/counties.shp')

#convert mammal strandings database into points shapefile
strandings['geometry'] = list(zip(strandings['LongWGS84'], strandings['LatWGS84']))
strandings['geometry'] = strandings['geometry'].apply(Point)
strandingsgdf: GeoDataFrame = gpd.GeoDataFrame(strandings)
strandingsgdf.set_geometry('geometry')
strandingsgdf.set_crs("EPSG:4326", inplace=True) #sets the coordinate reference system to epsg:3857 WGS84 lat/lon
strandingsgdf.to_file('marinestrandings.shp')

#load the new strandings shapefile
marinestrandings = gpd.read_file('marinestrandings.shp')
marinestrandings = marinestrandings.to_crs("EPSG:27700") #converting the CRS

#creating the map
myFig = plt.figure(figsize=(10, 10))  # create a figure of size 15x15 (representing the page size in inches)
myCRS = ccrs.UTM(30)  # create a reference system to transform our data.
ax = plt.axes(projection=ccrs.Mercator())   #create an axes object in the figure, using a Mercator projection

#add the outline of Scotland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='palegoldenrod', facecolor='palegoldenrod')
ax.add_feature(outline_feature)
outline = outline.to_crs("EPSG:27700")
xmin, ymin, xmax, ymax = outline.total_bounds

#adding settlements
settlements_plot = ax.plot(settlements.geometry.x, settlements.geometry.y, transform=myCRS, color='lightslategray',
                           marker='o', markersize = 1.1, linestyle = '' )

#adding counties
counties_feature = ShapelyFeature(counties['geometry'], myCRS, edgecolor='black', facecolor='lightcyan', linewidth=0.5)
ax.add_feature(counties_feature)

#adding waterways
waterways_feat = ShapelyFeature(waterways['geometry'], myCRS, edgecolor='dodgerblue', linewidth=0.2)
ax.add_feature(waterways_feat)

#adding beach substrate map

# get the number of unique soil types in the dataset
num_substrate = len(beach_substrate.FORE_DESC.unique())
print('Number of unique features: {}'.format(num_substrate)) #
substrate_colours = ["gold", "coral", "bisque", "tan", "lightyellow", "moccasin", "sandybrown", "navajowhite", "orange",
                "blanchedalmond", "orangered", "peachpuff", "darksalmon"] #selecting colours for substrate types
# get a list of unique names for the substrate types
substrate_names = list(beach_substrate.FORE_DESC.unique())

# next, add the substrate types to the map using the colors picked.
for i, name in enumerate(substrate_names):
    feat = ShapelyFeature(beach_substrate['geometry'][beach_substrate['FORE_DESC'] == name], myCRS,
                          edgecolor=substrate_colours[i],
                          facecolor=substrate_colours[i],
                          linewidth=4,
                          alpha=0.25)
    ax.add_feature(feat)

#adding strandings
num_mammal = len(marinestrandings.Class.unique()) # getting number of mammal types
print('Number of unique mammals: {}'.format(num_mammal))
mammal_colours = (["salmon", "cornflowerblue", "coral", "thistle", "forestgreen", "mediumslateblue", "darkturquoise",
                  "palegoldenrod", "violet", "olive", "seagreen", "indianred", "plum", "darkgrey", "c", "lemonchiffon"])
#mammal_colours = (["xkcd:sky blue", "xkcd:grey", "xkcd:sky blue", "xkcd:grey", "xkcd:sky blue", "xkcd:grey",
#                   "xkcd:sky blue", "xkcd:grey", "xkcd:sky blue", "xkcd:grey", "xkcd:sky blue", "xkcd:grey",
#                   "xkcd:sky blue", "xkcd:grey", "xkcd:sky blue", "xkcd:grey"])

mammal_names = list(marinestrandings.SubClass.unique()) #creating list of mammal names
print(mammal_names)

for i, name in enumerate(mammal_names, start=0):
    strandings_plot = ax.plot(marinestrandings.geometry.x, marinestrandings.geometry.y,
                              [marinestrandings['SubClass'] == name],
                              transform=myCRS, c=mammal_colours[i],
                              marker = 'o', markersize = 1.5, linestyle = '')


ax.stock_img #adding background to map

#mammal_colours = {"Grey seal":"salmon", "Harbour seal":"cornflowerblue", "Pelagic delphinid":"coral",
#                  "Marine turtle":"thistle", "Harbour porpoise":"forestgreen", "Cetacean (indeterminate species)":"mediumslateblue",
#                  "Mysticete":"darkturquoise", "Pinniped (indeterminate species)":"palegoldenrod", "Bottlenose dolphin":"violet",
#                  "Sperm/beaked whale":"olive", "Shark":"seagreen", "Pinniped (Other)":"indianred", "Kogia sp.":"plum",
#                  "Pelagic Delphinid":"darkgrey", "Marine Turtle":"c", "Basking shark":"lemonchiffon"}
#strandings_plot = ax.plot(marinestrandings.geometry.x, marinestrandings.geometry.y, transform=myCRS,
#                          color=marinestrandings['SubClass'].map(mammal_colours), marker='o', markersize=2,
#                          linestyle = '')

#Create map legend
# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

mammalnames = [name.title() for name in mammal_names]

mammal_handles = generate_handles(marinestrandings.SubClass.unique(), mammal_colours, alpha=0.25)
water_handle = generate_handles(['Waterways'], ['dodgerblue'])

handles = mammal_handles + water_handle
labels = mammalnames + ['Waterways']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=7.5,
                 fontsize=6, loc='upper left', frameon=True, framealpha=1)


# using the boundary of the shapefile features (Scotnad outline), zoom the map to Scotland
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

myFig.savefig('map.png', bbox_inches='tight', dpi=300)
plt.show()



