#!/usr/bin/env python3

import streamlit as st
#from PIL import Image
import pandas as pd
import numpy as np
import subprocess
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import pydeck
import meshio
import streamlit.components.v1 as components
import open3d as o3d
from pathlib import Path
import sys
import plotly.express as px
import plotly.graph_objects as go


## ------------------------------------- RGB and Thermal Data ---------------------------------
# Checks to see if the file is already in the working directory
path_to_file = 's10_flir_rgb_clustering_v4.csv'
path = Path(path_to_file)

if path.is_file():
    print('#### CSV is already in working directory ####')
else:
    subprocess.call(f'wget https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_3/flirIrCamera/season10_plant_clustering/{path_to_file}', shell = True)

# Reads in the specified csv file
df = pd.read_csv('s10_flir_rgb_clustering_v4.csv')

#df = df[df['plant_name'].notna()]

df['date'] = pd.to_datetime(df['date'])
df['date'] = [d.date() for d in df["date"]]

df = df.sort_values(by = ['date', 'treatment', 'plant_name'])

df = df[df['treatment']!='border']

## Plant Name file (temporary fix)
path_to_file = '2020-03-02_hull_volumes.csv'
path = Path(path_to_file)

if path.is_file():
    print('#### Plant Name CSV is already in working directory ####')
else:
    subprocess.call(f'wget https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/2020-03-02/{path_to_file}', shell = True)


df_names = pd.read_csv('2020-03-02_hull_volumes.csv')

names = pd.DataFrame(df_names['plant_name'].sort_values())

#names = pd.read_csv('2020-03-02_plant_name.csv')

## ------------------------------------------ PS2 Data ----------------------------------------

## Grabs the PS2 csv files, downloads the data, uncompresses it, and concatenates it all into one file
# subprocess.call('wget https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_2/ps2Top/ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
# subprocess.call('tar -xzvf ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
# subprocess.call('rm ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)

# df_list = []

# for csv in glob.glob('./fluorescence_outs/*/*.csv'):
#     temp_df = pd.read_csv(csv)
#     date = os.path.basename(csv).split('_')[0]
#     temp_df['date'] = pd.to_datetime(date)

#     df_list.append(temp_df)
    
# PS2_df = pd.concat(df_list)

## -------------------------------------- 3D Point Cloud Data ---------------------------------
## MESHIO
def getPointsDF(plyFile):
    pcd = meshio.read(plyFile)
    points = pcd.points
    points_df = pd.DataFrame(points, columns = ['x', 'y', 'z'])
    points_df['x'] = points_df['x'] - 409000
    points_df['y'] = points_df['y'] - 3660100
    points_df['z'] = points_df['z'] - 0.00
    points_df['r'] = 34
    points_df['g'] = 139
    points_df['b'] = 34
    return points_df

## NPZ
def getPointsNpz(npz_file):
    npz = np.load(npz_file)
    points_df = pd.DataFrame(npz['points'], columns=['x', 'y', 'z', 'red', 'green', 'blue'])
    points_df['x'] = points_df['x'] - 409000
    points_df['y'] = points_df['y'] - 3660100
    points_df['z'] = points_df['z'] - 0.00

    points_df['r'] = np.int64(points_df['red'])
    points_df['g'] = np.int64(points_df['green'])
    points_df['b'] = np.int64(points_df['blue'])

    del points_df['red']
    del points_df['green']
    del points_df['blue']

    return points_df

## OPEN3D
def getPointsO3d(plyFile):
    pcd = o3d.io.read_point_cloud(plyFile)
    down_pcd = pcd.voxel_down_sample(voxel_size=0.002)
    
    points = np.asarray(down_pcd.points)
    colors = np.asarray(down_pcd.colors)
    points_df = pd.DataFrame(points, columns = ['x', 'y', 'z'])
    colors_df = pd.DataFrame(colors, columns = ['r', 'g', 'b'])

    points_df['x'] = points_df['x'] - 409000
    points_df['y'] = points_df['y'] - 3660100
    points_df['z'] = points_df['z'] - 0.00

    points_df['r'] = colors_df['r']*255
    points_df['g'] = colors_df['g']*255
    points_df['b'] = colors_df['b']*255

    return points_df

def getVis(plantIn):
        # Checks if point cloud is already in the working directory
        path_to_pcd = (f'{plantIn}.ply')
        path = Path(path_to_pcd)

        if path.is_file():
            print('#### Point Cloud is already in working directory ####')
        else:
            subprocess.call(f'wget -O {plantIn}.ply https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_1/scanner3DTop/recent_changes/2020-03-02/plantcrop/combined_pointclouds/{plantIn}/combined_multiway_registered.ply', shell=True)

        ## Loading in point cloud
        pcd_df = getPointsO3d(path_to_pcd)

        print(pcd_df)

        target = [pcd_df["x"].mean(), pcd_df["y"].mean(), pcd_df["z"].mean()]

        point_cloud_layer = pydeck.Layer(
            "PointCloudLayer",
            data=pcd_df,
            get_position=["x", "y", "z"],
            get_color=["g", "r", "b"],
            get_normal=[0, 0, 15],
            auto_highlight=True,
            pickable=True,
            point_size=0.5,
        )

        view_state = pydeck.ViewState(target=target, rotation_x=15, rotation_orbit=30, controller=True, zoom=11.0, min_zoom=3.5)
        view = pydeck.View(type="OrbitView", controller=True)

        r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view], map_provider=None)
        return r.to_html(as_string=True)

