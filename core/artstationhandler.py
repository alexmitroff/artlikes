import json
import random
import time

import requests

from .func import print_step_name
from .settings import *

__all__ = (
    'artstation_handler',
)


class ArtstationHandler:

    def __new__(cls):
        """We do not need to have multiple instances of ArtstationHandler"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(ArtstationHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        print_step_name('Retrive artstation cookies', 1)
        session = requests.Session()
        session.get(HOME_URL)
        self.artstation_cookies = session.cookies.get_dict()

    @staticmethod
    def get_assets_count(assets: dict) -> int:
        return len(assets)

    @staticmethod
    def get_user_request_data(user: str) -> (str, dict):
        return 'users/{}'.format(user.lower()), {'page': 1}

    @staticmethod
    def get_search_request_data(search: str) -> (str, dict):
        request_data = {
            'direction': 'desc',
            'order': 'likes_count',
            'page': 1,
            'q': search,
            'show_pro_first': False
        }
        return 'search', request_data

    @staticmethod
    def get_request_url(mode: str) -> str:
        return '{}/{}/{}'.format(HOME_URL, mode, JSON_RESPONSE_NAME)

    def get_data(self, mode: str, request_data: dict) -> (dict, dict):
        r = requests.get(self.get_request_url(mode), cookies=self.artstation_cookies, params=request_data)
        art_json = r.json()
        return art_json.get('data'), art_json.get('total_count')

    def get_assets(self, user: str = None, search: str = None) -> dict:

        if not search and not user:
            print_step_name('Please provide user name or search term', 1)
            return {}

        if user:
            mode, request_data = self.get_user_request_data(user)
            print_step_name('Getting assets from {} profile'.format(user.upper()), 1)
        else:
            mode, request_data = self.get_search_request_data(search)
            print_step_name('Getting assets from "{}" search response'.format(search), 1)

        print_step_name('Retrive data from artstation', 1)
        assets, total_count = self.get_data(mode, request_data)

        i = self.get_assets_count(assets)
        print_step_name('Page {}: {}/{}'.format(request_data['page'], i, total_count), 1)
        while i < total_count:
            time.sleep(random.uniform(0.5, 5.0))
            request_data['page'] += 1

            print_step_name('Page {}: {}/{}'.format(request_data['page'], i, total_count), 1)
            next_assets, next_total_count = self.get_data(mode, request_data)
            assets += next_assets
            if i == len(assets):
                print_step_name('Page {}: {}/{}'.format(request_data['page'], i, next_total_count), 1)
                break
            i = self.get_assets_count(assets)
        print_step_name('All {} available assets were retrieved'.format(i), 1)
        return assets

    @staticmethod
    def save_as_json(assets: dict, filepath: str):
        with open(filepath, 'w') as f:
            data_str = json.dumps(assets)
            f.write(data_str)
            f.close()
        print_step_name(f'Pack assets to {filepath}', 1)


artstation_handler = ArtstationHandler()
