"""Script to transfer data in CSV to box plots

Usage:
    python csv2plot path/to/file.csv path/to/file2.csv

Returns two svg files with plots: likes and views
"""
import argparse
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from settings import *
import datetime as dt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_filename(file_path: str) -> str:
    """
    './results/20191228-161623_artstation_username.csv' => ['.', 'results', '20191228-161623_artstation_username.csv']
    => '20191228-161623_artstation_username.csv' => ['20191228-161623_artstation_username', 'csv']
    => '20191228-161623_artstation_username' => ['20191228-161623', 'artstation', 'username'] => '28.12.2019 username'
    :param file_path:
    :return: string
    """
    file_name_pieces = file_path.split('/')[-1].split('.')[0].split('_')
    date = dt.datetime.strptime(file_name_pieces[0], FILE_SAVE_FORMAT)
    return '%s %s' % (date.strftime(PLOT_LABELS_FORMAT), file_name_pieces[-1])


def save_boxplot(data_dict: dict, title: str = 'Likes'):
    keys = []
    values = []
    data = sorted(data_dict.items())
    for key, value in data:
        keys.append(get_filename(key))
        values.append(value)
    plt.figure()
    plt.boxplot(x=values, labels=keys)
    save_path = '%s.%s.%s' % (filepath, title.lower(), PLOT_FORMAT)
    plt.savefig(save_path, format=PLOT_FORMAT)
    print('Plot saved to', save_path)


def get_data_from_csv(file_path):
    """
    :param file_path:
    :return: likes, views (np.ndarray)
    """
    df = pd.read_csv(file_path)
    return df[LIKES_COLUMN_NAME].values, df[VIEWS_COLUMN_NAME].values


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", help="csv file path", nargs='+', type=str)
    args = parser.parse_args()

    if args.files:
        file_list = args.files
        file_list = file_list
        likes_dict = {}
        views_dict = {}
        for file_str in file_list:
            print('Process', file_str)
            filepath = os.path.join(BASE_DIR, file_str)
            likes, views = get_data_from_csv(filepath)
            likes_dict[file_str] = likes
            views_dict[file_str] = views
        save_boxplot(likes_dict, title='Likes')
        # save_boxplot(views_dict, title='Views')
