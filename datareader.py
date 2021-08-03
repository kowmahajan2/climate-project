import os
import numpy as np
import scipy as sp
import matplotlib.pyplot as mlp
from pyhdf.SD import SD, SDC
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob

"""# Open file.
FILE_NAME = "AIRS.2016.06.10.232.L2.SUBS2RET.v7.0.1.0.G20089173054.hdf"
hdf = SD(FILE_NAME, SDC.READ)

# List available SDS datasets.
print(hdf.datasets())

# Read dataset.
DATAFIELD_NAME='TSurfAir'
data3D = hdf.select(DATAFIELD_NAME)
data = data3D[:,:]

# Read geolocation dataset.
lat = hdf.select('Latitude')
latitude = lat[:,:]
lon = hdf.select('Longitude')
longitude = lon[:,:]

ax = mlp.axes(projection = ccrs.PlateCarree())

mlp.contourf(longitude, latitude, data, 50, transform = ccrs.PlateCarree(), cmap = "jet")

ax.coastlines(resolution= "50m")

mlp.savefig("surfTemp")
mlp.show()"""


levels = np.linspace(223, 323, 100)
date = input('enter date YYYY.MM.DD: ')
DATAFIELD_NAME = input('enter data field: ')

AIRS_date = "../../climate_data/AIRS/AIRS_India_2016_heatwave/AIRS." + str(date)
File_Name = AIRS_date + ".*"

i = 1

longitude = np.linspace(-180, 180, 360)
latitude = np.linspace(-90, 90, 180)

flat = np.zeros((180, 360))

ax = mlp.axes(projection = ccrs.PlateCarree())
ax.coastlines(resolution= "50m")
mlp.contourf(longitude, latitude, flat, transform = ccrs.PlateCarree(), cmap = "jet")

img_extent = [-180,180,-90,90]

for filename in glob.glob(File_Name, recursive = True):
    print(filename)
    
    hdf = SD(filename, SDC.READ)
    time = hdf.select("Time")
    print(time[0,0])
    data3D = hdf.select(DATAFIELD_NAME)
    data = data3D[:,:]

    lat = hdf.select('Latitude')
    latitude = lat[:,:]
    lon = hdf.select('Longitude')
    longitude = lon[:,:]

    mlp.contourf(longitude, latitude, data, levels, transform = ccrs.PlateCarree(), cmap = "jet")
    
    i = i+1

ax.gridlines()
ax.set_extent(img_extent)
mlp.title("surface temperature on 15 May")

mlp.colorbar(label = "Kelvin")
mlp.rcParams["figure.figsize"] = (10,10)

mlp.savefig("TSurfAirimg/surfTemp.png")
#mlp.show()
