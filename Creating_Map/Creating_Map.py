#Part 1 of the marine mammal stranding project plots locations of marine mammal strandings on top of beach substrate
#type on a map

#importing the files i will use
import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point

#load the data
outline = gpd.read_file('Data_Files/Scotland_boundary/Scotland boundary.shp') #outline of Scotland
strandings = pd.read_csv('Data_Files/Strandings_SMASS _data1992_2021_utf8.txt') #importing strandings for conversion
beach_substrate = gpd.read_file('Data_Files/Intertidal+Substrate+Foreshore+(England+and+Scotland)'
                                '/Intertidal Substrate Foreshore (England and Scotland)/DEFR00000009.shp')
waterways = gpd.read_file('Data_Files/DS_10283_2387/OSM_Scotland_OSGB/waterways.shp')
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
myFig = plt.figure(figsize=(10, 10))  # create a figure of size 10x10 (inches)
myCRS = ccrs.UTM(30)  # create a reference system to transform data
ax = plt.axes(facecolor='lightcyan', projection=ccrs.Mercator())   #create an axes object in the figure,
# using a Mercator projection, adding background colour to look like the sea

#add the outline of Scotland
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='palegoldenrod', facecolor='lemonchiffon')
ax.add_feature(outline_feature)
outline = outline.to_crs("EPSG:27700")
xmin, ymin, xmax, ymax = outline.total_bounds

#adding counties
counties_feature = ShapelyFeature(counties['geometry'], myCRS, edgecolor='black', facecolor='lemonchiffon', linewidth=0.5)
ax.add_feature(counties_feature)

#adding waterways
waterways_feat = ShapelyFeature(waterways['geometry'], myCRS, edgecolor='dodgerblue', linewidth=0.2)
ax.add_feature(waterways_feat)

#adding beach substrate map
# get the number of unique soil types in the dataset
num_substrate = len(beach_substrate.FORE_DESC.unique())
print('Number of unique features: {}'.format(num_substrate)) # so i know how many colours to choose
substrate_colours = ["gold", "coral", "bisque", "tan", "lightyellow", "moccasin", "sandybrown", "navajowhite", "orange",
                "blanchedalmond", "orangered", "peachpuff", "darksalmon"] #selecting colours for substrate types
# get a list of unique names for the substrate types
substrate_names = list(beach_substrate.FORE_DESC.unique())

# next, add the substrate types to the map using the colours picked.
for i, name in enumerate(substrate_names):
    feat = ShapelyFeature(beach_substrate['geometry'][beach_substrate['FORE_DESC'] == name], myCRS,
                          edgecolor=substrate_colours[i],
                          facecolor=substrate_colours[i],
                          linewidth=3, # making the lines extra wide so they show up on the map
                          alpha=0.25)
    ax.add_feature(feat)

#adding strandings
mammal_names = list(marinestrandings.SubClass.unique()) #creating list of mammal names for use in legend later
strandings_plot = ax.plot(marinestrandings.geometry.x, marinestrandings.geometry.y, transform=myCRS, c='gray',
                              marker = 'o', markersize = 1, linestyle = '')
#to do: edit the above so that different mammal types are different colours


#Create map legend
# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

mammalnames = [name.title() for name in mammal_names]
substrates = [name.title() for name in substrate_names]

substrate_handles = generate_handles(beach_substrate.FORE_DESC.unique(), substrate_colours, alpha=0.25)
mammal_handles = generate_handles(['Strandings'], ['gray'])
water_handle = generate_handles(['Waterways'], ['dodgerblue'])

handles = substrate_handles + mammal_handles + water_handle
labels = substrates + ['Stranded Mammal', 'Waterways']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=7.5,
                 fontsize=6, loc='upper left', frameon=True, framealpha=1)


# using the boundary of the shapefile features (Scotland outline), zoom the map to Scotland
ax.set_extent([xmin, xmax, ymin, ymax], crs=myCRS)

#adding grid lines
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-7.5, -6.5, -5.5, -4.5, -3.5],
                         ylocs=[10, 11, 9, 8, 7, 6, 5, 4])
gridlines.left_labels = True # turn off the left-side labels
gridlines.right_labels = False #turn off the right side labels
gridlines.bottom_labels = False # turn off the bottom labels

myFig.savefig('map.png', bbox_inches='tight', dpi=300)
plt.show()

