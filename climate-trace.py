import os
import requests
import datetime

climate_trace_files =[
    { 
        'url': 'sector_packages/buildings.zip',
        'destPath': 'sector_packages',
        'destName': 'buildings.zip'
    },
    { 
        'url': 'sector_packages/fossil_fuel_operations.zip',
        'destPath': 'sector_packages',
        'destName': 'fossil_fuel_operations.zip'
    },
    { 
        'url': 'sector_packages/manufacturing.zip',
        'destPath': 'sector_packages',
        'destName': 'manufacturing.zip'
    },
    { 
        'url': 'sector_packages/power.zip',
        'destPath': 'sector_packages',
        'destName': 'power.zip'
    },
    { 
        'url': 'sector_packages/waste.zip',
        'destPath': 'sector_packages',
        'destName': 'waste.zip'
    },
    { 
        'url': 'sector_packages/agriculture.zip',
        'destPath': 'sector_packages',
        'destName': 'agriculture.zip'
    },
    { 
        'url': 'sector_packages/transportation.zip',
        'destPath': 'sector_packages',
        'destName': 'transportation.zip'
    },
    { 
        'url': 'sector_packages/forestry_and_land_use.zip',
        'destPath': 'sector_packages',
        'destName': 'forestry_and_land_use.zip'
    },
]


def Main():
    t = datetime.datetime.now()
    file_name_date_part = t.strftime('%Y%m%d')
    for i, file in enumerate(climate_trace_files):
        download_file(f'https://downloads.climatetrace.org/{file["url"]}', file['destPath'], f'{file_name_date_part}_{file["destName"]}')


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
    




Main()