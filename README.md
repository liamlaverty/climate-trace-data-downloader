# (Unofficial) Climate Trace Data Downloader 

Downloads & unzips all inventory datasets from the ClimateTrace repository: https://climatetrace.org/

Companion app to https://github.com/liamlaverty/climate-trace-data-importer


## Copyright Note 

This repository uses the MIT License. The emissions inventory downloaded from ClimateTrace have different licenses, see https://climatetrace.org/faq for details


## What Does It Do?

* Downloads national ClimateTrace inventories for each country, for the categories:
  * Forest Sector
  * Non-Forest Sector
* Downloads international CliamteTrace inventories for the categories:
  * Agriculture
  * Buildings
  * Forestry and land use
  * Fossil Fuel Operations
  * Manufacturing
  * Power
  * Transportation
  * Waste
* Unzips the downloaded data

Once the download & unzipping are complete, a directory containing the following structure will be created, containing CSVs of inventories
```
~/data_packages/climate_trace/
 -> /country_packages/
   -> /forest_sectors/
     -> /ABW/
     -> /AFG/
     -> /AGO/
   -> /non_forest_sectors/
     -> /ABW/
     -> /AFG/
     -> /AGO/
 -> /sector_packages/
   -> /agriculture/
   -> /buildings/
   -> /plus /
```

## Usage
* in the project's main directory, run `python .\climate-trace.py`

### Optional Params

* `-o`, `--outputPath`               
  * The output path. 
  * If not specified, the current working directory will be used
  * Usage: `python .\climate-trace.py -o'C:\_example_data_files\example_directory'`

* `--skipDownloadSectors`           
  * Boolean value, defaults to `False`. 
  * When set, skips downloading of aggregated international data (the `sector_packages` dataset)
  * Usage: `python .\climate-trace.py --skipDownloadSectors`

* `--skipForestSectorDownload`      
  * Boolean value, defaults to `False`
  * When set, skips downloading of country-level forest sector data (the `country_packages/forest_sectors` datasets)
  * Usage: `python .\climate-trace.py --skipForestSectorDownload`

* `--skipNonForestSectorDownload`   
  * Boolean value, defaults to `False`
  * When set, skips downloading of country-level non-forest sector data (the `country_packages/non_forest_sectors` datasets)
  * Usage: `python .\climate-trace.py --skipNonForestSectorDownload`

* `--skipUnzipFiles`                
  * Boolean value, defaults to `False`
  * When set, skips unzipping of the downloaded files
  * Usage: `python .\climate-trace.py --skipUnzipFiles`

* `--specifyCountries`                
  * array of strings, defaults to empty
  * When set, only downloads specified countries
  * Accepts an array of ISO-3166-1 alpha-3 countries (see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)
    * raises an exception if any invalid country is given as a param
  * Usage: `python .\climate-trace.py --specifyCountries GBR USA AFG`
  * 


## Requirements

* At least 2TB hard drive space for the entire download, plus its unzipped files
