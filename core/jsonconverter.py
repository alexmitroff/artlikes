import csv
import json

from .func import print_step_name
from .settings import *

__all__ = (
    'json_converter',
)


class JsonConverter:

    def __new__(cls):
        """We do not need to have multiple instances of JsonConverter"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(JsonConverter, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def read_json(json_file_path: str) -> dict:
        with open(json_file_path, 'r', newline='') as json_file:
            print_step_name(f'Retrieve assets from {json_file_path}', 1)
            return json.load(json_file)

    def save_as_csv(self, input_file_path: str, output_file_path: str):
        assets = self.read_json(input_file_path)
        print_step_name(f'Pack assets to {output_file_path}', 1)
        with open(output_file_path, 'w', newline='') as csv_file:
            fieldnames = (
                PUBLISHED_COLUMN_NAME,
                LIKES_COLUMN_NAME,
                VIEWS_COLUMN_NAME,
                LOCATION_COLUMN_NAME,
            )
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for asset in assets:
                user = asset.get('user')
                location = user.get('location') if user else ''
                row = {
                    PUBLISHED_COLUMN_NAME: asset.get(PUBLISHED_COLUMN_NAME),
                    LIKES_COLUMN_NAME: asset.get(LIKES_COLUMN_NAME),
                    VIEWS_COLUMN_NAME: asset.get(VIEWS_COLUMN_NAME),
                    LOCATION_COLUMN_NAME: location,
                    }
                csv_writer.writerow(row)
        print_step_name('Assets was packed successfully', 1)


json_converter = JsonConverter()
