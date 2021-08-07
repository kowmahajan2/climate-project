import os
import numpy as np
from numpy.core.fromnumeric import var
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
from pyhdf.SD import SD, SDC
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob
import time as time
import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def SinglePlotter(DATAFIELD_NAME, tarlat, tarlon, year,levels = 0):
    #variable to store the averaged value along with granule time
    var_time_series = [] 
    time_series = []
    #variable to store all available values for the target location in each granule file
    aggr_var = []
    hdf = SD("AIRS.2003.06.28.183.L2.SUBS2RET.v7.0.1.0.G20141014422.hdf", SDC.READ)
    data3D = hdf.select(str(DATAFIELD_NAME))
    if(len(np.shape(data3D)) == 2):
        for filename in glob.glob("../../climate_data/AIRS/AIRS_India_"+str(year)+"_AMJ/*.hdf", recursive = True):
            print(filename)
            hdf = SD(filename, SDC.READ)
            granule_time = hdf.select("Time")
            print(granule_time[0,0])
            
            #data variable
            data3D = hdf.select(DATAFIELD_NAME)
            data = data3D[:,:]
            #data quality control array
            dataQCimp = hdf.select(DATAFIELD_NAME + str("_QC"))
            dataQC = dataQCimp[:,:]

            #location array corresponding to the above data
            lat = hdf.select('Latitude')
            latitude = lat[:,:]
            lon = hdf.select('Longitude')
            longitude = lon[:,:]

            #collecting all the relevant values from the current granule discarding all irrelevant values
            for i in range(0,len(latitude)):
                for j in range(0,len(latitude[0])):
                    if(latitude[i,j] < float(tarlat) + 0.5 and latitude[i,j] > float(tarlat) - 0.5 and longitude[i,j] < float(tarlon) + 0.5 and longitude[i,j] > float(tarlon) - 0.5 and data[i,j]!=-9999 and dataQC[i,j] != 2):
                        aggr_var.append(float(data[i,j]))
                        print(str(latitude[i,j]) + " " + str(longitude[i,j]) + str(data[i,j]))
            
            #averaging all relevant granule values to an average variable
            avg_var = np.nanmean(aggr_var)

            #checking and adding the averaged value to the var_time_series and adding the corresponding granule time to the time_series 
            if(np.isfinite(avg_var)):
                var_time_series.append(np.nanmean(aggr_var))
                time_series.append(granule_time[0,0])
                print(aggr_var)  

            #plt.scatter(time[0,0], np.nanmean(aggr_var) , label = "surftemp at " + str(tarlat) + " " + str(tarlon))
            hdf.end()
            #resetting the aggr_var list
            aggr_var = []
        #convert into arrays
        var_time_series = np.array(var_time_series)
        time_series = np.array(time_series)
        #convert from time to days from first granule
        #time_series = (time_series - time_series[0])/86400

        print(var_time_series)
        print(time_series)

        plt.plot(time_series, var_time_series, label =   str(DATAFIELD_NAME) +" at " + str(tarlat) + " " + str(tarlon)+ "in" + str(year))
        plt.legend()
        plt.title(str(DATAFIELD_NAME) + "plot")
        plt.grid()
        plt.savefig("images/" + str(DATAFIELD_NAME) + str(tarlat) + "." + str(tarlon) +  "." + str(year) + ".png")
        plt.clf()
        return time_series, var_time_series


    elif(len(np.shape(data3D)) == 3):
        #levels = int(input("Which level to plot (0 for all of them): "))
        hdf.end()
        for filename in glob.glob("../../climate_data/AIRS/AIRS_India_"+ str(year) + "_AMJ/*.hdf", recursive = True):
            #print(filename)
            hdf = SD(filename, SDC.READ)
            granule_time = hdf.select("Time")
            #print(granule_time[0,0])

            data3D = hdf.select(DATAFIELD_NAME)
            data = data3D[:,:,:]
            #data quality control array
            dataQCimp = hdf.select(DATAFIELD_NAME + str("_QC"))
            dataQC = dataQCimp[:,:,:]

            lat = hdf.select('Latitude')
            latitude = lat[:,:]
            lon = hdf.select('Longitude')
            longitude = lon[:,:]

            for i in range(0,len(latitude)):
                for j in range(0,len(latitude[0])):
                    if(latitude[i,j] < float(tarlat) + 0.5 and latitude[i,j] > float(tarlat) - 0.5 and longitude[i,j] < float(tarlon) + 0.5 and longitude[i,j] > float(tarlon) - 0.5 and any(data[i,j]!=-9999) and any(dataQC[i,j] != 2)):
                        aggr_var.append(data[i,j,:])
                        #print(str(latitude[i,j]) + " " + str(longitude[i,j]) + str(data[i,j]))
            
            avg_var = np.mean(aggr_var)
            if(np.isfinite(avg_var)):
                var_time_series.append(np.nanmean(aggr_var, axis = 0))
                time_series.append(granule_time[0,0])
                #print(aggr_var)  

            #plt.scatter(time[0,0], np.nanmean(aggr_var) , label = "surftemp at " + str(tarlat) + " " + str(tarlon))
            hdf.end()
            aggr_var = []


        #plt.savefig("pointscatter")
        #plt.clf()

        var_time_series = np.array(var_time_series)
        time_series = np.array(time_series)
        #time_series = (time_series - time_series[0])/86400

        print(np.shape(var_time_series))
        print(np.shape(time_series))

        if(levels != 0):

            plt.plot(time_series, var_time_series[:,levels], label = "surftemp at " + str(tarlat) + " " + str(tarlon))
            plt.title(str(DATAFIELD_NAME) + "plot")
            plt.legend()
            plt.grid()
            plt.savefig("images/" + str(DATAFIELD_NAME) + "plot at " + str(tarlat) + " " + str(tarlon) + " at level " + str(levels)+ ".png")
            plt.clf()
            return time_series, var_time_series

        if(levels == 0):
            pressures = np.array([1100, 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50])
            xcords = []
            ycords = []
            magni = []
            for i in range(0, len(var_time_series)):
                for j in range(0, len(var_time_series[0])):
                    if var_time_series[i,j] != -9999:
                        xcords.append(time_series[i])
                        ycords.append(pressures[j])
                        magni.append(var_time_series[i,j])
            plt.scatter(xcords, ycords, c = magni, s = 10, cmap = "jet")
            #print(magni)

            #plt.ylim(bottom = 0, top = np.max(var_time_series))
            plt.title(str(DATAFIELD_NAME) + "plot")
            plt.grid()
            #ax1.legend()
            plt.savefig("images/" + str(DATAFIELD_NAME) + str(tarlat) + "." + str(tarlon) +  "." + str(year) + ".png")
            plt.clf()
            return time_series, var_time_series

