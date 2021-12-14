# ACIC 2021 Visualization Web Application

Python script that produces a Streamlit web application that visualizes 3D point clouds as well as tabular data to enhance the user’s scientific investigations. Created as a group for the 2021 ACIC class. 

## Dropdown Menu:
* Allows the user to select fields of interest to render plant of choice
*	Fields are as follow:
	* Season
    * Ex) Season 10
  *	Species
    *	Ex) Lettuce
  *	Plant Number
    *	A text field that allows the user to write plant directly if they know which one they want to see
    *	Ex) Aido_10
  *	Date
    *	Ex) 2020-03-02
  *	Genotype
    *	Ex) Aido_10
  *	Treatment
    *	Ex) Treatment 1
  *	Plant Number
    *	Drop down with selections filtered with the above selections


## Point Clouds

### 3D Point Cloud:
*	Point cloud visual of the plant selected in the drop-down menus
*	Not accurate in color
*	Interactive

### Whole Field point Cloud:
*	Subsampled georeferenced point cloud of the entire field
*	Includes rendering of the individual plant point cloud in its accurate location (shown in an orange-red color
*	Interactive


## Graphs

### {Plant Number} RGB:
*	Interactive plotly line graph showing the bounding area for the plant selected in the drop downs
*	Includes a red dashed line to indicate the day being rendered

### (Plant Number} Thermal:
*	Interactive plotly line graph showing the median canopy temperature for the plant selected in the drop downs
*	Includes a red dashed line to indicate the day being rendered

### RGB:
*	Interactive plotly line graph showing the average bounding box of all plants separated by treatment for the entire season

### Thermal 
*	Interactive plotly boxplot showing the average median canopy temperature per treatment for the entire season
