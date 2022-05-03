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
#background = rst.open('Data_Files/Over_gb/GBOverview.tif') #background Ordnance Survey map
#scot data
strandings = pd.read_csv('Data_Files/Strandings_SMASS _data1992_2021_utf8.txt') #importing strandings for conversion

#adding fishing vessels

with rst.open('Data_Files/National Maps/National Maps/Rasters/ScotMap_Central_numberVessel_aggr_3_190713/ScotMap_Central_numberVessel_aggr_3_190713.tif')\
        as dataset:
    xmin, ymin, xmax, ymax = dataset.bounds
    crs = dataset.crs
    landcover = dataset.read(1)
    affine_tfm = dataset.transform

print('{} opened in {} mode'.format(dataset.name,dataset.mode))
print('image has {} band(s)'.format(dataset.count))
print('image size (width, height): {} x {}'.format(dataset.width, dataset.height))
print('band 1 dataype is {}'.format(dataset.dtypes[0])) # note that the band name (Band 1) differs from the list index [0]
#fishingvessels = fishingvessels.to_crs("EPSG:27700")
#print(fishingvessels.crs)
#mappedvessels = fishingvessels.read()

#adding fishing restrictions
#no_fishing = gpd.read_file('Data_Files/area_management_fishing_restrictions/area_management_fishing_restrictionsPolygon.shp')
#no_fishing = no_fishing.to_crs("EPSG:27700")

#convert mammal strandings database into points shapefile
strandings['geometry'] = list(zip(strandings['LongWGS84'], strandings['LatWGS84']))
strandings['geometry'] = strandings['geometry'].apply(Point)
strandingsgdf: GeoDataFrame = gpd.GeoDataFrame(strandings)
strandingsgdf.set_geometry('geometry')
strandingsgdf.set_crs("EPSG:4326", inplace=True) #sets the coordinate reference system to epsg:3857 WGS84 lat/lon
strandingsgdf.to_file('marinestrandings.shp')


#load the new strandings shapefile
marinestrandings = gpd.read_file('marinestrandings.shp')
marinestrandings = marinestrandings.to_crs("EPSG:27700")

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
#counties_feat = ShapelyFeature(counties['geometry'], myCRS, edgecolor='mediumblue', facecolor='mediumblue', linewidth=1)
#ax.add_feature(counties_feat)

#Adding no fishing zones
no_fishing_feature = ShapelyFeature(no_fishing['geometry'], myCRS, edgecolor='mediumblue', facecolor='mediumblue', linewidth=2)
ax.add_feature(no_fishing_feature)

#adding strandings
strandings_plot = ax.plot(marinestrandings.geometry.x, marinestrandings.geometry.y, transform=myCRS, color='coral',
                          marker = 'o', markersize = 1, linestyle = '')

#adding fishing vessel info
#ax.imshow(mappedvessels, transform=myCRS, extent=[xmin, xmax, ymin, ymax])

print(marinestrandings.crs)




# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS) # because total_bounds gives output as xmin, ymin, xmax, ymax,
# but set_extent takes xmin, xmax, ymin, ymax, we re-order the coordinates here.

myFig.savefig('map.png', bbox_inches='tight', dpi=300)
plt.show()
