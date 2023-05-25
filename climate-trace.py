import os
import argparse
import datetime
from datalists.country_lists import countrylists
from datalists.climate_trace_data_lists import climatetracedatalists
from utilitytools.filedownloader import FileDownloader
from utilitytools.zipper import Zipper


class ClimateTraceDataDownloader:

    def __init__(self):
        """instantiates the climate trace data downloader"""


    def main(self):    
        parser = argparse.ArgumentParser(description='Downloads data from ClimateTrace to an output location')
        parser.add_argument('-o', '--outputPath', help='the output filepath for downloads. Defaults to the working directory', type=str, required=False, default='.')
        parser.add_argument('--forestSectorDownload', action=argparse.BooleanOptionalAction, help='Toggles downloading of forest sector data', required=False)
        parser.add_argument('--downloadCountries', action=argparse.BooleanOptionalAction, help='Toggles downloading of country level data', required=False)
        parser.add_argument('--nonForestSectorDownload', action=argparse.BooleanOptionalAction, help='Toggles downloading of non-forest sector data', required=False)
        parser.add_argument('--unzipFiles', action=argparse.BooleanOptionalAction, help='Toggles unzipping of files into the download directory', required=False)

        parser.set_defaults(unzipFiles=True)

        args = parser.parse_args()
        print(f'path:{args.outputPath}')

        downloadCountries = args.downloadCountries == False
        downloadForest = args.forestSectorDownload == False
        downloadNonForest = args.nonForestSectorDownload == False
        unzipFilesAfterDownload = args.unzipFiles == True
        print(f'dl countries:{downloadCountries}')
        print(f'dl forest sectors:{downloadForest}')
        print(f'dl non-forest sectors:{downloadNonForest}')
        print(f'unzip after download:{unzipFilesAfterDownload}')

        t = datetime.datetime.now()
        file_name_date_part = t.strftime('%Y%m%d')
    
        if downloadNonForest:
            self.download_country_level_non_forest_data(file_name_date_part, args.outputPath)    
        if downloadForest:
            self.download_country_level_forest_data(file_name_date_part, args.outputPath)
        if downloadCountries:
            self.download_sector_level_data(file_name_date_part, args.outputPath)
    
        if unzipFilesAfterDownload:
            self.unzip_files(args.outputPath)

    def unzip_files(self, directory_src_path):
        """
        Unzips the files after downloading
        """
        files = [f for f in os.listdir(directory_src_path) if os.path.isfile(os.path.join(directory_src_path, f))]

        for i, file in enumerate(files):
            print(f'unzipping file {file}')
            # Zipper.unzip_file(file.path)

    def download_country_level_forest_data( self, file_path_date: str, dest_path:str):
        """
        Downloads country level data from climate trace for forest sectors
        """
        
        for i, country in enumerate(countrylists.country_three_char_list):
            # download file
            # https://downloads.climatetrace.org/country_packages/forest/AFG.zip
            # download the forest-sectors data first, then the forest data sectors
            file_url = f'https://downloads.climatetrace.org/country_packages/forest/{country["alpha-3"]}.zip'
            output_path = os.path.join(dest_path, 'data_packages', 'climate_trace', 'country_packages', 'forest')
            file = FileDownloader.download_file(file_url, output_path, f'{file_path_date}_{country["alpha-3"]}.zip')
            Zipper.unzip_file(os.path.join(output_path, file))
        

    def download_country_level_non_forest_data( self, file_path_date: str, dest_path:str):
        """
        Downloads country level data from climate trace for non-forest sectors
        """
        
        for i, country in enumerate(countrylists.country_three_char_list):
            # download file
            # https://downloads.climatetrace.org/country_packages/non_forest_sectors/AFG.zip
            # download the non-forest-sectors data first, then the forest data sectors
            file_url = f'https://downloads.climatetrace.org/country_packages/non_forest_sectors/{country["alpha-3"]}.zip'
            output_path = os.path.join(dest_path, 'data_packages', 'climate_trace', 'country_packages', 'non_forest_sectors')
            file = FileDownloader.download_file(file_url, output_path, f'{file_path_date}_{country["alpha-3"]}.zip')
            Zipper.unzip_file(os.path.join(output_path, file), os.path.join(output_path, f'{file_path_date}_{country["alpha-3"]}'))



    def download_sector_level_data(self, file_path_date: str, dest_path:str):
        """
        Downloads sector level data from climate trace
        """
        
        for i, file in enumerate(climatetracedatalists.climate_trace_files_list):
            output_path = os.path.join(dest_path, 'data_packages', 'climate_trace', file['destPath'])
            file = FileDownloader.download_file(f'https://downloads.climatetrace.org/{file["url"]}', output_path, f'{file_path_date}_{file["destName"]}')


ctd = ClimateTraceDataDownloader()
ctd.main()