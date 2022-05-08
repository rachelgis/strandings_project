# strandings_project
Python coding project for EGM722: Marine mammal strandings in Scotland
Strandings data provided by Scottish Marine Animal Stranding Scheme - Thanks to SMASS for their kind provision of this data. 
Step 1: Creates a map of Scotland and pins locations of strandings - code title is 'Creating_Map'
Step 2: Performs analysis on links between marine mammal strandings and beach substrate type - code title is 'Strandings_Analysis'

This python project aims to provide a method for exploring Marine Mammal Strandings and their causes. 
In this version, the project specifically looks at the relationship between marine mammal strandings, and beach substrate type, however the code can be adapted for other research areas: including fishing vessel areas, population density, etc. 
Thank you to the Scottish Marine Animal Stranding Scheme, who kindly sent me their data on marine mammal strandings for the purpose of this project. Their website can be found by navigating to: https://strandings.org/
If you have any questions about this code or project, please contact Cribbin-R@ulster.ac.uk

2.0 Set up and Installation Instructions
This code is designed to be compatible for download in virtual environment conda, and for running using an Integrated Development Environment. The code was created using PyCharm, but has not been tested in other IDEs, so we would recommend using PyCharm community edition if possible. 
Accessing the code, test data, and dependencies for installation
Navigate to https://github.com/rachelgis/strandings_project to access the repository which contains Parts 1 and 2 of the code, the relevant test data, and the dependencies for installation (found in the environment.yml file). 
The dependencies can also be seen here:
name: strandings_project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.8.8
  - geopandas=0.9.0
  - cartopy=0.18.0
  - notebook=6.2.0
  - matplotlib=3.5.1
  - pandas=1.4.2
  - shapely=1.8.0

The test data files required for this project can be found in the Data_Files section of the GitHub repository. The code has been written in such a way that the test data should be automatically pulled in to the code, and you should not need to change these, so long as you don’t change the location of the Python scripts from where they are in the “Part 1 and 2 of Strandings Project” folder.
Recommended step by step for ensuring it all runs smoothly (assuming GitHub and Anaconda Navigator are installed) is:
1)	Fork the repository provided again here: https://github.com/rachelgis/strandings_project  by clicking ‘fork’ to create a copy to your GitHub account. 
2)	Clone your copy of the repository to GitHub desktop
3)	Open Anaconda navigator, and create a new environment using the environment.yml file provided in the GitHub repository (go to the environments tab, click import, and open the environment file from the downloaded git repository on your desktop). 
4)	Navigate to the new environment page, and install the PyCharm (Community Edition) IDE 
5)	Open the IDE, and open Part 1 of the python script from the GitHub repository (called ‘Creating_Map’. 
6)	Once open, click where it says “Python 3.9” in the bottom right of the corner, click ‘Add interpreter’, then ‘Conda environment’, and then select ‘Existing environment’, and ensure the new conda environment is navigated to. 
7)	Then click ‘Add configuration’ and add the path to the script you are trying to run, and ensure “Python interpreter” is set to the correct environment
8)	Once this is done, you should be able to go ahead and run the codes. When running the second code, you will just need to edit the configuration to point to the second code, but the interpreter can remain the same.

