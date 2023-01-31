# -*- coding: utf-8 -*-
"""
Created on March 9 10:48:29 2022

Analysis of measured water levels against simulated flows for the Trois-lacs
exit point, to extract points to build a rating curve

@author: reds2401
"""

# %% Libraries
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# %% Files

folder = '../Processed_data/'
file_name = 'TroisLacs_Flow_WS_2022.csv'
ws_file = pd.read_csv(folder + file_name, sep=';').dropna(axis=0)  # Read water stage file
ws_file['WS_round'] = ws_file['WS'].round(2)
ws_counts = ws_file['WS_round'].value_counts()
ws_selec = ws_counts[ws_counts>6]
ws_calc = ws_file[ws_file['WS_round'].isin(ws_selec.index)]

# %% Create Probability distribution figure for each WS value
ws_dict = {}                                                        # Initialize Water stage dictionary
ws_list = []                                                        # Initialize Water stage list
i = 0
for ws in ws_calc['WS_round'].unique():
    plt.figure(dpi = 150)
    ws_n = str(ws)
    plt.title(ws_n)
    ws_i = ws_calc[ws_calc['WS_round']==ws]                         # Get all instances of each WS value
    ws_dict[ws_n] = ws_i['Q_out'].plot.kde().get_lines()[0].get_xydata()    # Plot KDE figure
    ws_mlv = np.extract(ws_dict[ws_n][:,1] == max(ws_dict[ws_n][:,1]), ws_dict[ws_n][:,0])[0]   # Get most likely value
    ws_list.append(ws_mpl)
ws_df = pd.DataFrame([ws_calc['WS_round'].unique(),ws_list]).T      # Assign values to WS-flow dataframe
ws_df.columns=['WS', 'Q']
ws_df.to_csv('WS-Q_measured_points(for_RC).csv',index=False)        # Write the file for weir rating curve calculations

# %% Violin plot for the complete set of WS

# Figure setup
plt.figure(dpi = 150)
plt.rc('font', size=4)
fs = 5  # fontsize
pos = list(np.float_(sorted(ws_dict)))
ws_data = []

# Building figure
for k in pos:
    ws_data.append(ws_calc['Q_out'].loc[ws_calc['WS_round']==k])
data = [np.random.normal(0, std, size=100) for std in pos]
x_pos = [str(pos[i]) for i in list(range(len(ws_data)))]                        # Without points count
# x_pos = [str(pos[i])+'\n'+str(len(ws_data[i])) for i in list(range(len(ws_data)))] # With points count
ws_vplot = plt.violinplot(ws_data, pos, points=100, widths=0.04,
                     showmeans=False, showextrema=False, showmedians=True)
plt.ylabel('Flow ($m^3/s$)')
plt.xlabel('Water stage ($masl$)')
plt.title('Flows  distribution for water levels at Trois-Lacs outlet for 2022')
plt.xticks(pos, x_pos, rotation = 90)
plt.grid(visible=True, linestyle='--', linewidth=0.5)
for pc in ws_vplot['bodies']:
    pc.set_alpha(0.5)
    pc.set_edgecolor('black')