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
import matplotlib as plt

import warnings
warnings.filterwarnings("ignore")

# Figure settings
plt.rcParams["figure.dpi"] = 150
plt.rcParams["grid.linestyle"] = '--'


# %% Files

read_folder = 'C:/Users/reds2401/Documents/HYDROTEL/Hydrotel_030101/simulation/simulation/resultat/'  # Folder with Hydrotel flow result datasets
write_folder = 'C:/Users/reds2401/OneDrive - USherbrooke/Research_project/Processed_Data/'            # Folder for results file
file_name = 'debit_aval.csv'

# %% Organize data
flow_grid = pd.read_csv(read_folder + file_name, sep = ';', header = 1)   # Table with all Hydrotel flow results
flow_grid = flow_grid.rename(columns = {flow_grid.columns[0]:'Dates'})    # Change the name of the first column

segment = '6'                                                             # Segment for which to create the FDC
flow_segment = flow_grid[~flow_grid['Dates'].str.contains('1990|1991')][['Dates',segment]]  # Table with 3h flows for the segment (Deleting first 2 years of warm up)
flow_daily = flow_segment.groupby(np.arange(len(flow_segment))//8).mean() # Calculate daily average
dates = flow_segment['Dates'][::8].str.slice(stop=10)                     # Remove hour from date
flow_daily.insert(0,'Dates',list(dates))                                  # Join tables

# %% Daily max values
flow_daymx = flow_segment.groupby(np.arange(len(flow_segment))//8).max()  # Calculate daily average
flow_daymx = flow_daymx.set_index('Dates')                                # Set dates as the index
flow_daymx.index = pd.to_datetime(flow_daymx.index)
flow_daymx['Year'] = flow_daymx.index.year                                # Get year values as a columns
flow_max_an = flow_daymx.groupby('Year')[segment].max()

# %% Build Mean Daily Flow-Duration curve
M = len(flow_daily)                                                       # Number of data points
fdc_seg_dy = flow_daily.sort_values(by=segment, axis = 0, ascending = False) # Arranging the table in descending order
fdc_seg_dy['n'] = [i+1 for i in list(range(M))]                          # Assigning n value
fdc_seg_dy['W'] = 100*fdc_seg_dy['n']/(M+1)                             # Calculating Weibull's exceedance probability

# Plotting the result
fdc_seg_dy.plot(x = 'W', y = [segment], xlabel='Exceedance probability', grid=True,
                  ylabel='Flow($m^3/s$)',legend=False, title='Daily Flow-Duration Curve')

# %% Build 3 hour Flow-Duration curve
N = len(flow_segment)                                                       # Number of data points
fdc_seg_3h = flow_segment.sort_values(by=segment, axis = 0, ascending = False) # Arranging the table in descending order
fdc_seg_3h['n'] = [i+1 for i in list(range(N))]                          # Assigning n value
fdc_seg_3h['W'] = 100*fdc_seg_3h['n']/(N+1)                             # Calculating Weibull's exceedance probability

# Plotting the result
fdc_seg_3h.plot(x = 'W', y = [segment], xlabel='Exceedance probability (%)', grid=True,
                  ylabel='Flow($m^3/s$)',legend=False, color='k')

# Format the plot to add a blue zone between the 20 and 80 x marks
plt.pyplot.axvline(x=20, color='k', linestyle='--')
plt.pyplot.axvline(x=80, color='k', linestyle='--')
plt.pyplot.axvspan(20, 80, alpha=0.8, color='lightblue')
plt.pyplot.text(50, 0.5*max(fdc_seg_3h[segment]), 'Regular flows', horizontalalignment='center', fontsize=12)
plt.pyplot.text(20, fdc_seg_3h.loc[fdc_seg_3h['W'] == 20, segment].iloc[0], fdc_seg_3h.loc[fdc_seg_3h['W'] == 20, segment].iloc[0],
                horizontalalignment='right', verticalalignment='center', color='b', fontsize=10)
plt.pyplot.text(80, fdc_seg_3h.loc[fdc_seg_3h['W'] == 80, segment].iloc[0], fdc_seg_3h.loc[fdc_seg_3h['W'] == 80, segment].iloc[0],
                horizontalalignment='left', verticalalignment='center', color='b', fontsize=10)

# %% Plot a portion of the series
sta_date = '2005-10-01'
end_date = '2005-10-31'

sta_index = flow_daily[flow_daily['Dates']==sta_date].index.values[0]
end_index = flow_daily[flow_daily['Dates']==end_date].index.values[0]+1

flow_subs = flow_daily.iloc[sta_index:end_index] # Flow subseries

flow_subs.plot(x = 'Dates', y = [segment], rot = 90, legend=False, grid=True,
               ylabel = 'Flow($m^3/s$)', title = 'Subset of average daily flows')