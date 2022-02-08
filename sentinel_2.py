from sentinelsat.sentinel import SentinelAPI, read_geojson, geojson_to_wkt

import zipfile

import os

check_data_days_back = 1


def create_directory(direc: str):
    Path(direc).mkdir(parents=True, exist_ok=True)


def return_curr_date_str(days_to_skip, dt=None, get_str=True):
    if dt is None:
        dt = datetime.now() - timedelta(days=days_to_skip)
    return dt.strftime(r'%Y%m%d') if get_str else dt


api = SentinelAPI('sentinel_username', 'sentinel_password', 'https://scihub.copernicus.eu/dhus')


# footprint = geojson_to_wkt(read_geojson(r"E:\Python\sentinel\geoj.json"))
# Footprint should be dictionary of coordinates (e.g. bounding box)
def download_dataset(footprint: dict, directory: str):
    # Dates from and to for which you want to download data
    _DATE1 = return_curr_date_str(days_to_skip=check_data_days_back)
    _DATE2 = return_curr_date_str(days_to_skip=check_data_days_back - 1)
    footprint = geojson_to_wkt(footprint)
    print(_DATE1, _DATE2)
    products = api.query(footprint,
                              date=(_DATE1, _DATE2),
                              platformname='Sentinel-2',
                              processinglevel='Level-2A',
                              cloudcoverpercentage=(0, 100))

    for key, prod in products.items():
        api.get_product_odata(key)
        directory = os.path.join(
            directory,
            return_curr_date_str(0, prod['endposition']),
            'input',
        )
        create_directory(directory)
        api.download(key, directory_path=directory)

        zip_directory = os.path.join(directory, f"{prod['title']}.zip")
        with zipfile.ZipFile(zip_directory, 'r') as zip_ref:
            zip_ref.extractall(directory)
        return zip_directory.replace('.zip', '.SAFE')
