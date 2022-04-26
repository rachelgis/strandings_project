#Creating map branch of my marine mammals stranding project
#importing the files i will use

import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import rasterio as rst
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.geometry import MultiPoint

#load the data
outline = gpd.read_file('Data_Files/Scotland_boundary/Scotland boundary.shp') #outline of Scotland
background = rst.open('Data_Files/Over_gb/GBOverview.tif') #background Ordnance Survey map
counties = gpd.read_file('Data_Files/Localities2020boundaries/Localities2020boundaries/Localities2020_MHW.shp') #gov
#scot data
strandings = pd.read_csv('Data_Files/Strandings_SMASS _data1992_2021_utf8.txt') #importing strandings for conversion

#convert mammal strandings database into points shapefile
strandings['geometry'] = list(zip(strandings['LongOSGB36'], strandings['LatOSGB36']))
strandings['geometry'] = strandings['geometry'].apply(Point)
strandingsgdf: GeoDataFrame = gpd.GeoDataFrame(strandings)
strandingsgdf.set_geometry('geometry')
strandingsgdf.set_crs("EPSG:4277", inplace=True) #sets the coordinate reference system to epsg:3857 WGS84 lat/lon
strandingsgdf.to_file('marinestrandings.shp')


#load the new strandings shapefile
marinestrandings = gpd.read_file('marinestrandings.shp')
marinestrandings.to_crs("OSGB 1936 / British National Grid")

#creating the map
myFig = plt.figure(figsize=(10, 10))  # create a figure of size 15x15 (representing the page size in inches)
myCRS = ccrs.UTM(30)  # create a reference system to transform our data.
ax = plt.axes(projection=ccrs.Mercator())  # finally, create an axes object in the figure, using a Mercator
# projection, where we can actually plot our data.

# first, we just add the outline of Scotland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature) # add the features we've created to the map.

#adding counties
counties_feat = ShapelyFeature(counties['geometry'], myCRS, edgecolor='mediumblue', facecolor='mediumblue', linewidth=1)
ax.add_feature(counties_feat)

#adding strandings
#strandings_feat = ShapelyFeature(marinestrandings['geometry'], myCRS, edgecolor='coral', facecolor='coral', linewidth=3)
#ax.add_feature(strandings_feat)
plt.scatter()



# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # because total_bounds gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

myFig.savefig('map.png', bbox_inches='tight', dpi=300)
plt.show()
