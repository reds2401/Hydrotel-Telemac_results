# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:11:31 2022

Analysis of Hydrotel results:
 1. Build and plot flow-duration curves.
 2. Plot subseries of flows

@author: reds2401
"""
# %% Libraries
import numpy as np
import pandas as pd
import os
import datetime

import warnings
warnings.filterwarnings("ignore")

# %% Files

read_folder = 'C:/Users/reds2401/Documents/HYDROTEL/Hydrotel_030101/simulation/simulation/resultat/'  # Folder with Hydrotel flow result datasets
write_folder = 'C:/Users/reds2401/OneDrive - USherbrooke/Research_project/Processed_Data/'            # Folder for results file
file_name = 'debit_aval.csv'

# %% Organize data
flow_grid = pd.read_csv(read_folder + file_name, sep = ';', header = 1)   # Table with all Hydrotel flow results
flow_grid = flow_grid.rename(columns = {flow_grid.columns[0]:'Dates'})    # Change the name of the first column

segment = '6'                                                             # Segment for which to create the FDC
flow_segment = flow_grid[~flow_grid['Dates'].str.contains('1990|1991')][['Dates',segment]]  # Table with flows for the segment (Deleting first 2 years of warm up)
flow_daily = flow_segment.groupby(np.arange(len(flow_segment))//8).mean() # Calculate daily average
dates = flow_segment['Dates'][::8].str.slice(stop=10)                     # Remove hour from date
flow_daily.insert(0,'Dates',list(dates))                                  # Join tables

# %% Build Flow-Duration curve
M = len(flow_daily)                                                       # Number of data points
fdc_segment = flow_daily.sort_values(by=segment, axis = 0, ascending = False) # Arranging the table in descending order
fdc_segment['n'] = [i+1 for i in list(range(M))]                          # Assigning n value
fdc_segment['W'] = fdc_segment['n']/(M+1)                                 # Calculating Weibull's probability

fdc_segment.plot(x = 'W', y = [segment])                                  # Plotting the result

# %% Plot a portion of the series
sta_date = '2005-10-01'
end_date = '2005-10-31'

sta_index = flow_daily[flow_daily['Dates']==sta_date].index.values[0]
end_index = flow_daily[flow_daily['Dates']==end_date].index.values[0]+1

flow_subs = flow_daily.iloc[sta_index:end_index] # Flow subseries
# x_label = pd.to_datetime([i for i in flow_subs['Dates']], format = "%Y-%m-%d").strftime('%Y %m %d')


flow_subs.plot(x = 'Dates', y = [segment], rot = 90)