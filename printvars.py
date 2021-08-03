from pyhdf.SD import SD, SDC
import os

# Open file.
FILE_NAME = input("Enter an hdf4 file: ")
hdf = SD(FILE_NAME, SDC.READ)

# List available SDS datasets.
print(hdf.datasets())