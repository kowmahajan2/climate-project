import os
import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from pyhdf.SD import SD, SDC
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob
from cycler import cycler



img_extent = [50,110,0,50]

month = input("enter target month(01-12): ")
DATAFIELD_NAME = input("Enter target variable: ")
#monthly_func = input("Monthly max(1), min(2), mean(3)")
#daily_func = input("Daily max(1), min(2), mean(3)")
Lats = np.linspace(0,50,101)
Lons = np.linspace(50,110,121)
aggr_var =  np.empty((101,121), dtype = object)

for i in range(0,len(aggr_var)):
    for j in range(0, len(aggr_var[0])):
        aggr_var[i,j] = []

avg_var = np.zeros((19,101,121))

hdf = SD("AIRS.2003.06.28.183.L2.SUBS2RET.v7.0.1.0.G20141014422.hdf", SDC.READ)
time = hdf.select("Time")
print(time[0,0])

data3D = hdf.select(DATAFIELD_NAME)

for year in range(2003, 2022):
    for filename in glob.glob("../../climate_data/AIRS/AIRS_India_" + str(year) + "_AMJ/AIRS." +str(year) +"." + str (month) + "*.hdf", recursive = True):
        print(filename)
        hdf = SD(filename, SDC.READ)
        time = hdf.select("Time")
        print(time[0,0])

        data3D = hdf.select(DATAFIELD_NAME)
        data = data3D[:,:]
        dataQCimp = hdf.select(DATAFIELD_NAME + str("_QC"))
        dataQC = dataQCimp[:,:]

        lat = hdf.select('Latitude')
        latitude = lat[:,:]
        latitude = np.array(latitude)
        latitude = np.round(2*latitude, decimals = 0)/2
        lon = hdf.select('Longitude')
        longitude = lon[:,:]
        longitude = np.array(longitude)
        longitude = np.round(2*longitude, decimals = 0)/2
        #print(latitude)

        for i in range(0,len(latitude)):
            for j in range(0,len(latitude[0])):
                if(latitude[i,j] < 50 and latitude[i,j] > 0 and longitude[i,j] < 110 and longitude[i,j] > 50 and data[i,j]!=-9999 and dataQC[i,j] != 2):
                    #print(latitude[i,j]*2, (longitude[i,j] - 50)*2)
                    aggr_var[int(latitude[i,j]*2), int((longitude[i,j] - 50)*2)].append(data[i,j])
                    #print(str(latitude[i,j]) + " " + str(longitude[i,j]) + str(data[i,j]))
    
    for i in range(0,len(aggr_var)):
        for j in range(0, len(aggr_var[0])):
            aggr_var[i,j] = np.array(aggr_var[i,j])

    for i in range(0,len(aggr_var)):
        for j in range(0, len(aggr_var[0])):
            avg_var[year - 2003,i,j] = np.mean(aggr_var[i,j])
    
    aggr_var =  np.empty((101,121), dtype = object)

    for i in range(0,len(aggr_var)):
        for j in range(0, len(aggr_var[0])):
            aggr_var[i,j] = []

print(avg_var)


#mlp.show()
levels = np.linspace(0,80, 100)
for i in range(0, 19):
    ax = plt.axes(projection = ccrs.PlateCarree())
    ax.gridlines()
    ax.set_extent(img_extent)
    ax.coastlines(resolution= "50m")
    plt.title("CWV climatology " + str(month))
    plt.rcParams["figure.figsize"] = (10,10)

    plt.contourf(Lons, Lats, avg_var[i], levels, transform = ccrs.PlateCarree(), extend = "both", cmap = "jet")
    plt.colorbar(label = "Kg/m^2")
    plt.savefig("images/CWV" + str(2003+i) + str(month))
    plt.clf()   

times = np.linspace(2003, 2021, 19)
cwv_trend = np.zeros((len(avg_var[0]), len(avg_var[0,0])))
cwv_const = np.zeros((len(avg_var[0]), len(avg_var[0,0])))
cwv_trend_sig = np.zeros((len(avg_var[0]), len(avg_var[0,0])))
cwv_const_sig = np.zeros((len(avg_var[0]), len(avg_var[0,0])))
cwv_sig = np.zeros((len(avg_var[0]), len(avg_var[0,0])))
for i in range(0,len(avg_var[0]) ):
    print(i)
    for j in range(0,len(avg_var[0,0])):
        #mask = ~np.isnan(avg_var[:,i,j])
        linreg = sp.stats.linregress(times, avg_var[:,i,j])
        #print(str(linreg[2]) + " " + str(linreg[3]))
        cwv_trend[i,j], cwv_const[i,j] = linreg[0], linreg[1]
        if(linreg[3]<0.05):
            cwv_trend_sig[i,j], cwv_const_sig[i,j] = linreg[0], linreg[1]
            cwv_sig[i,j] = 1
 
ax = plt.axes(projection = ccrs.PlateCarree())
ax.gridlines()
ax.set_extent(img_extent)
ax.coastlines(resolution= "50m")
ax.add_feature(cfeature.BORDERS.with_scale('10m'),
               linestyle='-', alpha=.3)
plt.title("CWV trends "+ str(month))
plt.rcParams["figure.figsize"] = (10,10)
levels = np.linspace(-0.5, 0.5, 20)
plt.contourf(Lons, Lats, cwv_trend, levels, transform = ccrs.PlateCarree(),  extend = "both", cmap = "coolwarm")
plt.colorbar(label = "Kg/m^2/yr")
plt.savefig("images/CWVtrends"+ str(month))
plt.clf()

ax = plt.axes(projection = ccrs.PlateCarree())
ax.gridlines()
ax.set_extent(img_extent)
ax.coastlines(resolution= "50m")
ax.add_feature(cfeature.BORDERS.with_scale('10m'),
               linestyle='-', alpha=.3)
plt.title("CWV significant trends " + str(month))
plt.rcParams["figure.figsize"] = (10,10)
levels = np.linspace(-0.5, 0.5, 20)
plt.contourf(Lons, Lats, cwv_trend_sig, levels, transform = ccrs.PlateCarree(),  extend = "both", cmap = "coolwarm")
plt.colorbar(label = "Kg/m^2/yr")
plt.savefig("images/CWVtrendssig"+ str(month))
plt.clf()

