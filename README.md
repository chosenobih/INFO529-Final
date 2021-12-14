# BE/INFO/ISTA/PLS/ 429/529 FALL 2021 FINAL PROJECT

-This repository contains the files for the final project of the above mentioned class.

## About

### Project description
This is a visualization/database mini project for the PhytoOracle research team.PhytoOracle is a series of distributed data processing pipelines which take raw 2D image and 3D point cloud data and extract phenotypic trait data. These data is useful to researchers because it allows for:
Identification of top performing crop genotypes, assessment of phenotypic variations due to genotype variations and evaluatiion of how environment will influence crop yield

### Project goal
The main goal of this project is to develop a VR/web-based point cloud environment that enables the following: Visualization of a set of individual plants point cloud data, visualization of phenotypic data in an interactive manner, time series visualization of individual plants in the data.

### Plan
The class was divided into functional groups with graduate students serving  as team lead. The functional groups include:
  - Data wranglers
  - Data visualization
  - Cyberinfrastructure
  - Evangelizers/Documentation

### Running Containers:
  - git clone <> ( cloing the githiub repo)
  - cd /containes
  - $make (This will build the image for you)
  - $docker run -p 8501:8501 final (This will run the image final)
  - http://localhost:8501/ (Link to view the running script)
  
  Additional: $docker pull give1up1no1option/ista429final:1.0 (pull the container from docker hub)
### Product documentation
Click [final documentation](https://jordane.gitbook.io/user-manual/)
