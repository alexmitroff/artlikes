import argparse
import json

from likes2csv import write_data_to_csv
from datetime import datetime as dt


def read_json(filename):
    with open(filename, 'r', newline='') as jsonfile:
        datastore = json.load(jsonfile)
        return datastore


def get_assets(datastore):
    return datastore.get('data')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", help="path to json file", type=str)
    args = parser.parse_args()

    data = read_json(args.json)
    assets = get_assets(data)

    if assets:
        date = dt.now().strftime("%Y%m%d-%H%M%S")
        affix = args.json
        affix = '-'.join(affix.split(' '))
        filename = "{}_artstation_{}.csv".format(date, affix)
        write_data_to_csv(assets, filename)
