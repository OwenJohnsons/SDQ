'''
Code Purpose: Extracts and flattens data from .nc files into a single .dat file.
Code Author: Owen A. Johnson 
Date: 2023-11-21
'''
#%%
import netCDF4 as nc
import numpy as np
from glob import glob
import datetime 
from astropy.time import Time
from tqdm import tqdm

file_list = sorted(glob('input-data/*f1m*.nc'))
print('Number of f1m files: ', len(file_list))
print('Approximate length of final array: ', len(file_list)*1440)

dates = []; densities = []; mjds = []

for file in tqdm(file_list):
    dataset = nc.Dataset(file, 'r')
    if 'proton_density' in dataset.variables:
        # - Density Extraction -
        proton_density = dataset.variables['proton_density'][:]
        densities = np.append(densities, proton_density[0:])

        # - Time Conversion - 
        time = dataset.variables['time'][:] # units: milliseconds since 1970-01-01T00:00:00Z
        converted_time = [datetime.datetime.utcfromtimestamp(t/1000) for t in time]
        dates = np.append(dates, converted_time)
        time_object = Time(converted_time, scale='utc')
        mjd = time_object.mjd; mjds = np.append(mjds, mjd)

# --- Remove Negative Data Entries --- 
print('Number of negative data entries: ', len(densities[densities < 0]))

# - Write to .dat file date, mjd and density -
data = np.column_stack((dates, mjds, densities))
np.savetxt(('DSCOVR-total-data-%s.txt' % dates[-1]), data, fmt=['%s', '%.6f', '%.2f'], delimiter='\t', header='Date\tMJD\tDensities (cm^3)')
print(f'Data has been merged and saved.')

# %%