def MultiPlotter(DATAFIELD_NAMES, tarlat, tarlon, year):
    fig, ax = plt.subplots(figsize = (10,10))
    twin = ax.twinx()
    #variable to store the averaged value along with granule time
    for fieldnumber in range(0,2):
        var_time_series = [] 
        time_series = []
        #variable to store all available values for the target location in each granule file
        aggr_var = []
        hdf = SD("AIRS.2003.06.28.183.L2.SUBS2RET.v7.0.1.0.G20141014422.hdf", SDC.READ)
        data3D = hdf.select(str(DATAFIELD_NAMES[fieldnumber]))
        if(len(np.shape(data3D)) == 2):
            for filename in glob.glob("../../climate_data/AIRS/AIRS_India_"+str(year)+"_AMJ/*.hdf", recursive = True):
                print(filename)
                hdf = SD(filename, SDC.READ)
                granule_time = hdf.select("Time")
                print(granule_time[0,0])
                
                #data variable
                data3D = hdf.select(DATAFIELD_NAMES[fieldnumber])
                data = data3D[:,:]
                #data quality control array
                dataQCimp = hdf.select(DATAFIELD_NAMES[fieldnumber] + str("_QC"))
                dataQC = dataQCimp[:,:]

                #location array corresponding to the above data
                lat = hdf.select('Latitude')
                latitude = lat[:,:]
                lon = hdf.select('Longitude')
                longitude = lon[:,:]

                #collecting all the relevant values from the current granule discarding all irrelevant values
                for i in range(0,len(latitude)):
                    for j in range(0,len(latitude[0])):
                        if(latitude[i,j] < float(tarlat) + 0.5 and latitude[i,j] > float(tarlat) - 0.5 and longitude[i,j] < float(tarlon) + 0.5 and longitude[i,j] > float(tarlon) - 0.5 and data[i,j]!=-9999 and dataQC[i,j] != 2):
                            aggr_var.append(float(data[i,j]))
                            print(str(latitude[i,j]) + " " + str(longitude[i,j]) + str(data[i,j]))
                
                #averaging all relevant granule values to an average variable
                avg_var = np.nanmean(aggr_var)

                #checking and adding the averaged value to the var_time_series and adding the corresponding granule time to the time_series 
                if(np.isfinite(avg_var)):
                    var_time_series.append(np.nanmean(aggr_var))
                    time_series.append(granule_time[0,0])
                    print(aggr_var)  

                #plt.scatter(time[0,0], np.nanmean(aggr_var) , label = "surftemp at " + str(tarlat) + " " + str(tarlon))
                hdf.end()
                #resetting the aggr_var list
                aggr_var = []
            #convert into arrays
            var_time_series = np.array(var_time_series)
            time_series = np.array(time_series)
            #convert from time to days from first granule
            time_series = (time_series - time_series[0])/86400

            print(var_time_series)
            print(time_series)
            if(fieldnumber == 0):
                ax.plot(time_series, var_time_series, alpha = 0.7, label =   str(DATAFIELD_NAMES[fieldnumber]) +" at " + str(tarlat) + " " + str(tarlon)+ "in" + str(year))
                ax.legend()
                ax.grid()
                fig.savefig("images/" + str(DATAFIELD_NAMES[fieldnumber]) + str(fieldnumber)+ "."  + str(tarlat) + "." + str(tarlon) + "." + str(year) + ".png")
            elif(fieldnumber == 1):
                twin.plot(time_series, var_time_series, label =   str(DATAFIELD_NAMES[fieldnumber]) +" at " + str(tarlat) + " " + str(tarlon)+ "in" + str(year))
                twin.legend()
                twin.grid()
                fig.savefig("images/" + str(DATAFIELD_NAMES[fieldnumber]) + str(fieldnumber)+ "."  + str(tarlat) + "." + str(tarlon) + "." + str(year) + ".png")


        elif(len(np.shape(data3D)) == 3):
            #levels = int(input("Which level to plot (0 for all of them): "))
            hdf.end()
            for filename in glob.glob("../../climate_data/AIRS/AIRS_India_"+ str(year) + "_AMJ/*.hdf", recursive = True):
                print(filename)
                hdf = SD(filename, SDC.READ)
                granule_time = hdf.select("Time")
                print(granule_time[0,0])

                data3D = hdf.select(DATAFIELD_NAMES[fieldnumber])
                data = data3D[:,:,:]
                #data quality control array
                dataQCimp = hdf.select(DATAFIELD_NAMES[fieldnumber] + str("_QC"))
                dataQC = dataQCimp[:,:,:]

                lat = hdf.select('Latitude')
                latitude = lat[:,:]
                lon = hdf.select('Longitude')
                longitude = lon[:,:]

                for i in range(0,len(latitude)):
                    for j in range(0,len(latitude[0])):
                        if(latitude[i,j] < float(tarlat) + 0.5 and latitude[i,j] > float(tarlat) - 0.5 and longitude[i,j] < float(tarlon) + 0.5 and longitude[i,j] > float(tarlon) - 0.5 and any(data[i,j]!=-9999) and any(dataQC[i,j] != 2)):
                            aggr_var.append(data[i,j,:])
                            print(str(latitude[i,j]) + " " + str(longitude[i,j]) + str(data[i,j]))

                avg_var = np.mean(aggr_var)
                if(np.isfinite(avg_var)):
                    var_time_series.append(np.nanmean(aggr_var, axis = 0))
                    time_series.append(granule_time[0,0])
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
                if(fieldnumber== 0):
                    ax.plot(time_series, var_time_series[:,levels], alpha = 0.7, label = "surftemp at " + str(tarlat) + " " + str(tarlon))
                    ax.legend()
                    ax.grid()
                    fig.savefig("images/" + str(DATAFIELD_NAMES[fieldnumber]) + str(fieldnumber) + str(tarlat) + "." + str(tarlon) +  "." + str(year) +  "." + str(levels) + ".png")
                elif(fieldnumber == 1):
                    twin.plot(time_series, var_time_series[:,levels], label = "surftemp at " + str(tarlat) + " " + str(tarlon))
                    twin.legend()
                    twin.grid()
                    fig.savefig("images/" + str(DATAFIELD_NAMES[fieldnumber]) + str(fieldnumber) + str(tarlat) + "." + str(tarlon) +  "." + str(year) +  "." + str(levels) + ".png")

            if(levels == 0):
                pressures = np.array([1100, 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50])
                xcords = []
                ycords = []
                magni = []
                for i in range(0, len(var_time_series)):
                    for j in range(0, len(var_time_series[0])):
                        if var_time_series[i,j] != -9999:
                            xcords.append(time_series[i])
                            ycords.append(pressures[j])
                            magni.append(var_time_series[i,j])

                if(fieldnumber == 0):
                    ax.scatter(xcords, ycords, c = magni, s = 10, cmap = "jet", alpha = 0.7, label =  str(DATAFIELD_NAMES[fieldnumber]) + " at " + str(tarlat) + " " + str(tarlon) +  " on " + str(year))
                    ax.grid()
                    ax.legend()
                    fig.savefig("images/" + str(DATAFIELD_NAMES[fieldnumber]) + str(fieldnumber) + str(tarlat) + "." + str(tarlon) +  "." + str(year) + ".png")
                elif(fieldnumber == 1):
                    twin.scatter(xcords, ycords, c = magni, s = 10, cmap = "jet", label =  str(DATAFIELD_NAMES[fieldnumber]) + " at " + str(tarlat) + " " + str(tarlon) +  " on " + str(year))
                    twin.grid()
                    twin.legend()
                    fig.savefig("images/" + str(DATAFIELD_NAMES[fieldnumber]) + str(fieldnumber) + str(tarlat) + "." + str(tarlon) +  "." + str(year) + ".png")
                
                print(magni)


