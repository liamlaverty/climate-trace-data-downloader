import zipfile

class Zipper:

    @staticmethod
    def unzip_file(src:str, dest:str):
        with zipfile.ZipFile(src, 'r') as zip_ref:
            zip_ref.extract(dest)