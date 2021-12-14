#!/usr/bin/env python3

import streamlit as st
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
import os


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

## ------------------------------------------ PS2 Data ----------------------------------------


## Grabs the PS2 csv files, downloads the data, uncompresses it, and concatenates it all into one file
path_to_file = 'fluorescence_out.csv'
path = Path(path_to_file)

if path.is_file():
    print('#### Fluorescence CSV is already in working directory ####')
else:
    subprocess.call(f'wget https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_2/ps2Top/ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
    subprocess.call(f'tar -xzvf ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)
    subprocess.call(f'rm ps2Top-fluorescence_aggregation_S10.tar.gz', shell=True)

    df_list = []

    for csv in glob.glob('./fluorescence_outs/*/*.csv'):
        fluor_df = pd.read_csv(csv)
        date = os.path.basename(csv).split('_')[0]
        fluor_df['date'] = pd.to_datetime(date)

        df_list.append(fluor_df)
    
    PS2_df = pd.concat(df_list)

    PS2_df.to_csv('fluorescence_out.csv')

PS2_df = pd.read_csv('fluorescence_out.csv')

subprocess.call('rm -r fluorescence_outs', shell=True)

## -------------------------------------- 3D Point Cloud Data ---------------------------------
## Preps PLY Point Cloud using MESHIO
def getPointsDF(plyFile):
    pcd = meshio.read(plyFile)
    points = pcd.points
    points_df = pd.DataFrame(points, columns = ['x', 'y', 'z'])
    # Shifts coordinates to a more manageable range
    points_df['x'] = points_df['x'] - 409000
    points_df['y'] = points_df['y'] - 3660100
    points_df['z'] = points_df['z'] - 0.00
    # Sets arbitrary RGB values to make the point cloud green
    points_df['r'] = 34
    points_df['g'] = 139
    points_df['b'] = 34
    return points_df

## Preps NPZ Point Clouds
def getPointsNpz(npz_file):
    npz = np.load(npz_file)
    points_df = pd.DataFrame(npz['points'], columns=['x', 'y', 'z', 'red', 'green', 'blue'])
    # Shifts coordinates to a more manageable range
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

## Preps PLY Point Clouds using Open3d
def getPointsO3d(plyFile):
    pcd = o3d.io.read_point_cloud(plyFile)
    down_pcd = pcd.voxel_down_sample(voxel_size=0.002)
    
    points = np.asarray(down_pcd.points)
    colors = np.asarray(down_pcd.colors)
    points_df = pd.DataFrame(points, columns = ['x', 'y', 'z'])
    colors_df = pd.DataFrame(colors, columns = ['r', 'g', 'b'])

    # Shifts coordinates to a more manageable range
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

        target = [pcd_df["x"].mean(), pcd_df["y"].mean(), pcd_df["z"].mean()]

        ## Sets poing cloud layer details (note the RGB ordering was switched to get a green point cloud)
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

        ## Sets view settings
        view_state = pydeck.ViewState(target=target, rotation_x=15, rotation_orbit=30, controller=True, zoom=11.0, min_zoom=3.5)
        view = pydeck.View(type="OrbitView", controller=True)

        ## Converts the point cloud layer into html
        r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view], map_provider=None)
        return r.to_html(as_string=True)

## -------------------------------------- Streamlit Visuals ----------------------------------------


#page_config sets up the title of the page (this mainly affects the
#text that appears on the browser tab as far as I know)
#icon makes the icon on the browser tab into a chart emoji
st.set_page_config(
        page_title = "ACIC Visualization Mockup",
        page_icon = "chart_with_upwards_trend",
        layout = "wide"
    )

# Markdowns for navigation bar
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <a class="navbar-brand" href="" target="_blank">ACIC Visualization</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://jordane.gitbook.io/user-manual/" target="_blank">Documentation</a> 
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

#dropdown menues for season10 (currently the only season we have to implement)
#returns a string indicating the plant that should be implemented 
def season10_menu():
    plantIn = ""
    speciesIn = st.sidebar.selectbox(
        "Species",
        ("Lettuce", ""))
    #nameIn = st.sidebar.text_input("Plant Number")
    #displays full dropdown menu if no name has been entered
    #if(nameIn == ""):
    dateIn = st.sidebar.selectbox(
        "Date",
        (df['date'].unique()))
    genoIn = st.sidebar.selectbox(
        "Genotype",
        (df['genotype'].unique()))
    st.sidebar.write('Select Treatment(s)')
    treat1 = st.sidebar.checkbox('Treatment 1')
    treat2 = st.sidebar.checkbox('Treatment 2')
    treat3 = st.sidebar.checkbox('Treatment 3')
    #[TO-DO] update the conditions for the options that appear
    #for the plant number dropdown to include new input widgets
    plantIn = st.sidebar.selectbox(
    "Plant Number",
    (names[names['plant_name'].str.contains(genoIn) == True]['plant_name'].sort_values().unique()))
    #if a plant name has been entered, displays only the dates for that plant
    # else:
    #     #[TO-DO] Need to connect the options of this dropdown to
    #     #nameIn from the textbox. Currently it's still displaying
    #     #the same dates as the main dropdown
    #     dateIn = st.selectbox(
    #     "Date",
    #     (df['date'].unique()))
    #     plantIn = nameIn
    
    return plantIn, dateIn
#st.markdown writes text onto the page
st.markdown("# ACIC Visualization Mockup")
st.markdown('***')