def DayAvgVar(time_series, var_time_series):
    avg_var = []
    days = np.linspace(1,91,91)
    aggr_var = []
    epoch_time = time.mktime((1993, 1,1,0,0,0,4,1,0)) + 5.5*3600
    day = time.gmtime(epoch_time + time_series[0])[2]
    start_day = time.gmtime(epoch_time + time_series[0])[7] - time.gmtime(epoch_time + time_series[0])[2] + 1 
    granule = 0
    for day in days:
        #print(current_day + day -1)
        while time.gmtime(epoch_time + time_series[granule])[7] == start_day + day -1:
            aggr_var.append(var_time_series[granule])
            granule = granule +1
            if granule >= len(var_time_series):
                break
        aggr_var = np.array(aggr_var)
        if len(aggr_var) == 0:
            avg_var.append(np.zeros(np.shape(var_time_series[1])) - 9999)
            aggr_var = []
        else:
            avg_var.append(np.nanmean(aggr_var, axis = 0))
            aggr_var = []
        if granule >= len(var_time_series):
            break
    while len(avg_var) < 91:
        avg_var.append(np.zeros(np.shape(var_time_series[1])) - 9999)

    avg_var = np.array(avg_var)
    return days, avg_var


def AnoSinglePlotter(DATAFIELD_NAME, tarlat, tarlon, taryear):
    aggr_var_series = []
    days = np.linspace(1, 91, 91)

    for year in range(2003,2022):
        print(year)
        blockPrint()
        year_data = SinglePlotter(DATAFIELD_NAME, tarlat, tarlon, year)
        enablePrint()
        print(np.shape(year_data[1]))
        #print(year_data[0]/86400)
        #print(year_data[1])
        day_avg_var = DayAvgVar(year_data[0], year_data[1])
        #print(day_avg_var)
        aggr_var_series.append(day_avg_var[1])
        print(np.shape(day_avg_var[1]))
    print(len(aggr_var_series))
    aggr_var_series = np.array(aggr_var_series)
    
    avg_var_series = np.nanmean(aggr_var_series, axis = 0)
    print("final shape" + str(len(np.shape(avg_var_series))))
    if len(np.shape(avg_var_series)) == 1:
        if int(taryear) == 0:
            for iter_year in range(2003, 2022):
                plt.plot(days, aggr_var_series[int(iter_year) - 2003] - avg_var_series, label =   str(DATAFIELD_NAME) +" anomalies at " + str(tarlat) + " " + str(tarlon)+ "in" + str(iter_year))
                plt.legend()
                plt.title(str(DATAFIELD_NAME) + " anomalies plot")
                plt.grid()
                plt.savefig("images/" + str(DATAFIELD_NAME)+"anom" + str(tarlat) + "." + str(tarlon) +  "." + str(iter_year) + ".png")
                plt.clf()
        else:
            plt.plot(days, aggr_var_series[int(taryear) - 2003] - avg_var_series, label =   str(DATAFIELD_NAME) +" anomalies at " + str(tarlat) + " " + str(tarlon)+ "in" + str(taryear))
            plt.legend()
            plt.title(str(DATAFIELD_NAME) + " anomalies plot")
            plt.grid()
            plt.savefig("images/" + str(DATAFIELD_NAME)+"anom" + str(tarlat) + "." + str(tarlon) +  "." + str(taryear) + ".png")
    else:
        print("plotting")
        if int(taryear) == 0:
            for iter_year in range(2003, 2022):
                print(iter_year)
                pressures = np.array([1100, 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50])
                xcords = []
                ycords = []
                magni = []
                for i in range(0, len(aggr_var_series[0])):
                    for j in range(0, len(aggr_var_series[0,0])):
                        if aggr_var_series[iter_year - 2003,i,j] != -9999 and avg_var_series[i,j] >= 0:
                            xcords.append(days[i])
                            ycords.append(pressures[j])
                            magni.append(aggr_var_series[iter_year - 2003,i,j] - avg_var_series[i,j])
                plt.scatter(xcords, ycords, c = magni, s = 10, cmap = "jet", label = str(DATAFIELD_NAME)+" anomaly at" + str(tarlat) + "." + str(tarlon) +  " in " + str(iter_year))
                #print(magni)

                #plt.ylim(bottom = 0, top = np.max(var_time_series))
                plt.colorbar()
                plt.title(str(DATAFIELD_NAME) + "plot")
                plt.grid()
                #ax1.legend()
                plt.savefig("images/" + str(DATAFIELD_NAME)+"anom" + str(tarlat) + "." + str(tarlon) +  "." + str(iter_year) + ".png")
                plt.clf()
        else:
            plt.plot(days, aggr_var_series[int(taryear) - 2003] - avg_var_series, label =   str(DATAFIELD_NAME) +" anomalies at " + str(tarlat) + " " + str(tarlon)+ "in" + str(taryear))
            plt.legend()
            plt.title(str(DATAFIELD_NAME) + " anomalies plot")
            plt.grid()
            plt.savefig("images/" + str(DATAFIELD_NAME)+"anom" + str(tarlat) + "." + str(tarlon) +  "." + str(taryear) + ".png")


    

    
