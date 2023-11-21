#%% 
'''
Code Purpose: 
Code Author: Owen A. Johnson 
Date: 2023-11-20
'''
import argparse
import netCDF4 as nc
from glob import glob
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import datetime 
import numpy as np 
import scienceplots
plt.style.use('science')

file_list = glob('input-data/*f1m*.nc')
print('Number of f1m files: ', len(file_list))

plotting = True

for file in file_list:
    dataset = nc.Dataset(file, 'r')
    if 'proton_density' in dataset.variables:
        time = dataset.variables['time'][:] # units: milliseconds since 1970-01-01T00:00:00Z
        # convert to DD-MM-YYYY HH:MM:SS
        converted_time = [datetime.datetime.utcfromtimestamp(t/1000) for t in time]
        converted_time_float = [t.hour + t.minute/60 for t in converted_time]
        proton_density = dataset.variables['proton_density'][:]
        print('Filename: ', file)

        if plotting == True:
            plt.figure(figsize=(16, 4), dpi = 200)
            
            plt.scatter(converted_time_float, proton_density, s=1, facecolors='none', edgecolors='k')
            plt.axhline(y=proton_density.mean(), color='r', linestyle='--', label='Mean: %s' % np.round(proton_density.mean(), 2))
            plt.axhline(y=np.median(proton_density), color='g', linestyle='--', label='Median: %s' % np.round(np.median(proton_density), 2))
            plt.axhline(y=proton_density.mean() + proton_density.std(), color='b', linestyle=':', label='$\sigma$')
            plt.axhline(y=proton_density.mean() - proton_density.std(), color='b', linestyle=':') 

            plt.title('Observation Start Time: ' + str(converted_time[0]))
            plt.ylabel('Density (cm$^{-3}$)'); plt.xlabel('Time (hours)')
            plt.xlim(0, 24); plt.legend()
            plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.savefig('plots/' + str(converted_time[0])[0:-9] + '.png')
    else: 
        print('No density variable in file: ', file)
    break