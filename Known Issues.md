# Known Issues

### Containerization
- the post-containerization deployment is not fully working on VICE. Trying to run the application seems to bottleneck around 75% and quit on itself after a long runtime. So essentially the container application has not been able to run on the VICE DE at this current moment. It seems that there may be some networking issues that need to be resolved.

### Database and Accessing Data
- The SQLite database is not integrated with UI Team’s Streamlit application.
- The database likely needs some more testing/debugging to ensure that the public Cyverse links were properly added, plus data summaries/statistics from the database could be added to the dashboard. 
- A slight tweaking of the scraping functions of the script would allow addition of links to point cloud data as well as new numeric/phenotypic data from other seasons to the database. Quality check on any new data inputs would be necessary.

### User Interface
- Non-functioning dropdown menus: The season, species, and date columns are non-functioning and provide no input into the specific point cloud that is being retrieved from Cyverse.
  - Season and Lettuce are hard-coded
  - Date reads unique values from the RGB and thermal phenotypic trait data

- Accurate dates, but it is not used to populate the downstream dropdown menus (i.e., no logic attached to the values)
  - This also encompasses the treatment check boxes (they are not currently being used to filter the data)

- No Time Series Component: Due to the non-functional date dropdown, we are not able to retrieve multiple point clouds of the same plant for different days
  - All of the point clouds that we are currently visualizing are for 2020-03-02 only
  - Not having these point clouds has led to not having the time series component in the web application

- Plant Number Populated by .csv File: Due to the fact that we were only visualizing 2020-03-02 data, the current solution to populate the plant number dropdown is to look at the 2020-03-02_hull_volumes.csv
  - This is a temporary fix
  - Was the only way we could assure that all of the choices in the plant number dropdown had a point cloud associated with them

- No Statistics About the Quality of the Data: One of the initial goals was to have stats related to the information in the database on the web application
  - Stats would have included
    - Number of plants captured that day
    - Number of plots with no URL
    - Number of rows with NaN values. Etc.
  - Once the database is implemented, these should be simple to visualize on the web app

- Lack of functioning database: The database was to be created using two different scripts (the scraping script and the data cleaning/concatenating script)
  - The scraping script allows the user to scrape all of the existing information from cyverse which includes:
    - Dates available
    - Plants scanned on those dates
    - URLs associated
- The second script was to create a SQLite database that took the information from the scraping script and populated the database with the corresponding phenotypic trait data
- Would give the visualization script one database to use to populate the dropdowns, grab the URLs and generate the plots
- Allows for a dynamic database with accurate information
    - Database scripts are in place, but they were not merged
- There seems to be an issue with the SQLite script accurately populating the information associated to the info generated from scraping

- PS2 Graph Details: Current PS2 graph included is only the season level graph
  - This graph does not include treatments
  - The only PS2 data available did not have treatment information
  - The goal was also to include a plot level PS2 graph in the individual plant section of the web app

    Same problem arose before with the lack of information in the current csv we are retrieving 

- Inconsistencies in Graphs: RGB and thermal individual graphs show some strange trends (sudden drop offs in the middle of the season) for certain plants
  - At first, we thought it was due to the sorting of the dataframe we were using to populate the plotly graphs
  - That did not solve the issue
  - We currently think it has to do with plotly itself (maybe exploration into other graphical libraries might be a good idea)

- Issues with URLs produced by Streamlit: Streamlit produces URLs that the user can click on to project their visualization on the web
  - These links work great when the script was run locally
  - Once containerized, the URLs (both network URL and external URL) would not load the application
  - The only way to get around it was to visit the 
  - Link (this would show the application)
  - This happened on both Singularity and Docker when Sebastian tested it out
  - The strange thing is that when Emmanuel tested it out, they worked fine on Singularity
  - Something to note is that Sebastian could only get singularity on his local computer by installing it via a VM
  - It might be a permission error (potentially the same one that Team CI was running into with VICE)
