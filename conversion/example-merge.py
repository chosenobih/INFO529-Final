#%%
#
# M E R G E  E X A M P L E
#


import pandas as pd
#import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
import os
import argparse
import sys
import glob
import subprocess as sp

parser = argparse.ArgumentParser("Merge example")

parser.add_argument('-r', '--rgb', action="store", required=True, help="Flir RGB file")
parser.add_argument('-f', '--fluorescence', action="store", required=True, help="Fluorescence tarball")
parser.add_argument('-o', '--output', action="store", required=True, help="Output file for merge frame")
arguments = parser.parse_args()

WGET    = 'wget '
TAR     = 'tar '
TAROPTS = ' -xvzf '
RM      = 'rm '

#df = pd.read_csv('https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_3/flirIrCamera/season10_plant_clustering/s10_flir_rgb_clustering_v4.csv')
# Read in the file from the host
try:
    df = pd.read_csv(arguments.rgb)
# This is not the correct way to do this.  Handle specific errors
except BaseException as e:
    print("Error encountered reading FLIR file: {}".format(e))
    sys.exit(1)

#%%

df['date'] = pd.to_datetime(df['date'])
df = df[df['treatment']!='border']

# Thermal
# sns.relplot(
#     x='date',
#     y='median',
#     hue='treatment',
#     kind='line',
#     data=df
# )
# plt.xlabel('Date')
# plt.ylabel('Median (Kelvin)')
# plt.xticks(rotation=45);

# Individual Plant
df['plant_name'].unique()
# sns.relplot(
#     x='date',
#     y='bounding_area_m2',
#     kind='line',
#     data=df[df['plant_name']=='Passport_82']
# )
# plt.xticks(rotation=45);

# PS2

# sp.call('iget -KPVT /iplant/home/shared/phytooracle/season_10_lettuce_yr_2020/level_2/ps2Top/ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
tarballURL = arguments.fluorescence
# This gets the last component (after the last /)
tarball = tarballURL.rsplit('/',1)[-1]

try:
    # Check the return code after each call
    rc = sp.call(WGET + tarballURL, shell=True)
    if rc == 0:
        rc = sp.call(TAR + TAROPTS + tarball, shell=True)
    if rc == 0:
        rc = sp.call(RM + tarball, shell=True)
    if rc != 0:
        sys.exit(1)
except BaseException as e:
    print("Error encountered: {}".format(e))
    sys.exit(1)


#%%

df_list = []

for csv in glob.glob('./fluorescence_outs/*/*.csv'):
    temp_df = pd.read_csv(csv)
    date = os.path.basename(csv).split('_')[0]
    temp_df['date'] = pd.to_datetime(date)

    df_list.append(temp_df)

final_df = pd.concat(df_list)

#%%

df['plot'] = df['plot'].str.replace('_', ' ')

#%%

df = df.set_index(['plot', 'date'])

#%%

df.index[0]

#%%

final_df = final_df.set_index(['Plot', 'date'])

#%%

final_df.index[0]

#%%

df.join(final_df)

#%%

df.to_csv(arguments.output)

sys.exit(0)

#%%
