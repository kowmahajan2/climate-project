from pyhdf.SD import SD, SDC
import os

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


# Open file.
FILE_NAME = input("Enter an hdf4 file: ")
hdf = SD(FILE_NAME, SDC.READ)

# List available SDS datasets.
print(hdf.datasets())