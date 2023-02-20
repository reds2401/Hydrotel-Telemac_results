# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 08:40:31 2023

Analyse Telemac results for water extension as measured by Max depth

@author: reds2401
"""

# %% Libraries
import os
import pandas as pd
import geopandas as gpd

import warnings
warnings.filterwarnings("ignore")

# %% Read files
main_f = 'C:/Users/reds2401/OneDrive - USherbrooke/Research_project/Maps/QGIS_Model/Flood_results_202302/'
max_shp_files = [sf for sf in os.listdir(main_f) if ('WEmax' in sf) and ('.shp' in sf)]     # List max extension area shapefiles
min_shp_files = [sf for sf in os.listdir(main_f) if ('WEmin' in sf) and ('.shp' in sf)]     # List min extension area shapefiles

# %% Get area from the Max ext shapefiles
cols = ['HG1998-03','HG2005-10','HG2014-04','HG2019-04','HG2019-10','HG2022-05']
rows = ['B1975','B2004','B2019','B2020']
max_area_df = pd.DataFrame(columns=cols, index=rows)
for sh in max_shp_files:
    max_wext = gpd.read_file(main_f+sh)
    max_area_df[sh[12:21]][sh[6:11]] = float(max_wext.area)

# %% Get area from the min ext shapefiles
min_area_df = pd.DataFrame(columns=cols, index=rows)
for sh in min_shp_files:
    min_wext = gpd.read_file(main_f+sh)
    min_area_df[sh[12:21]][sh[6:11]] = float(min_wext.area)