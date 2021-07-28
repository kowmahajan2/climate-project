import os
import numpy as np
import scipy as sp
import matplotlib.pyplot as mlp
from pyhdf.SD import SD, SDC
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob

tarlat = input("Target latitude: ")
tarlon = input("Target longitude: ")

DATAFIELD_NAME = input('enter data field: ')

for filename in glob.glob("../../climate_data/AIRS/AIRS_India_2016_heatwave/*.hdf", recursive = True):
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

    var_time_series = []
    time_series = []
    aggr_var = []

    for i in range(0,len(latitude)):
        for j in range(0,len(latitude[0])):
            if(latitude[i,j] < float(tarlat) + 0.5 and latitude[i,j] > float(tarlat) - 0.5 and longitude[i,j] < float(tarlon) + 0.5 and longitude[i,j] > float(tarlon) - 0.5):
                aggr_var.append(data[i,j])
    
    var_time_series.append(np.mean(aggr_var))
    time_series.append(time[0,0])
    aggr_var = []    
    

    #mlp.plot(time[0,0], np.mean(aggr_var), label = "surftemp at " + str(tarlat) + " " + str(tarlon))

var_time_series = np.array(var_time_series)
time_series = np.array(time_series)

mlp.plot(time_series, vars_time_series, label = "surftemp at " + str(tarlat) + " " + str(tarlon))

mlp.title("Surface temps during 2016")

