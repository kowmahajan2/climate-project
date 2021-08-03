import os
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from pyhdf.SD import SD, SDC
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob
from cycler import cycler

tarlat = input("Target latitude: ")
tarlon = input("Target longitude: ")

year = input("year: ")

datafields = input("number of datafields: ")

plottype = input("0:time series 1:anomaly: ")
DATAFIELD_NAMES = []
for i in range(0, int(datafields)):
    DATAFIELD_NAMES.append(input('enter data field: '))



hdf = SD("AIRS.2003.06.28.183.L2.SUBS2RET.v7.0.1.0.G20141014422.hdf", SDC.READ)
time = hdf.select("Time")
print(time[0,0])
for DATAFIELD_NAME in DATAFIELD_NAMES:
    print(DATAFIELD_NAME)
    var_time_series = []
    time_series = []
    aggr_var = []
    hdf = SD("AIRS.2003.06.28.183.L2.SUBS2RET.v7.0.1.0.G20141014422.hdf", SDC.READ)
    data3D = hdf.select(str(DATAFIELD_NAME))
    if(len(np.shape(data3D)) == 2):
        
        for filename in glob.glob("../../climate_data/AIRS/AIRS_India_"+str(year)+"_AMJ/*.hdf", recursive = True):
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
            lon = hdf.select('Longitude')
            longitude = lon[:,:]

            for i in range(0,len(latitude)):
                for j in range(0,len(latitude[0])):
                    if(latitude[i,j] < float(tarlat) + 0.5 and latitude[i,j] > float(tarlat) - 0.5 and longitude[i,j] < float(tarlon) + 0.5 and longitude[i,j] > float(tarlon) - 0.5 and data[i,j]!=-9999 and dataQC[i,j] != 2):
                        aggr_var.append(float(data[i,j]))
                        print(str(latitude[i,j]) + " " + str(longitude[i,j]) + str(data[i,j]))
            
            avg_var = np.nanmean(aggr_var)
            if(np.isfinite(avg_var)):
                var_time_series.append(np.nanmean(aggr_var))
                time_series.append(time[0,0])
                print(aggr_var)  

            #plt.scatter(time[0,0], np.nanmean(aggr_var) , label = "surftemp at " + str(tarlat) + " " + str(tarlon))
            hdf.end()
            aggr_var = []


        #plt.savefig("pointscatter")
        #plt.clf()

        var_time_series = np.array(var_time_series)
        time_series = np.array(time_series)
        time_series = (time_series - time_series[0])/86400

        print(var_time_series)
        print(time_series)

        plt.plot(time_series, var_time_series, label =   str(DATAFIELD_NAME) +" at " + str(tarlat) + " " + str(tarlon)+ "in" + str(year))
        plt.legend()
        plt.title(str(DATAFIELD_NAME) + "plot")
        plt.grid()
        plt.savefig("images/" + str(DATAFIELD_NAME) + "plot at " + str(tarlat) + " " + str(tarlon) + "in" + str(year) + ".png")


    elif(len(np.shape(data3D)) == 3):
        levels = int(input("Which level to plot (0 for all of them): "))
        hdf.end()
        for filename in glob.glob("../../climate_data/AIRS/AIRS_India_"+ str(year) + "_AMJ/*.hdf", recursive = True):
            print(filename)
            hdf = SD(filename, SDC.READ)
            time = hdf.select("Time")
            print(time[0,0])

            data3D = hdf.select(DATAFIELD_NAME)
            data = data3D[:,:,:]

            lat = hdf.select('Latitude')
            latitude = lat[:,:]
            lon = hdf.select('Longitude')
            longitude = lon[:,:]

            for i in range(0,len(latitude)):
                for j in range(0,len(latitude[0])):
                    if(latitude[i,j] < float(tarlat) + 0.5 and latitude[i,j] > float(tarlat) - 0.5 and longitude[i,j] < float(tarlon) + 0.5 and longitude[i,j] > float(tarlon) - 0.5 ):
                        aggr_var.append(data[i,j,:])
                        print(str(latitude[i,j]) + " " + str(longitude[i,j]) + str(data[i,j]))
            
            avg_var = np.mean(aggr_var)
            if(np.isfinite(avg_var)):
                var_time_series.append(np.nanmean(aggr_var, axis = 0))
                time_series.append(time[0,0])
                print(aggr_var)  

            #plt.scatter(time[0,0], np.nanmean(aggr_var) , label = "surftemp at " + str(tarlat) + " " + str(tarlon))
            hdf.end()
            aggr_var = []


        #plt.savefig("pointscatter")
        #plt.clf()

        var_time_series = np.array(var_time_series)
        time_series = np.array(time_series)
        time_series = (time_series - time_series[0])/86400

        print(np.shape(var_time_series))
        print(np.shape(time_series))

        if(levels != 0):
            plt.plot(time_series, var_time_series[:,levels], label = "surftemp at " + str(tarlat) + " " + str(tarlon))
            plt.title(str(DATAFIELD_NAME) + "plot")
            plt.legend()
            plt.grid()
            plt.savefig("images/" + str(DATAFIELD_NAME) + "plot at " + str(tarlat) + " " + str(tarlon) + " at level " + str(levels)+ ".png")
        if(levels == 0):
            n = len(var_time_series[0])
            color = plt.cm.coolwarm(np.linspace(0.1,0.9,n)) # This returns RGBA; convert:
            hexcolor = map(lambda rgb:'#%02x%02x%02x' % (rgb[0]*255,rgb[1]*255,rgb[2]*255),
                        tuple(color[:,0:-1]))
            custom_cycler = (cycler(color=color))
            fig, ax1 = plt.subplots(1,1)
            ax1.set_prop_cycle(custom_cycler)
            for i in range(0,len(var_time_series[0])):
                ax1.plot(time_series, var_time_series[:,i], label = str(DATAFIELD_NAME) +" at " + str(tarlat) + " " + str(tarlon) + " at level " + str(i)+ ".png")
            """pressures = np.array([1100, 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50])
            print(np.shape(pressures))
            print(np.shape(var_time_series))
            plt.scatter(time_series, pressures, c = var_time_series, cmap = "jet")"""
            plt.ylim(bottom = 0, top = np.max(var_time_series))
            plt.title(str(DATAFIELD_NAME) + "plot")
            plt.grid()
            #ax1.legend()
            plt.savefig("images/" + str(DATAFIELD_NAME) + "scatter " + str(tarlat) + " " + str(tarlon))