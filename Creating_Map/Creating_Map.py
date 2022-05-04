#Creating map branch of my marine mammals stranding project
#importing the files i will use

import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from cartopy.feature import ShapelyFeature
import rasterio as rst
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.geometry import MultiPoint

#load the data
outline = gpd.read_file('Data_Files/Scotland_boundary/Scotland boundary.shp') #outline of Scotland
strandings = pd.read_csv('Data_Files/Strandings_SMASS _data1992_2021_utf8.txt') #importing strandings for conversion
soiltype = gpd.read_file('Data_Files/Hutton_Soils250K_v1_4/Hutton_Soils_250K_v1.4/qmsoils_UCSS_v1_3.shp')
soiltype

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
myFig = plt.figure(figsize=(15, 15))  # create a figure of size 15x15 (representing the page size in inches)
myCRS = ccrs.UTM(30)  # create a reference system to transform our data.
ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.

# first, we just add the outline of Scotland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature) # add the features we've created to the map.

#adding strandings
strandings_plot = ax.plot(marinestrandings.geometry.x, marinestrandings.geometry.y, transform=myCRS, color='coral',
                          marker = 'o', markersize = 1, linestyle = '')

#adding soil type map

# get the number of unique municipalities we have in the dataset
num_soils = len(soiltype.MSG84_1.unique())
print('Number of unique features: {}'.format(num_soils)) #
soil_colours = ["gold", "darkgreen", "red", "slateblue", "orchid", "moccasin", "brown", "steelblue", "violet",
                "mediumseagreen", "orangered", "pink", "honeydew", "aqua"] #selecting colours for soil types
# get a list of unique names for the soil types
soiltype_update = soiltype[soiltype.MSG84_1.notnull()] # remove null values from dataset

soil_names = list(soiltype_update.MSG84_1.unique())



# next, add the soil types to the map using the colors picked.
# here, we're iterating over the unique values in the 'MSG84_1' field.
# we're also setting the edge color to be black, with a line width of 0.5 pt.
# Feel free to experiment with different colors and line widths.
for i, name in enumerate(soil_names):
    feat = ShapelyFeature(soiltype['geometry'][soiltype['MSG84_1'] == name], myCRS,
                          edgecolor='k',
                          facecolor=soil_colours[i],
                          linewidth=1,
                          alpha=0.25)
    ax.add_feature(feat)

myFig # to show the updated figure


#soiltype_plot = ax.plot(soiltype['geometry'], myCRS, edgecolor='mediumblue', facecolor='mediumblue')
#ax.add_feature(soiltype_plot)
print(soiltype)



# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # because total_bounds gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

myFig.savefig('map.png', bbox_inches='tight', dpi=300)
plt.show()
