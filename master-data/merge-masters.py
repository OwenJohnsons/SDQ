'''
Code Purpose: 
Author: Owen A. Johnson
Date: 2023-11-24
'''
#%%
import pandas as pd 
from astropy.time import Time

# --- Load in data ---
ace_df = pd.read_csv('ACE-total-data.txt', sep=' ')
dsco_df = pd.read_csv('DSCOVR-total-data.txt', sep = ' ')

print('ACE data length: ', len(ace_df))
print('DSCOVR data length: ', len(dsco_df))

# --- Generate dates for ACE data ---
print(ace_df.keys())
ace_dates = []
ace_mjds = ace_df['MJD'].values

for mjd in ace_mjds:
    # Convert to Julian Date
    jd = mjd + 2400000.5
    # Convert to astropy Time object
    t = Time(jd, format='jd')
    # Convert to datetime object
    date = t.to_datetime()
    # Append YYYY-MM-DD HH:MM:SS to list
    ace_dates.append(date.strftime('%Y-%m-%d %H:%M:%S'))

# add dates to dataframe
ace_df['Date'] = ace_dates

# --- Merge dataframes ---
merged_df = pd.merge(ace_df, dsco_df, on='Date', how='inner')
print('Merged data length: ', len(merged_df))

# --- Save to .txt file ---
merged_df.to_csv('master-data.txt', sep=' ', index=False)

