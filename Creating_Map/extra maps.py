


#adding fishing vessels

with rst.open('Data_Files/National Maps/National Maps/Rasters/ScotMap_Central_numberVessel_aggr_3_190713/ScotMap_Central_numberVessel_aggr_3_190713.tif')\
        as dataset:
    xmin, ymin, xmax, ymax = dataset.bounds
    #crs = dataset.crs
    img = dataset.read




#fishingvessels = fishingvessels.to_crs("EPSG:27700")
#print(fishingvessels.crs)
#mappedvessels = fishingvessels.read()

#adding fishing restrictions
#no_fishing = gpd.read_file('Data_Files/area_management_fishing_restrictions/area_management_fishing_restrictionsPolygon.shp')
#no_fishing = no_fishing.to_crs("EPSG:27700")

#adding counties
#counties_feat = ShapelyFeature(counties['geometry'], myCRS, edgecolor='mediumblue', facecolor='mediumblue', linewidth=1)
#ax.add_feature(counties_feat)

#Adding no fishing zones
#no_fishing_feature = ShapelyFeature(no_fishing['geometry'], myCRS, edgecolor='mediumblue', facecolor='mediumblue', linewidth=2)
#ax.add_feature(no_fishing_feature)

#adding ordnance survey base map

map_background = rst.open('Data_Files/Over_gb/GBOverview.tif') #background Ordnance Survey map

print('{} opened in {} mode'.format(map_background.name,map_background.mode))
print('image has {} band(s)'.format(map_background.count))
print('image size (width, height): {} x {}'.format(map_background.width, map_background.height))
print('band 1 dataype is {}'.format(map_background.dtypes[2])) # note that the band name (Band 1) differs from the list index [0]
print(map_background.bounds)
print(map_background.crs)

with rst.open('Data_Files/Over_gb/GBOverview.tif') as background:
    img = background.read()
    xmin, ymin, xmax, ymax = background.bounds

myCRS = ccrs.UTM(29) # the background map CRS is EPSG:27700
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

ax.imshow(img[0:2], cmap='Set3', vmin=200, vmax=5000)
plt.show()