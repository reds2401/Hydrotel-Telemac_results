# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:29:28 2022

Read hydrotel results and generate a hydrograph of a particular event to be
used in a Telemac Unsteady state simulation

@author: reds2401
"""

# %% Libraries
import numpy as np
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta
import csv
import matplotlib.pyplot as plt

#%% Figure settings
plt.rcParams["figure.dpi"] = 150
plt.rcParams['lines.linewidth'] = 0.5
plt.rcParams['figure.figsize'] = (10,7)
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.25
plt.rcParams['grid.linestyle'] = '--'

# %% Read flow series results file from Hydrotel
os.chdir('C:/Users/reds2401/Documents/HYDROTEL/Hydrotel_030101/simulation/simulation/resultat')

csv_table = pd.read_csv('debit_aval.csv',skiprows=1, sep=';')
csv_table.rename(columns={csv_table.columns[0]:"Date"},inplace=True)

# %% Extract selected flows within dates for Boundaries for Telemac2D
# Segment 6 = Trois-Lacs outlet, Segment 3 = Trois-Lacs inlet
# Segments 41 and 5 = tributaries inlets to Trois-Lacs

# cols = ['Date','6','41','5','3',]   # With tributaries
cols = ['Date','6','3',]              # Without tributaries

nlb = len(cols)-1 # Number of liquid boundaries

hg_dates = ['1998-03-26', '2005-10-14', '2014-04-07', '2019-04-12',
            '2019-10-27', '2022-05-26']   # Starting dates for the Hydrographs

bc_fol = 'C:/Telemac_projects/'  # Folder to write results

br_df = pd.DataFrame()

# Build time column (In seconds, Telemac fromat)
bt = 172800     # Base time: the time of the Steady State simulation
t_col = np.arange(bt-10800, bt+14*86400, 10800)

for hgd in hg_dates:
    sta_dt = hgd+' 00:00'                                   # Starting datetime in format yyyy-mm-dd hh:mm
    sta_dtt = datetime.strptime(sta_dt, '%Y-%m-%d %H:%M')
    end_dtt = sta_dtt + timedelta(days=14)
    end_dt = datetime.strftime(end_dtt, '%Y-%m-%d %H:%M')   # End datetime in format yyyy-mm-dd hh:mm

    # Find indexes and extract table for dates in hydrotel table
    sta_index = csv_table[csv_table['Date']==sta_dt].index.values[0]-1
    end_index = csv_table[csv_table['Date']==end_dt].index.values[0]
    bc_table = csv_table[cols].iloc[sta_index:end_index].round(3)

    # Insert time column
    bc_table.insert(0,'T',t_col)
    bc_df = bc_table.drop('Date', axis = 1)
    bc_df['3']=bc_df['3']*-1
    br_df[hgd[:-3]] = list(bc_df['6'])

    # %% Write CSV file
    short_dt = hgd[:-3]
    bc_nam = 'HG-'+short_dt+'.txt'
    bc_dir = bc_fol + bc_nam
    with open(bc_dir, 'w', newline = '') as bc_file:
        writer = csv.writer(bc_file)
        writer.writerow(['# Liquid boundaries for hydrographs of '+short_dt])
        writer.writerow(['# '+str(nlb)+' boundaries managed'])
        writer.writerow(['# Total volume in asumed equal to total volume out'])
        writer.writerow(['#'])
        if nlb == 4:
            writer.writerow(['T	Q(1)	Q(2)	Q(3)	Q(4)'])    # With tributaries
            writer.writerow(['s	m3/s	m3/s	m3/s	m3/s'])
        else:
            writer.writerow(['T	Q(1)	Q(2)'])                        # Without tributaries
            writer.writerow(['s	m3/s	m3/s'])
    bc_df.to_csv(bc_dir, index=False, header=False, mode='a', sep='\t')

# %% Plot hydrographs
br_df.index = t_col/86400
br_df.plot(use_index=True)