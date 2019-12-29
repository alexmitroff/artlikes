# Import basic modules
import argparse
import csv
import datetime as dt
import random
import time

import requests

# Constants
JSON_RESPONSE_NAME = 'projects.json'
HOME_URL = 'https://www.artstation.com'


def print_step_name(step_name='', decoration_number=4):
    print('{0} {1} {0}'.format('#'*decoration_number, step_name))


def get_assets_from_artstation(search=None, user=None):
    if not search and not user:
        print_step_name('Please provide user name or search term', 1)
        return None

    if user:
        mode = 'users/{}'.format(user.lower())
        request_data = {'page': 1}
        print_step_name('Getting assets from {} profile'.format(user.upper()), 1)
    else:
        mode = 'search'
        request_data = {
            'direction': 'desc',
            'order': 'likes_count',
            'page': 1,
            'q': search,
            'show_pro_first': False
        }
        print_step_name('Getting assets from "{}" search response'.format(search), 1)

    print_step_name('Retrive cookies', 1)
    request_url = '{}/{}/{}'.format(HOME_URL, mode, JSON_RESPONSE_NAME)
    session = requests.Session()
    response_cookies = session.get(HOME_URL)
    artstation_cookies = session.cookies.get_dict()
    print(artstation_cookies)

    print_step_name('Retrive assets', 1)
    r = requests.get(request_url, cookies=artstation_cookies, params=request_data)
    print(r.content.decode())
    art_json = r.json()
    page = request_data['page']
    total_count = art_json.get('total_count')
    assets = art_json.get('data')

    i = len(assets)
    print_step_name('Page {}: {}/{}'.format(request_data['page'], i, total_count), 1)
    while i < total_count:
        time.sleep(random.uniform(0.5, 5.0))
        request_data['page'] += 1

        print_step_name('Page {}: {}/{}'.format(request_data['page'], i, total_count), 1)
        r = requests.get(request_url, cookies=artstation_cookies, params=request_data)
        art_json = r.json()
        assets += art_json.get('data')
        total_count = art_json.get('total_count')
        if i == len(assets):
            print_step_name('Page {}: {}/{}'.format(request_data['page'], i, total_count), 1)
            break
        i = len(assets)
    print_step_name('All {} avaliable assets are retrived'.format(i), 1)
    return assets


def write_data_to_csv(assets=None, filename='untitled.csv'):
    print_step_name('Pack assets to {}'.format(filename), 1)
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = [
            'published_at',
            'likes_count',
            'views_count',
            'location',
        ]
        artwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        artwriter.writeheader()
        for asset in assets:
            user = asset.get('user')
            location = user.get('location') if user else ''
            row = {
                'published_at': asset.get('published_at'),
                'likes_count': asset.get('likes_count'),
                'views_count': asset.get('views_count'),
                'location': location,
                }
            artwriter.writerow(row)
    print_step_name('Assets was packed successfuly', 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="search term", type=str)
    parser.add_argument("-u", "--user", help="username", type=str)
    args = parser.parse_args()

    assets = get_assets_from_artstation(args.search, args.user)

    if assets:
        date = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        affix = args.search if args.search else args.user
        affix = '-'.join(affix.split(' '))
        filename = "{}_{}.csv".format(date, affix)
        write_data_to_csv(assets, filename)
