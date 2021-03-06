import os

PUBLISHED_COLUMN_NAME = 'published_at'
LIKES_COLUMN_NAME = 'likes_count'
VIEWS_COLUMN_NAME = 'views_count'
LOCATION_COLUMN_NAME = 'location'

PLOT_FORMAT = 'svg'
PLOT_LABELS_FORMAT = "%d.%m.%Y"
FILE_SAVE_FORMAT = "%Y%m%d-%H%M%S"

JSON_RESPONSE_NAME = 'projects.json'
HOME_URL = 'https://www.artstation.com'

HOME_DIR = os.getenv('HOME')
RESULT_PATH = f'{HOME_DIR}/artlikes_result'
