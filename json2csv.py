import argparse

from core.jsonconverter import json_converter
from core.settings import RESULT_PATH


def process_data(json_path: str):
    if not json_path:
        return 'No json file was provided'

    filename = json_path.split('/')[-1].split('.')[0]
    csv_filename = f'{filename}.csv'

    json_converter.save_as_csv(f'{json_path}', f'{RESULT_PATH}/{csv_filename}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", help="path to json file", type=str)
    args = parser.parse_args()

    process_data(args.json)
