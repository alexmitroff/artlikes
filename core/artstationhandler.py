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
    _basic_params = {
        'additional_fields': 'views_count',
        'page': 1,
    }

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

    def get_user_request_data(self, user: str) -> (str, dict):
        """Prepare request parameters for user mode

        :param user: str
        :return: mode: str, request_data: dict
        """
        request_data = self._basic_params
        return f'users/{user.lower()}', request_data

    def get_search_request_data(self, search: str) -> (str, dict):
        """Prepare request parameters for search mode

        :param search: str
        :return: mode: str, request_data: dict
        """
        request_data = {
            'direction': 'desc',
            'order': 'likes_count',
            'q': search,
            'show_pro_first': False
        }
        request_data.update(self._basic_params)
        return 'search', request_data

    @staticmethod
    def get_request_url(mode: str) -> str:
        return f'{HOME_URL}/{mode}/{JSON_RESPONSE_NAME}'

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
            print_step_name(f'Getting assets from {user.upper()} profile', 1)
        else:
            mode, request_data = self.get_search_request_data(search)
            print_step_name(f'Getting assets from "{search}" search response', 1)

        print_step_name('Retrive data from artstation', 1)
        assets, total_count = self.get_data(mode, request_data)

        assets_count = self.get_assets_count(assets)
        print_step_name(f'Page {request_data["page"]}: {assets_count}/{total_count}', 1)

        while total_count > assets_count:
            time.sleep(random.uniform(0.5, 5.0))
            request_data['page'] += 1

            next_assets, total_count = self.get_data(mode, request_data)
            assets += next_assets

            renewed_assets_count = self.get_assets_count(assets)
            print_step_name(f'Page {request_data["page"]}: {assets_count}/{total_count}', 1)
            if not assets_count == renewed_assets_count:
                assets_count = renewed_assets_count
            else:
                break

        print_step_name(f'All {assets_count} available assets were retrieved', 1)
        return assets

    @staticmethod
    def save_as_json(assets: dict, filepath: str):
        with open(filepath, 'w') as f:
            data_str = json.dumps(assets)
            f.write(data_str)
            f.close()
        print_step_name(f'Pack assets to {filepath}', 1)


artstation_handler = ArtstationHandler()