## -------------------------------------- Streamlit Visuals ----------------------------------------


#page_config sets up the title of the page (this mainly affects the
#text that appears on the browser tab as far as I know)
#icon makes the icon on the browser tab into a chart emoji
st.set_page_config(
        page_title = "ACIC Vizualization Mockup",
        page_icon = "chart_with_upwards_trend",
        layout = "wide"
    )
#st.markdown writes text onto the page
st.markdown("# ACIC Vizualization Mockup")
st.markdown('***')

#st.columns(n) creates n equally spaced columns on the page 
col1, col2 = st.columns(2)

## adds content to col2
with col2:
    st.header("PointCloud")
    #st.selectbox(x, y) creates a dropdown menue
    #x is the title for the dropdown box
    #y is the different dropdown options
    #stores selection into variable, in this case dateIn
    dateIn = st.selectbox(
        "Date",
        (df['date'].unique()))
    treatmentIn = st.selectbox(
        "Treatment",
        (df['treatment'].unique()))
    genoIn = st.selectbox(
        "Genotype",
        (df['genotype'].unique()))
    # plantIn = st.selectbox(
    #     "Plant Number",
    #     (df[df['plant_name'].str.contains(genoIn) == True]['plant_name'].sort_values().unique()))
    plantIn = st.selectbox(
        "Plant Number",
        (names[names['plant_name'].str.contains(genoIn) == True]['plant_name'].sort_values().unique()))
    
    st.markdown("### 3D Point Cloud")

    visualizationHTML = getVis(plantIn)
    components.html(visualizationHTML, height=650)

    ## ------------------------------------ Thermal Graph --------------------------------------
    st.markdown("### THERMAL")

    ## Make graph
    Thermal = sns.relplot(x='date', y='median', hue='treatment', kind='line', data=df)
    plt.xlabel('Date')
    plt.ylabel('Median (Kelvin)')
    plt.xticks(rotation=45)
    plt.tight_layout();

    st.pyplot(Thermal)

##adds content to col1
with col1:
    #writes text as header of the graph
    #st.header("Individual Plant")
    ## ------------------------- Individual Graph Bounding Area --------------------------------
    st.markdown(f"### {plantIn} Bounding Area ($m^2$)")
    
    ## Make graph
    ind_df = df[df['plant_name'] == plantIn]

    fig = px.line(ind_df, x="date", y="bounding_area_m2", title=f'{plantIn} Bounding Area (m2)', width=600, height=400)

    ## Add graph to streamlit
    st.plotly_chart(fig)

    ## ------------------------- Individual Graph Median Temp --------------------------------
    st.markdown(f"### {plantIn} Median Temperature (Kelvin)")
    
    ## Make graph
    ind_df = df[df['plant_name'] == plantIn]

    fig_temp = px.line(ind_df, x="date", y="median", title=f'{plantIn} Plant Canopy Temperature (Kelvin)', width=600, height=400)
    # fig_temp.add_trace(go.Scatter(x=['2020-02-13'], y=df.loc[df['date'] == dateIn, 'median'], mode = 'markers',
    #                      marker_symbol = 'star',
    #                      marker_size = 15))

    ## Add graph to streamlit
    st.plotly_chart(fig_temp)

    ## -------------------------------------- RGB Graph ----------------------------------------
    st.markdown('##')
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.header("Whole Field")
    st.markdown('***')

    st.markdown("### RGB")
    
    ## Make graph
    RGB = sns.relplot(x='date', y='bounding_area_m2', hue='treatment', kind='line', data=df)
    plt.xlabel('Date')
    plt.ylabel('Bounding area ($m^2$)')
    plt.xticks(rotation=45)
    plt.tight_layout();

    ## Add graph to streamlit
    st.pyplot(RGB)

    ## -------------------------------------- PS2 Graph ----------------------------------------
    #st.markdown("### PS2")
    #image = Image.open("pics/ps2GraphTemp.png")
    #st.image(image)

    # ## ------------------------------------ Thermal Graph --------------------------------------
    # st.markdown("### THERMAL")

    # ## Make graph
    # Thermal = sns.relplot(x='date', y='median', hue='treatment', kind='line', data=df)
    # plt.xlabel('Date')
    # plt.ylabel('Median (Kelvin)')
    # plt.xticks(rotation=45)
    # plt.tight_layout();

    # st.pyplot(Thermal)
## ------------------------------------------------------------------------------

subprocess.run(f'rm -r {plantIn}.ply', shell = True)


