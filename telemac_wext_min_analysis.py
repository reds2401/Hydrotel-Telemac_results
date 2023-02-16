# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:42:31 2022

Analyze Telemac results for water extension as measured by Min depth

@author: reds2401
"""

#%% Libraries
import os
import pandas as pd
from shapely.geometry import Polygon, LineString, Point, MultiPoint

import warnings
warnings.filterwarnings("ignore")

#%% Files
main_folder = 'C:/Telemac_projects/'
bathy_folders = [bf for bf in os.listdir(main_folder) if 'Bathy' in bf]        # Read only bathymetry folders
bathyms = bathy_folders[0:4]

#%% Build a Dictionary results of Dataframes for each BATHYMETRY and plot them
md_res_dic = {}
result_folder = '/Results_20230215/'
write_folder = 'C:/Users/reds2401/OneDrive - USherbrooke/Research_project/Maps/QGIS_Model/Flood_results_202302/'
for bf in bathyms :
    res_folder = main_folder+bf+result_folder                                   # Results folder path
    res_filelist = [cas for cas in os.listdir(res_folder)
                    if all(x in cas for x in ['MinDepth'])]                     # List MinDepth files
    os.chdir(main_folder+bf+result_folder)                                      # Change directory to results folder
    md_hg_dic = {}                                                              # Initialize mindepth hydrograph dictionary for current bathymetry
    md_df = pd.DataFrame()                                                      # Initialize mindepth hydrograph dataframe
    for file in res_filelist:
        md_df = pd.read_csv(file, sep='\s+', header=None,
                            skiprows=13, names = ['X', 'Y', 'Depth'])           # Read mindepth results file
        md_df['Depth'][md_df['Depth'] < 0] = 0                                  # Make all negative and small depths to zero
        md_hg_dic[file[15:-4]] = md_df                                          # Store dataframe in dictionary
        #md_df_wo0 = md_df[~(md_df == 0).any(axis=1)]                           # MinDepth dataframe without zeros
        file_name = 'Dmin_'+file[9:-4]
        md_df.to_csv(write_folder+file_name+'.csv',index = False)              # Save dataframe without zeros to csv file
    md_res_dic[bf] = md_hg_dic


#%% Gemoetry analysis with Shapely
hg_list = [hgn[15:-4] for hgn in res_filelist]
ba_df = pd.DataFrame(columns=bathyms,index=hg_list)       # Bathymetry areas Dataframe initialization
bai_df = pd.DataFrame(columns=bathyms,index=hg_list)      # Bathymetry area increase Dataframe initialization
base_area = 2440881
for b in bathyms:
    for hg in hg_list:
        point_df = md_res_dic[b][hg]                                            # Read Bathymetry points dataframe
        point_df = point_df[~(point_df == 0).any(axis=1)][['X', 'Y']]  # Delete points/rows with zero depth
        bathy_mp = MultiPoint(list(point_df.to_records(index=False)))           # Create Bathymetry multipoint element
        # CONVEX HULL DOES NOT WORK TO GET THE FLOODED AREA
        bathy_bo = bathy_mp.convex_hull                                         # Create Bathymetry boundary Polygon
        bathy_ar = bathy_bo.area                                                # Extract Bathymetry surface area from boundary
        bathy_ai = 100*((bathy_ar - base_area)/base_area-1)                         # Compute Bathymetry area increase
        ba_df[b][hg] = bathy_ar                                                 # Store bathymetry area in DF
        bai_df[b][hg] = bathy_ai                                                # Store increase percentage in DF
