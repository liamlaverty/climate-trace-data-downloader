import zipfile
import os

class Zipper:

    @staticmethod
    def unzip_file(src_file:str):
        dest_path = os.path.splitext(src_file)[0]
        print(f'unzipping file {src_file} to {dest_path}')

        with zipfile.ZipFile(src_file, 'r') as zip_ref:
            zip_ref.extractall(dest_path)