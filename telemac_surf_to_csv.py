# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:42:31 2022

Convert Telemac surface results for Max depth, Min Depth, and Max Vel to .csv
files that can be read in QGIS.

@author: reds2401
"""

#%% Libraries
import os
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

#%% Files
t_folder = 'C:/Telemac_projects/'                                              # Folder containing telemac projects 
bathy_folders = [bf for bf in os.listdir(t_folder) if 'Bathy' in bf]           # Read only bathymetry folders
bathyms = bathy_folders[0:4]

result_folder = '/Results_20230215/'
write_folder = 'C:/Users/reds2401/OneDrive - USherbrooke/Research_project/Maps/QGIS_Model/Flood_results_202302/'

# %% Function
def telemac2csv(r_var, w_var, r_fold, w_fold, par):
    """
    Function to read specific .xyz Telemac2D files and write them to csv.
    Works for maximum and minimum depth and maximum velocity.
    
    Parameters
    ----------
    r_var : string
        Name of files for a specific variable to read.
    w_var : string
        String for the name of the files to write.
    r_fold : string
        Directory to read the result files.
    w_fold : string
        Directory to write the files
    par : string
        Parameter to read from the results file.

    Returns
    -------
    None.
    """
    filelist = [cas for cas in os.listdir(r_fold)
                    if all(x in cas for x in [r_var])]                       # List Specific variable files
    for file in filelist:
        var_df = pd.read_csv(file, sep='\s+', header=None,
                            skiprows=13, names = ['X', 'Y', par])            # Read results file
        var_df[par][var_df[par] < 0.0001] = 0                                # Make all negative and small values to zero
        file_name = w_var+file.replace(r_var,'')[:-4]+'.csv'
        var_df.to_csv(w_fold+file_name,index = False)                        # Save dataframe to csv file

#%% Read telemac files and write them to csv format easier to read in QGIS

for bf in bathyms :
    res_dir = t_folder+bf+result_folder                                      # Results folder path
    os.chdir(res_dir)                                                        # Change directory to results folder
    
    #%% Write MaxDepth files
    telemac2csv('MaxDepth', 'Dmax', res_dir, write_folder, 'Depth')
    
    #%% Write MinDepth files
    telemac2csv('MinDepth', 'Dmin', res_dir, write_folder, 'Depth')
    
    #%% Write MaxVel files
    telemac2csv('MaxVel', 'Vmax', res_dir, write_folder, 'Velocity')

