
#This section of the code will perform some analysis on links between marine mammal strandings and beach substrate

# importing relevant modules
import geopandas as gpd
import matplotlib.pyplot as plt

#importing datasets
beach_substrate = gpd.read_file('Data_Files/Intertidal+Substrate+Foreshore+(England+and+Scotland)'
                                '/Intertidal Substrate Foreshore (England and Scotland)/DEFR00000009.shp')
marinestrandings = gpd.read_file('marinestrandings.shp')

#setting the CRS
marinestrandings = marinestrandings.to_crs("EPSG:27700") #converting the CRS
print(beach_substrate.crs) # checking if CRS is correct (should be EPSG:27700)
beach_substrate = beach_substrate.set_crs("EPSG:27700")


#First, we can take a look at how many of each marine mammal was found stranded in Scotland within the study
# time frame, ordered by count
print(marinestrandings['SubClass'].value_counts())

#Next we will try to identify any relationships between mammal strandings and beach substrate
#Completing a spatial join to compare the datasets
mammalsubstratejoin = gpd.sjoin(marinestrandings, beach_substrate, how='inner', lsuffix='left', rsuffix='right') # perform the spatial join

#(Note that as sum marine mammals were not found on beaches (floating at sea, etc.) the total number of strandings will
#decrease once join is completed)

mammalsubstrategrouped = mammalsubstratejoin.groupby(['SubClass', 'FORE_DESC'])['SubClass'].size().to_frame('size') # summarize the strandings by beach substrate
#added size as new column 'size' for use in bar chart

# The grouped dataset had set the 'SubClass' as the index which would cause problems later on, so I will reset this:
mammalsubstrategrouped.reset_index(inplace=True)
mammalsubstrategrouped.info(verbose=True)
#Some of the rows had split into two due to different letters being capatalised, so I will prevent this by making
#letter capitals the same across the dataset:
mammalsubstrategrouped['SubClass'] = mammalsubstrategrouped['SubClass'].str.capitalize()

print(mammalsubstrategrouped)

# In order to put the results into a bar chart, we want to reorder the dataframe so that each beach substrate type
#has its own column:
newdf = mammalsubstrategrouped.reset_index().groupby(['SubClass', 'FORE_DESC'])['size'].aggregate('first').unstack()
newdf.to_csv('newdf.csv')

print(newdf.head()) # making sure that worked

# fixing the index row again:
newdf.reset_index(inplace=True)
newdf.info(verbose=True)
newdf['SubClass'] = newdf['SubClass'].str.capitalize()

newdf = newdf.sort_values('SubClass')

# Now I will create a bar chart indicating the distribution of beach substrate types amongst marine mammal strandings:

ax = newdf.plot.bar(x='SubClass', stacked=True, color=["indianred", "coral", "gold", "olive", "forestgreen",
                                                       "mediumturquoise",
                                                       "lightskyblue", "royalblue", "darkslateblue",
                                                       "mediumpurple", "violet", "tab:pink", "tab:brown"], width=0.2,
                    figsize=(15,8))
ax.set_title('Stranding Substrates', fontsize=20)
ax.set_ylim(0,2100)
ax.set_xticklabels(['Basking shark','Bottlenose dolphin','Cetacean', 'Grey seal', 'Harbour porpoise',
                    'Harbour seal', 'Kogia', 'Marine turtle', 'Mysticete', 'Pelagac Delphinid',
                    'Pinniped', 'Pinniped indeterminate', 'Shark', 'Sperm/beaked whale'], rotation=0, fontsize=8)
plt.legend(['Boulders/Loose Rock', 'Gravel', 'Made Ground (Man Made)', 'Mud', 'Mud and Gravel', 'Not Present',
            'Rock Platform', 'Rock platform with banks of gravel', 'Rock platform with boulders/loose rock',
            'Sand', 'Sand & Gravel', 'Sand & Mud', 'Unspecified'], loc='upper left', ncol = 1, fontsize=8)
#ax.spines['right'].set_visible(False)
#ax.spines['left'].set_visible(False)
#ax.spines['top'].set_visible(False)
#ax.spines['bottom'].set_visible(False)
# draw grid lines
ax.set_axisbelow(True)
ax.yaxis.grid(color='gray', linestyle='dashed')

# Note: the bar chart will print at the end of this code to prevent the code from stopping
# In order to add more meaning to these results, it is useful to know the percentage area covered by each substrate type

for i, row in beach_substrate.iterrows(): # iterate over each row in the GeoDataFrame
    beach_substrate.loc[i, 'Area'] = row['geometry'].area # assign the row's geometry area to a new column, Area

print(beach_substrate.head()) # checking the new geodataframe has changed correctly

#creating a function so we don't have to write the individual calculation of substrate area each time:
def substrate_percent(beach):
    total_beach = beach_substrate['Area'].sum()
    specify_beach = beach_substrate[beach_substrate['FORE_DESC'] == beach]['Area'].sum()
    area = (specify_beach / total_beach) * 100
    print('Total percentage area of ' + beach + ' is {:.2f}'.format(area))

#Printing the areas of each substrate type:
substrate_percent('GRAVEL')
substrate_percent('SAND')
substrate_percent('BOULDERS/LOOSE ROCK')
substrate_percent('MADE GROUND (MAN MADE)')
substrate_percent('MUD')
substrate_percent('MUD & GRAVEL')
substrate_percent('NOT PRESENT')
substrate_percent('ROCK PLATFORM')
substrate_percent('ROCK PLATFORM WITH BANKS OF GRAVEL')
substrate_percent('ROCK PLATFORM WITH BOULDERS /LOSE ROCK')
substrate_percent('SAND & GRAVEL')
substrate_percent('SAND & MUD')
substrate_percent('UNSPECIFIED')

#Finally, we will compare these percentages to percentages from the joined dataframe above
#Writing a function so we don't have to individually calculate percentage of strandings each time
def strandings_percent(beach):
    total_strandings = mammalsubstrategrouped['size'].sum()
    per_beach = (newdf[beach].sum() / total_strandings) * 100
    print('Total percentage of strandings in ' + beach + ' is {:.2f}'.format(per_beach))

print("----------------------------------------------") # so that results are easier to distinguish on the terminal
# printing the percentage of strandings on each substrate type
strandings_percent('GRAVEL')
strandings_percent('SAND')
strandings_percent('BOULDERS/LOOSE ROCK')
strandings_percent('MADE GROUND (MAN MADE)')
strandings_percent('MUD')
strandings_percent('MUD & GRAVEL')
strandings_percent('NOT PRESENT')
strandings_percent('ROCK PLATFORM')
strandings_percent('ROCK PLATFORM WITH BANKS OF GRAVEL')
substrate_percent('ROCK PLATFORM WITH BOULDERS /LOSE ROCK')
strandings_percent('SAND & GRAVEL')
strandings_percent('SAND & MUD')
strandings_percent('UNSPECIFIED')

#From this we can see that sand makes up 45.88 percent of marine mammal strandings, but only 13.13% of total beach type
#Rock  platform makes up 41.08% of beach type but only 18.11% of strandings (strandings that have been reported at least)
plt.show()
