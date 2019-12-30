import datetime as dt
import os

from .settings import FILE_SAVE_FORMAT

__all__ = (
    'print_step_name',
    'create_file_name',
    'get_or_create_dir',
)


def print_step_name(step_name: str = '', decoration_number: int = 4):
    decoration = '#'*decoration_number
    print(f'{decoration} {step_name} {decoration}')


def create_file_name(user: str, search: str) -> str:
    date = dt.datetime.now().strftime(FILE_SAVE_FORMAT)
    affix = user if user else search
    affix = '-'.join(affix.split(' '))
    return f'{date}_{affix}'


def get_or_create_dir(dir_path: str) -> str:
    if os.path.exists(dir_path):
        return dir_path
    try:
        os.mkdir(dir_path)
    except OSError:
        print(f'Creation of the directory {dir_path} failed')
    else:
        print(f'Successfully created the directory {dir_path}')
    return dir_path