#target location
tarlat = input("Target latitude: ")
tarlon = input("Target longitude: ")
#year of interest
taryear = input("year: ")

#number of datafields to plot, doesn't really work right now
#only use one datafield name  until more functionality is added
datafields = input("number of datafields: ")

DATAFIELD_NAMES = []
for i in range(0, int(datafields)):
    DATAFIELD_NAMES.append(input('enter data field: '))


#whether to plot just the value or the anomaly from average
plottype = input("0:time series 1:anomaly: ")
#Which levels to plot
levels = int(input("Which level to plot (0 for all of them): "))
#sample file to check variable properties
hdf = SD("AIRS.2003.06.28.183.L2.SUBS2RET.v7.0.1.0.G20141014422.hdf", SDC.READ)
granule_time = hdf.select("Time")
print(granule_time[0,0])

if len(DATAFIELD_NAMES) == 1:
    if int(plottype) == 0:
        #works completely i think
        SinglePlotter(DATAFIELD_NAMES[0], tarlat, tarlon, taryear, levels)
    elif int(plottype) == 1:
        #works well enough, enter 0 in target year to plot anomaly for all the years, doesn't incur any extra processing cost
        AnoSinglePlotter(DATAFIELD_NAMES[0], tarlat, tarlon, taryear)
elif len(DATAFIELD_NAMES) == 2:
    #works I think, only 2 datafields, why would you wanna plot more anyway
    MultiPlotter(DATAFIELD_NAMES, tarlat, tarlon, taryear)

#To add 
# anomaly plotter for multiple datafields
# add unplotting versions for each of the functions to reduce cost.
# add non clearing versions of each plotter, to plot even more data on the same plot. 
