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

### Running Containers on Local Computer:
  
  ### Docker
  ```
  docker run -p 8501:8501 give1up1no1option/ista429final:1.0
  ```
  
  ### Singularity
  ```
  singularity run docker://give1up1no1option/ista429final:1.0
  ```
  
  Once the docker builds and runs successfully, the Web Application can be accessed using the following link:
  ```
  http://localhost:8501/
  ```
  
### Product documentation
Click [Project Documentation](https://ekene-chosen-obih.gitbook.io/acic-finals/)
