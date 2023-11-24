'''
Code Author: Owen A. Johnson
Date: 2023-11-20
Code Purpose: Simple script to increment through a list of links and download them without overloading querying service. Also unpacks and then deltes compressed files aftewards. 
'''
#%%
import os
from tqdm import tqdm

# --- Read .txt file in lines --- 
file = open('data-pointers.txt', 'r')
lines = file.readlines()
# find all strings with https
links = lines[0].split(' ')
print('Number of days to download: ', len(links))
for link in tqdm(links):
    os.system('wget ' + link)
print('Download complete.')

# --- Extracting .nc.gz files ---
os.system('gunzip *.nc.gz')
print('Extracting complete.')

# --- Removing .nc.gz files ---
os.system('rm *.nc.gz')