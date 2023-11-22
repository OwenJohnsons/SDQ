'''
Code Purpose:
Author: 
Date: 
'''
#%% 
from glob import glob
import numpy as np 
from datetime import datetime, timedelta


file_list = glob('*.txt')
year_array = []; density_array = []

for file in file_list:
    year, density = np.loadtxt(file, skiprows=1, usecols = (2,4), unpack = True)
    year_array = np.append(year_array, year); density_array = np.append(density_array, density)

# - Fractional Year to MJD - 
def time_conversion(fractional_year):
    seconds_year = 24*60*60*365.25 # seconds in a year
    seconds_since = (fractional_year - int(fractional_year))*seconds_year

    # Calculate days, hours, and minutes
    days = seconds_since // (24 * 3600)
    hours = int((seconds_since % (24 * 3600)) // 3600)
    minutes = int((seconds_since % 3600) / 60)

    mjd = datetime(int(fractional_year), 1, 1) + timedelta(days = days, hours = hours, minutes = minutes)

    # Calculate the difference in days from the MJD epoch (November 17, 1858)
    mjd_epoch = datetime(1858, 11, 17)
    delta = mjd - mjd_epoch
    return delta.days + delta.seconds / (24 * 60 * 60)

mjd_array = np.array([time_conversion(year) for year in year_array])

# - Save the data -
np.savetxt('ACE-total-data.txt', np.c_[mjd_array, density_array], fmt = '%.8f %.4f', header = 'MJD Density')