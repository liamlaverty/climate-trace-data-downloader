import os
import argparse
import datetime
from datalists.country_lists import countrylists
from datalists.climate_trace_data_lists import climatetracedatalists
from utilitytools.filedownloader import FileDownloader


class ClimateTraceDataDownloader:

    def __init__(self):
        """instantiates the climate trace data downloader"""


    def Do_Main(self):    
        parser = argparse.ArgumentParser(description='Downloads data from ClimateTrace to an output location')
        parser.add_argument('-o', '--outputPath', help='the output filepath for downloads. Defaults to the working directory', type=str, required=False, default='.')
        parser.add_argument('--forestSectorDownload', action=argparse.BooleanOptionalAction, help='Toggles downloading of forest sector data', required=False)
        parser.add_argument('--nonForestSectorDownload', action=argparse.BooleanOptionalAction, help='Toggles downloading of non-forest sector data', required=False)

        args = parser.parse_args()
        print(f'path:{args.outputPath}')

        downloadForest = args.forestSectorDownload == True
        downloadNonForest = args.nonForestSectorDownload == True
        print(f'dl forest sectors:{downloadForest}')
        print(f'dl non-forest sectors:{downloadNonForest}')

        t = datetime.datetime.now()
        file_name_date_part = t.strftime('%Y%m%d')
        self.download_country_level_data(file_name_date_part, args.outputPath, downloadForest, downloadNonForest)
        self.download_sector_level_data(file_name_date_part, args.outputPath)


    def download_country_level_data( self, file_path_date: str, dest_path:str, download_forest_sectors:bool, download_non_forest_sectors:bool):
        """
        Downloads country level data from climate trace
        """
        
        for i, country in enumerate(countrylists.country_three_char_list):
            # download file
            # https://downloads.climatetrace.org/country_packages/non_forest_sectors/AFG.zip
            # https://downloads.climatetrace.org/country_packages/forest/AFG.zip

            if download_non_forest_sectors:
            # download the non-forest-sectors data first, then the forest data sectors
                file_url = f'https://downloads.climatetrace.org/country_packages/non_forest_sectors/{country["alpha-3"]}.zip'
                output_path = os.path.join(dest_path, 'data_packages', 'climate_trace', 'country_packages', 'non_forest_sectors')
                FileDownloader.download_file(file_url, output_path, f'{file_path_date}_{country["alpha-3"]}.zip')
            
            if download_forest_sectors:
                # download the forest-sectors data first, then the forest data sectors
                file_url = f'https://downloads.climatetrace.org/country_packages/forest/{country["alpha-3"]}.zip'
                output_path = os.path.join('data_packages', 'climate_trace', 'country_packages', 'forest')
                FileDownloader.download_file(file_url, output_path, f'{file_path_date}_{country["alpha-3"]}.zip')
            


    def download_sector_level_data(self, file_path_date: str, dest_path:str):
        """
        Downloads sector level data from climate trace
        """
        
        for i, file in enumerate(climatetracedatalists.climate_trace_files_list):
            output_path = os.path.join(dest_path, 'data_packages', 'climate_trace', file['destPath'])
            FileDownloader.download_file(f'https://downloads.climatetrace.org/{file["url"]}', output_path, f'{file_path_date}_{file["destName"]}')


ctd = ClimateTraceDataDownloader()
ctd.Do_Main()