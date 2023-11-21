#%% 
'''
Code Purpose: 
Code Author: Owen A. Johnson 
Date: 2023-11-20
'''
import argparse
import netCDF4 as nc
from glob import glob
import pandas as pd
import datetime 
import numpy as np 

parser = argparse.ArgumentParser(description='Plots Solar electron densitites for a given MJD range.')
parser.add_argument('-s', '--start', type=float, help='Start MJD', required=True)
parser.add_argument('-f', '--end', type=float, help='End MJD', required=True)
parser.add_argument('-p', '--plot', action='store_true', help='Plot data (default = True)', default=True)
args = parser.parse_args()

df = pd.read_csv('DSCOVR-total-data.txt', delimiter='\t', header=0)
dates = df['# Date'].values; mjds = df['MJD'].values; densities = df['Densities (cm^3)'].values

def nearest_idx(val, array):
    idx = (np.abs(array - val)).argmin()
    return idx

start_idx = nearest_idx(args.start, mjds); end_idx = nearest_idx(args.end, mjds)
print('Start index: ', start_idx, 'End index: ', end_idx)

proton_density = densities[start_idx:end_idx]; mjd_times = mjds[start_idx:end_idx]
# hours from MJD start time
converted_time_float = (mjd_times - mjd_times[0])*24
print('Number of data points: ', len(proton_density))

# --- Save Values to .txt file ---
data = np.column_stack((mjd_times, proton_density))
np.savetxt('output-data/DSCOVR-data-%s-%s.txt' % (args.start, args.end), data, fmt=['%.6f', '%.2f'], delimiter='\t', header='MJD\tDensities (cm^3)')

if args.plot == True:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator
    import scienceplots

    plt.style.use('science'); plt.figure(figsize=(16, 4), dpi = 200)
    
    plt.scatter(converted_time_float, proton_density, s=1, facecolors='none', edgecolors='k')
    plt.axhline(y=proton_density.mean(), color='r', linestyle='--', label='Mean: %s' % np.round(proton_density.mean(), 2))
    plt.axhline(y=np.median(proton_density), color='g', linestyle='--', label='Median: %s' % np.round(np.median(proton_density), 2))
    plt.axhline(y=proton_density.mean() + proton_density.std(), color='b', linestyle=':', label='$\sigma$')
    plt.axhline(y=proton_density.mean() - proton_density.std(), color='b', linestyle=':') 

    plt.title('Observation Start Time: ' + str(dates[start_idx]))
    plt.ylabel('Density (cm$^{-3}$)'); plt.xlabel('Time (hours)')
    plt.legend()
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig('plots/DSCOVR-data-%s-%s.png' % (args.start, args.end))