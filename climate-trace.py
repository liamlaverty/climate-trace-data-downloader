import os
import requests
import datetime
from datalists.country_lists import countrylists
from datalists.climate_trace_data_lists import climatetracedatalists

def Do_Main():    
    t = datetime.datetime.now()
    file_name_date_part = t.strftime('%Y%m%d')
    download_country_level_data(file_name_date_part)
    download_sector_level_data(file_name_date_part)


def download_country_level_data(file_path_date: str, download_forest_sectors:bool = True):
    """
    Downloads country level data from climate trace
    """
    
    for i, country in enumerate(countrylists.country_three_char_list):
        # download file
        # https://downloads.climatetrace.org/country_packages/non_forest_sectors/AFG.zip
        # https://downloads.climatetrace.org/country_packages/forest/AFG.zip

        # download the non-forest-sectors data first, then the forest data sectors
        file_url = f'https://downloads.climatetrace.org/country_packages/non_forest_sectors/{country["alpha-3"]}.zip'
        dest_path = os.path.join('data_packages', 'climate_trace', 'country_packages', 'non_forest_sectors')
        download_file(file_url, dest_path, f'{file_path_date}_{country["alpha-3"]}.zip')
        
        if download_forest_sectors:
            # download the forest-sectors data first, then the forest data sectors
            file_url = f'https://downloads.climatetrace.org/country_packages/forest/{country["alpha-3"]}.zip'
            dest_path = os.path.join('data_packages', 'climate_trace', 'country_packages', 'forest')
            download_file(file_url, dest_path, f'{file_path_date}_{country["alpha-3"]}.zip')
        


def download_sector_level_data(file_path_date: str):
    """
    Downloads sector level data from climate trace
    """
     
    for i, file in enumerate(climatetracedatalists.climate_trace_files_list):
        dest_path = os.path.join('data_packages', 'climate_trace', file['destPath'])
        download_file(f'https://downloads.climatetrace.org/{file["url"]}', dest_path, f'{file_path_date}_{file["destName"]}')


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
    



Do_Main()