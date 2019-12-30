import argparse

from core.artstationhandler import artstation_handler
from core.func import create_file_name
from core.jsonconverter import json_converter
from core.settings import RESULT_PATH


def process_data(user: str, search: str):

    assets = artstation_handler.get_assets(user=user, search=search)
    if not assets:
        return 'No assets available'

    filename = create_file_name(user, search)
    json_filename = f'{filename}.json'
    csv_filename = f'{filename}.csv'

    artstation_handler.save_as_json(assets, f'{RESULT_PATH}/{json_filename}')
    json_converter.save_as_csv(f'{RESULT_PATH}/{json_filename}', f'{RESULT_PATH}/{csv_filename}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="search term", type=str)
    parser.add_argument("-u", "--user", help="username", type=str)
    args = parser.parse_args()

    process_data(args.user, args.search)
