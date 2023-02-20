# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:42:31 2022

Analyse Telemac results for water extension as measured by Max depth

@author: reds2401
"""

#%% Libraries
import os
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

#%% Files
main_folder = 'C:/Telemac_projects/'
bathy_folders = [bf for bf in os.listdir(main_folder) if 'Bathy' in bf]        # Read only bathymetry folders
bathyms = bathy_folders[0:4]

#%% Read telemac files and write them to easier csv format
result_folder = '/Results_20230215/'
write_folder = 'C:/Users/reds2401/OneDrive - USherbrooke/Research_project/Maps/QGIS_Model/Flood_results_202302/'
for bf in bathyms :
    res_folder = main_folder+bf+result_folder                                   # Results folder path
    max_filelist = [cas for cas in os.listdir(res_folder)
                    if all(x in cas for x in ['MaxDepth'])]                     # List MaxDepth files
    os.chdir(main_folder+bf+result_folder)                                      # Change directory to results folder
    maxd_df = pd.DataFrame()                                                      # Initialize maxdepth hydrograph dataframe
    # Write MaxDepth files
    for file in max_filelist:
        maxd_df = pd.read_csv(file, sep='\s+', header=None,
                            skiprows=13, names = ['X', 'Y', 'Depth'])           # Read maxdepth results file
        maxd_df['Depth'][maxd_df['Depth'] < 0] = 0                              # Make all negative and small depths to zero
        file_name = 'Dmax_'+file[9:-4]
        maxd_df.to_csv(write_folder+file_name+'.csv',index = False)             # Save dataframe to csv file
        
    # Write MinDepth files
    mind_df = pd.DataFrame()
    min_filelist = [cas for cas in os.listdir(res_folder)
                    if all(x in cas for x in ['MinDepth'])]                     # List MinDepth files
    for file in min_filelist:
        mind_df = pd.read_csv(file, sep='\s+', header=None,
                            skiprows=13, names = ['X', 'Y', 'Depth'])           # Read mindepth results file
        mind_df['Depth'][mind_df['Depth'] < 0] = 0                              # Make all negative and small depths to zero
        file_name = 'Dmin_'+file[9:-4]
        mind_df.to_csv(write_folder+file_name+'.csv',index = False)             # Save dataframe to csv file
        
    
