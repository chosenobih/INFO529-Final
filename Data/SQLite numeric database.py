#!/usr/bin/env python
# coding: utf-8

# In[14]:


import sqlite3 as sql
import pandas as pd
import os
import glob
import subprocess as sp


# In[45]:


# Create a dataframe from the rgb/thermal data csv stored on cyverse
s10 = pd.read_csv('https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_3/flirIrCamera/season10_plant_clustering/s10_flir_rgb_clustering_v4.csv')


# In[46]:


# Get the compressed tar ball containing all the PSII data csvs from cyverse
sp.call('wget https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_2/ps2Top/ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
# Decompress the tar ball, creates a folder of csv files called fluorescence outs
sp.call('tar -xzvf ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
# Removes the compressed tar ball file
sp.call('rm ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)


# In[47]:


psII_list = []

# Creating one large data frame from all the PSII csv files in the fluorescence out folder (see above cell)
for csv in glob.glob('./fluorescence_outs/*/*.csv'):
    temp_df = pd.read_csv(csv)
    date = os.path.basename(csv).split('_')[0]
    temp_df['date'] = pd.to_datetime(date)
    psII_list.append(temp_df)
    
psII_df = pd.concat(psII_list)
# Preparing the psII data frame for merging
psII_df = psII_df.set_index(['Plot', 'date'])


# In[48]:


psII_df


# In[49]:


# Preparing the rgb/thermal data frame for merging
s10['date'] = pd.to_datetime(s10['date'])
s10 = s10[s10['treatment']!='border']
s10.query('plant_name != "NA" and not plant_name.contains("Border")', inplace=True)
s10['Plot'] = s10['plot'].str.replace('_', ' ')
del s10['plot']
s10 = s10.set_index(['Plot', 'date'])


# In[50]:


s10 = s10.join(psII_df)


# In[51]:


s10


# In[52]:


# Open a connection to a new database
conn = sql.connect('test.db')

# Create a table in that database, does not need to be repeated unless the data has changed
s10.to_sql('s10_new', conn)


# In[69]:


# Open a connection to the database
# conn = sql.connect('test.db')

# Query the database, in this case read the data from all columns of the s10_total table in the database (recreating the original dataframe)
total = pd.read_sql("SELECT * FROM s10_new", conn)


# In[70]:


test1 = pd.read_sql('SELECT * FROM s10_new WHERE Plot == "MAC Field Scanner Season 10 Range 18 Column 28"', conn)


# In[72]:


test2 = pd.read_sql('SELECT * FROM s10_new WHERE plant_name == "Rex_43"', conn)
test2


# In[ ]:


return test.db

