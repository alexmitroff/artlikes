# Import basic modules
import argparse
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def save_boxplot(df, likes=True):
    column='likes_count' if likes else 'views_count'
    plt.figure();
    likes_boxplot = df.boxplot(column=column)
    format = 'svg'
    plt.savefig('{}.{}.{}'.format(filepath, column, format), format=format)

def get_data_from_csv(filepath=None):
    df = pd.read_csv(filepath)
    likes = df[df.columns[1]]
    views = df[df.columns[2]]
    save_boxplot(df)
    if not views.empty:
        save_boxplot(df, False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="csv file path", type=str)
    args = parser.parse_args()
    if args.file:
        filepath = os.path.join(BASE_DIR, args.file)
        get_data_from_csv(filepath)
