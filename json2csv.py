"""Script that converts JSON to CSV data

Usage:
    python json2csv.py -f path_to/file_name.json

Returns file <file_name>.csv
"""

import argparse

from core.func import get_or_create_dir
from core.jsonconverter import json_converter
from core.settings import RESULT_PATH


def process_data(json_path: str):
    if not json_path:
        return 'No json file was provided'

    filename = json_path.split('/')[-1].split('.')[0]
    csv_filename = f'{filename}.csv'

    result_path = get_or_create_dir(RESULT_PATH)
    json_converter.save_as_csv(f'{json_path}', f'{result_path}/{csv_filename}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="path to json file", type=str)
    args = parser.parse_args()

    process_data(args.json)
