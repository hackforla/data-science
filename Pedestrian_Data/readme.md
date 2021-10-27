Pedestrian Safety Analysis for Greater Wilshire Neighborhood Council
====================================================================

Can existing datasets help us identify the places in the Greater Wilshire neighborhood that would most benefit from new road safety features for pedestrians and cyclists?

## Presentation and Analysis

The latest presentation and analysis can be found on the Hack For LA shared Google Drive, under `Data Science (community of practice) > Pedestrian_Data > Report`.

## Data Sources

The analysis is based on 

- City of LA
  - Police records of [traffic accidents by date](https://data.lacity.org/Public-Safety/Traffic-Accidents-by-date/2mzm-av8t)
  - The [Neighborhood Council Boundary Shapefile](https://data.lacity.org/City-Infrastructure-Service-Requests/Neighborhood-Councils-Certified-/fu65-dz2f)

- Mapillary 
  - Database of traffic features (documented here: [Mapillary.com API Documentation](https://www.mapillary.com/developer/api-documentation))

Running the Jupyter Notebooks
-----------------------------

Mapillary has given Hack For LA access to their database, which we access through the `mapillarywrapper` module.

Before running the pedestrian safety notebooks, first request a copy of the `mapillary.cfg` file with the Hack For LA client ID, and save the cfg file to `/311-data/mapillarywrapper/mapillary.cfg` in your local repo.

With the cfg file allowing access to mapillary's API, you can run these notebooks in order:

### Notebook 1: Download Latest Data

The first notebook ([1-download-latest-data.ipynb](/Pedestrian_Data/Notebook/1-download-latest-data.ipynb)) downloads all relevant data from the City of LA and Mapillary into [a directory of raw csv files](/Pedestrian_Data/Data/1-raw-data). If those files already exist, only more recent data will be requested from City of LA and Mapillary APIs, and the existing files will be updated.

### Notebook 2: Refine Data

The next notebook ([2-refine-data.ipynb](/Pedestrian_Data/Notebook/2-refine-data.ipynb)) filters the raw data for only the relevant fields, and identifies the neighborhood councils for each GPS coordinate. These filtered and joined datasets are saved in a separate directory at [/Pedestrian_Data/Data/2-refined-data/](/Pedestrian_Data/Data/2-refined-data/). This notebook also filters these further into smaller files that perform better in QGIS, to allow for interactive exploration of the data.

### Notebook 3: Analysis

The final notebook ([3-find-interesting-info.ipynb](/Pedestrian_Data/Notebook/3-find-interesting-info.ipynb
)) crunches the numbers and generates the charts we used in our analysis.

QGIS
----

For mapping visualizations, including overlays of traffic accident data with road safety data, we used QGIS. The QGIS file is available at [/Pedestrian_Data/QGIS_Explorer/accidents-and-crosswalks.qgz](/Pedestrian_Data/QGIS_Explorer/accidents-and-crosswalks.qgz).

---

Contact Henry Kaplan with questions.
