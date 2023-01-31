# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 10:41:16 2022

Analyze Telemac results of water levels hydrographs

@author: reds2401
"""

#%% Libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

#%% Figure settings
plt.rcParams["figure.dpi"] = 150
plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['figure.figsize'] = (10,7)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.25
plt.rcParams['grid.linestyle'] = '--'

#%% Files
main_folder = 'C:/Telemac_projects/'
bathy_folders = [bf for bf in os.listdir(main_folder) if 'Bathy' in bf]        # Read only bathymetry folders
bathy_folders = bathy_folders[0:4]

#%% Build a Dictionary results of Dataframes for each BATHYMETRY and plot them
ws_res_dic = {}
result_folder = '/Results_20221111/'
for bf in bathy_folders :
    res_folder = main_folder+bf+result_folder
    res_filelist = [cas for cas in os.listdir(res_folder)
                    if all(x in cas for x in ['FreeSurface'])]                 # List FreeSurface files
    os.chdir(main_folder+bf+result_folder)
    res_df = pd.DataFrame()
    for file in res_filelist:
        res_df[file[18:-4]] = pd.read_csv(file).iloc[1::,2]                    # Read only the second column of each results file
    res_df = res_df.apply(pd.to_numeric, errors='coerce')
    t_c = np.round(np.arange(0,len(res_df)/96,1/96), 3)
    res_df.index = t_c
    res_df.plot(y=list(res_df.columns), use_index = True, title = bf)
    plt.show()
    ws_res_dic[bf] = res_df                                                    # Assign the Dataframe to the dictionary

#%% Build a Dictionary results of Dataframes for each HYDROGRAPH and plot them
hg_res_dic = {}
hydrographs = ws_res_dic[bathy_folders[0]].columns
hg_max = pd.DataFrame(columns=bathy_folders,index=hydrographs)
hg_ini = pd.DataFrame(columns=bathy_folders,index=hydrographs)
hg_min = pd.DataFrame(columns=bathy_folders,index=hydrographs)

hg_st_dates = {'HG1998-03': datetime.datetime(1998,3,26),
               'HG2005-10': datetime.datetime(2005,10,14),
               'HG2014-04': datetime.datetime(2014,4,7),
               'HG2019-04': datetime.datetime(2019,4,12),
               'HG2019-10': datetime.datetime(2019,10,27),
               'HG2022-05': datetime.datetime(2022,5,26),}

for hg in hydrographs :
    hg_df = pd.DataFrame()
    for b in bathy_folders:
        hg_df[b] = ws_res_dic[b][hg]                                           # Read hydrograph column for each bathymetry
        hg_max[b][hg] = hg_df[b].max()
        hg_min[b][hg] = hg_df[b].min()
        hg_ini[b][hg] = hg_df[b][0]

    start_date = hg_st_dates[hg] # Start date
    time_interval = datetime.timedelta(minutes=15) # Time interval between each date
    num_dates = len(hg_df)
    dates = [start_date + time_interval*i for i in range(num_dates)]

    hg_df.index = dates
    hg_res_dic[hg] = hg_df                                                     # Assign the Dataframe to the dictionary
    print(hg, '\n', hg_df.max())

# %% MultiPlot each Hydrograph for all bathymetries

plt.rcParams['figure.figsize'] = (12,4)

fig, axs = plt.subplots(2, 3, sharex = False, sharey = True, constrained_layout = False)

for hg, ax in zip(hydrographs, axs.ravel()):
    hg_res_dic[hg].plot(ax=ax, legend=False)
    ax.set_title(hg, y=1.0, pad=-12)


handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4)
plt.subplots_adjust(top=1.8, bottom=0.22,wspace=0.1)

axs[0][0].set_ylabel('Water level (masl)', fontsize=12)
axs[1][0].set_ylabel('Water level (masl)', fontsize=12)

plt.show()