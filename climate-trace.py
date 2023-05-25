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
        parser.add_argument('--downloadSectors', action=argparse.BooleanOptionalAction, help='Toggles downloading of sector level data', required=False)
        parser.add_argument('--forestSectorDownload', action=argparse.BooleanOptionalAction, help='Toggles downloading of country level forest sector data', required=False)
        parser.add_argument('--nonForestSectorDownload', action=argparse.BooleanOptionalAction, help='Toggles downloading of country level non-forest sector data', required=False)
        parser.add_argument('--unzipFiles', action=argparse.BooleanOptionalAction, help='Toggles unzipping of files into the download directory', required=False)

        parser.set_defaults(downloadSectors=True)
        parser.set_defaults(forestSectorDownload=True)
        parser.set_defaults(nonForestSectorDownload=True)
        parser.set_defaults(unzipFiles=True)

        args = parser.parse_args()
        print(f'path:{args.outputPath}')

        downloadSectors = args.downloadSectors == True
        downloadForest = args.forestSectorDownload == True
        downloadNonForest = args.nonForestSectorDownload == True
        unzipFilesAfterDownload = args.unzipFiles == True

        print(f'dl countries:{downloadSectors}')
        print(f'dl forest sectors:{downloadForest}')
        print(f'dl non-forest sectors:{downloadNonForest}')
        print(f'unzip after download:{unzipFilesAfterDownload}')

        t = datetime.datetime.now()
        file_name_date_part = t.strftime('%Y%m%d')

        non_forest_dest_path = os.path.join(args.outputPath, 'data_packages', file_name_date_part, 'climate_trace', 'country_packages', 'non_forest_sectors')
        forest_dest_path = os.path.join(args.outputPath, 'data_packages', file_name_date_part, 'climate_trace', 'country_packages', 'forest_sectors')
        countries_dest_path = os.path.join(args.outputPath, 'data_packages', file_name_date_part, 'climate_trace', 'sector_packages')
    
         # limit the number of files downloaded (for testing)
         # set to -1 or 0 to download all
        top_n_files_only = -1

        if downloadNonForest:
            self.download_country_level_non_forest_data(non_forest_dest_path, top_n_countries = top_n_files_only)    
        if downloadForest:
            self.download_country_level_forest_data(forest_dest_path, top_n_countries = top_n_files_only)
        if downloadSectors:
            self.download_sector_level_data(countries_dest_path, top_n_filesets = top_n_files_only)
    
        if unzipFilesAfterDownload:
            self.unzip_files(non_forest_dest_path)
            self.unzip_files(forest_dest_path)
            self.unzip_files(countries_dest_path)

    def unzip_files(self, directory_src_path):
        """
        Unzips the files after downloading
        """
        files = [f for f in os.listdir(directory_src_path) if os.path.isfile(os.path.join(directory_src_path, f))]

        for i, file in enumerate(files):
            path = os.path.join(directory_src_path, file)             
            Zipper.unzip_file(os.path.join(directory_src_path, file))


    def download_country_level_forest_data( self, dest_path:str, top_n_countries: int = -1):
        """
        Downloads country level data from climate trace for forest sectors
        """

        for i, country in enumerate(countrylists.country_three_char_list[:5]):
            # download file
            # https://downloads.climatetrace.org/country_packages/forest/AFG.zip
            # download the forest-sectors data first, then the forest data sectors
            file_url = f'https://downloads.climatetrace.org/country_packages/forest/{country["alpha-3"]}.zip'
            FileDownloader.download_file(file_url, dest_path, f'{country["alpha-3"]}.zip')
            if top_n_countries > 0:
                if i >= top_n_countries: 
                    return


    def download_country_level_non_forest_data( self, dest_path:str, top_n_countries: int = -1):
        """
        Downloads country level data from climate trace for non-forest sectors
        """
        
        for i, country in enumerate(countrylists.country_three_char_list[:5]):
            # download file
            # https://downloads.climatetrace.org/country_packages/non_forest_sectors/AFG.zip
            # download the non-forest-sectors data first, then the forest data sectors
            file_url = f'https://downloads.climatetrace.org/country_packages/non_forest_sectors/{country["alpha-3"]}.zip'
            FileDownloader.download_file(file_url, dest_path, f'{country["alpha-3"]}.zip')
            if top_n_countries > 0:
                if i >= top_n_countries: 
                    return


    def download_sector_level_data(self, dest_path:str, top_n_filesets = -1):
        """
        Downloads sector level data from climate trace
        """
        
        for i, file in enumerate(climatetracedatalists.climate_trace_files_list):
            file = FileDownloader.download_file(f'https://downloads.climatetrace.org/{file["url"]}', dest_path, f'{file["destName"]}')
            if top_n_filesets > 0:
                if i >= top_n_filesets: 
                    return


ctd = ClimateTraceDataDownloader()
ctd.main()