# Written by Hayden Payne and Nik Pearce
# For PhytoOracle project and ACIC 2021 Final
# The purpose of this script is to 
# 1) read in data from specific locations in the PhytoOracle data store on Cyverse
# 2) format it into pandas dataframes, make organization edits and merge the dataframes into one
# 3) add the merged dataframe to a sqlite database
# The script returns a SQLite database file

#!/usr/bin/env python
# coding: utf-8

import sqlite3 as sql
import pandas as pd
import os
import glob
import subprocess as sp


# Create a dataframe from the rgb/thermal data csv stored on cyverse
s10 = pd.read_csv('https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_3/flirIrCamera/season10_plant_clustering/s10_flir_rgb_clustering_v4.csv')


# Get the compressed tar ball containing all the PSII data csvs from cyverse
sp.call('wget https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_2/ps2Top/ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
# Decompress the tar ball, creates a folder of csv files called fluorescence outs
sp.call('tar -xzvf ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
# Removes the compressed tar ball file
sp.call('rm ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)

# Create an empty list to contain temporary dataframes from all the PSII csv files
psII_list = []

# Creating one large data frame from all the PSII csv files in the fluorescence out folder (see above cell)
for csv in glob.glob('./fluorescence_outs/*/*.csv'):
    temp_df = pd.read_csv(csv)
    date = os.path.basename(csv).split('_')[0]
    temp_df['date'] = pd.to_datetime(date)
    psII_list.append(temp_df)
    
psII_df = pd.concat(psII_list)

# Set index to tupule of Plot and date columns in order to merge with rgb/thermal data in S10 df
psII_df = psII_df.set_index(['Plot', 'date'])

# Preparing the rgb/thermal data frame for merging

s10['date'] = pd.to_datetime(s10['date'])
# Remove all border plants because they did not undergo treatments and won't be analyzed futher
s10 = s10[s10['treatment']!='border']
# Remove all rows with 'NA' plant names or "Border" plants
s10.query('plant_name != "NA" and not plant_name.contains("Border")', inplace=True)
# Reformat names of 'Plot' column for easier merging with PSII data
s10['Plot'] = s10['plot'].str.replace('_', ' ')
# Set index to tupule of Plot and date columns in order to merge with PSII data
s10 = s10.set_index(['Plot', 'date'])

# Join the two data frames on the basis of their indices (Plot and date)
s10 = s10.join(psII_df)

# Add the merged data frame as a table in a sqlite database

# Open a connection to a new database
conn = sql.connect('test.db')

# Create a table in that database, does not need to be repeated unless the data has changed
# Comment this out after the first time you run it, otherwise you will get an error
s10.to_sql('s10_new', conn)

# Test Queries
# Query the database, in this case read the data from all columns of the s10_total table in the database (recreating the original dataframe)
test1 = pd.read_sql('SELECT * FROM s10_new WHERE Plot == "MAC Field Scanner Season 10 Range 18 Column 28"', conn)
print(test1)
test2 = pd.read_sql('SELECT * FROM s10_new WHERE plant_name == "Rex_43"', conn)
print(test2)

# Returns the whole database file
return test.db

