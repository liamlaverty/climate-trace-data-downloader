import os
import requests

class FileDownloader:
    
    @staticmethod
    def download_file(url: str, destFilePath: str, destFileName:str):
        if not os.path.exists(destFilePath):
            os.makedirs(destFilePath)

        file_path = os.path.join(destFilePath, destFileName)

        request = requests.get(url, allow_redirects=True, stream=True)

        if request.ok:
            print(f'downloading to {os.path.abspath(file_path)}')

            with open(file_path, 'wb') as f:
                for chunk in request.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())
            return os.path.abspath(file_path)
        else:
            print(f'Status:{request.status_code, request.text}. Failed to download {url} to {file_path}')
        
    