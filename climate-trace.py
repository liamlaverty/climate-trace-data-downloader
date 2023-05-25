import os
import requests
import argparse
import datetime
from datalists.country_lists import countrylists
from datalists.climate_trace_data_lists import climatetracedatalists


class ClimateTradeDataDownloader:


    def Do_Main():    
        parser = argparse.ArgumentParser(description='Downloads data from ClimateTrace to an output location')
        parser.add_argument('-o', '--outputPath', help='the output filepath for downloads. Defaults to the working directory', type=str, required=False, default='.')
        parser.add_argument('-f', '--forestSectorDownload', help='Toggles downloading of forest sector data, defaults to true', type=bool, default=True, required=False)
        parser.add_argument('-n', '--nonForestSectorDownload', help='Toggles downloading of non-forest sector data, defaults to true', type=bool, default=True, required=False)

        args = parser.parse_args()
        print(f'path:{args.outputPath}')
        print(f'dl forest sectors:{args.forestSectorDownload}')
        print(f'dl non-forest sectors:{args.nonForestSectorDownload}')

        t = datetime.datetime.now()
        file_name_date_part = t.strftime('%Y%m%d')
        download_country_level_data(file_name_date_part, args.outputPath, args.forestSectorDownload, args.nonForestSectorDownload)
        download_sector_level_data(file_name_date_part, args.outputPath)


    def download_country_level_data(file_path_date: str, dest_path:str, download_forest_sectors:bool, download_non_forest_sectors:bool):
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
                download_file(file_url, output_path, f'{file_path_date}_{country["alpha-3"]}.zip')
                return
            
            if download_forest_sectors:
                # download the forest-sectors data first, then the forest data sectors
                file_url = f'https://downloads.climatetrace.org/country_packages/forest/{country["alpha-3"]}.zip'
                output_path = os.path.join('data_packages', 'climate_trace', 'country_packages', 'forest')
                download_file(file_url, output_path, f'{file_path_date}_{country["alpha-3"]}.zip')
                return
            


    def download_sector_level_data(file_path_date: str, dest_path:str):
        """
        Downloads sector level data from climate trace
        """
        
        for i, file in enumerate(climatetracedatalists.climate_trace_files_list):
            output_path = os.path.join(dest_path, 'data_packages', 'climate_trace', file['destPath'])
            download_file(f'https://downloads.climatetrace.org/{file["url"]}', output_path, f'{file_path_date}_{file["destName"]}')


    def download_file(url: str, destFilePath: str, destFileName:str):
        if not os.path.exists(destFilePath):
            os.makedirs(destFilePath)

        file_path = os.path.join(destFilePath, destFileName)

        request = requests.get(url, allow_redirects=True, stream=True)

        if request.ok:
            print(f'saving to {os.path.abspath(file_path)}')

            with open(file_path, 'wb') as f:
                for chunk in request.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
        else:
            print(f'Status:{request.status_code, request.text}. Failed to download {url} to {file_path}')
        


ctd = ClimateTradeDataDownloader()
ctd.Do_Main()