st.markdown(f"## Individual Plant Level Data")
#st.columns(n) creates n equally spaced columns on the page 
col1, col2 = st.columns(2)

with col1:
    st.header("3D PointCloud")
    plantIn = ""
    seasonIn = st.sidebar.selectbox(
        "Seasons",
        ("Season 10", ""))
    if(seasonIn == "Season 10"):
        plantIn, dateIn = season10_menu()
    else:
        st.markdown("Other Seasons Not Implemented")

    visualizationHTML = getVis(plantIn)
    components.html(visualizationHTML, height=850)

  ## ------------------------------------------------------------------------------------

##adds content to col2
with col2:
    #writes text as header of the graph
    #st.header("Individual Plant")
    ## ------------------------- Individual Graph Bounding Area --------------------------------
    st.markdown('')
    st.markdown(f"### {plantIn} RGB")
    
    ## Make graph
    ind_df = df[df['plant_name'] == plantIn]

    fig = px.line(ind_df, x="date", y="bounding_area_m2", title=f'{plantIn} Bounding Area (m2)', width=600, height=400)
    fig.add_vline(x = pd.to_datetime(f'{dateIn}'), line_dash="dash", line_color="red")

    ## Add graph to streamlit
    st.plotly_chart(fig, use_column_width=True)

    ## ------------------------- Individual Graph Median Temp --------------------------------
    st.markdown(f"### {plantIn} Thermal")
    
    ## Make graph
    ind_df = df[df['plant_name'] == plantIn]

    fig_temp = px.line(ind_df, x="date", y="median", title=f'{plantIn} Plant Canopy Temperature (Kelvin)', width=600, height=400)
    fig_temp.add_vline(x = pd.to_datetime(f'{dateIn}'), line_dash="dash", line_color="red")

    ## Add graph to streamlit
    st.plotly_chart(fig_temp, use_column_width=True)

## New Columns
st.markdown(f"## Season Level Data")

col1, col2, col3 = st.columns(3)

with col1:
    ## -------------------------------------- RGB Graph ----------------------------------------
    st.markdown("### RGB")

    ## Plotly Graph
    mean = df.groupby(['date', 'treatment']).mean().reset_index()

    fig = px.line(mean, x = "date", y = 'bounding_area_m2', color = 'treatment', width=550, height=400)

    st.plotly_chart(fig, use_column_width=True)

with col2:
    ## -------------------------------------- PS2 Graph ----------------------------------------
    st.markdown("### PS2")
    
    ## Plotly Graph
    fig_fluor = px.box(PS2_df, x = "date", y = 'FV/FM', width=600, height=400)

    st.plotly_chart(fig_fluor, use_column_width=True)

    ## ------------------------------------ Thermal Graph --------------------------------------
with col3:

    st.markdown("### THERMAL")

    ## Plotly Graph
    mean = df.groupby(['date', 'treatment']).mean().reset_index()
    
    fig_temp = px.box(mean, x = "treatment", y = 'median', color = 'treatment', width=600, height=400)

    st.plotly_chart(fig_temp, use_column_width=True)

## ------------------------------------ Field Point Cloud -----------------------------------
## Full-field Point Cloud
col1 = st.columns(1)

## Downloads subsampled point cloud
path_to_file = 'Lettuce_Reduced_4.ply'
path = Path(path_to_file)

if path.is_file():
    print('#### Field Point Cloud is already in working directory ####')
else:
    subprocess.call(f'wget https://data.cyverse.org/dav-anon/iplant/projects/phytooracle/season_10_lettuce_yr_2020/level_0/drone/RGB/point_clouds/{path_to_file}', shell = True)


pcd = o3d.io.read_point_cloud('Lettuce_Reduced_4.ply')

points = np.asarray(pcd.points)
colors = np.asarray(pcd.colors)
points_df = pd.DataFrame(points, columns = ['x', 'y', 'z'])
colors_df = pd.DataFrame(colors, columns = ['r', 'g', 'b'])

# Shifts coordinates to a more manageable range
points_df['x'] = points_df['x'] - 409000.00
points_df['y'] = points_df['y'] - 3660100.00
points_df['z'] = points_df['z'] - 361.00

points_df['r'] = colors_df['r']*255
points_df['g'] = colors_df['g']*255
points_df['b'] = colors_df['b']*255

pcd_df = getPointsO3d(f'{plantIn}.ply')
concat_df = pd.concat([points_df, pcd_df])

#target = [concat_df["x"].mean(), concat_df["y"].mean(), concat_df["z"].mean()]

target = [pcd_df["x"].mean(), pcd_df["y"].mean(), pcd_df["z"].mean()]

point_cloud_layer = pydeck.Layer(
    "PointCloudLayer",
    data=concat_df,
    get_position=["x", "y", "z"],
    get_color=["r", "g", "b"],
    get_normal=[0, 0, 15],
    auto_highlight=True,
    pickable=True,
    point_size=1.0,
)

## Sets view settings
view_state = pydeck.ViewState(target=target, rotation_x=90, rotation_orbit=90, controller=True, zoom=11.0, min_zoom=1.0)
view = pydeck.View(type="OrbitView", controller=True)

## Converts the point cloud layer into html
r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view], map_provider=None)
components.html(r.to_html(as_string=True), height=500)


## ------------------------------------------------------------------------------

## Deletes the point cloud file that was downloaded after each selection has been visualized
subprocess.run(f'rm -r {plantIn}.ply', shell = True)