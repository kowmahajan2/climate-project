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

var_time_series = []
time_series = []
aggr_var = []

hdf = SD("AIRS.2016.06.10.232.L2.SUBS2RET.v7.0.1.0.G20089173054.hdf", SDC.READ)
time = hdf.select("Time")
print(time[0,0])

data3D = hdf.select(DATAFIELD_NAME)
print(np.shape(data3D))