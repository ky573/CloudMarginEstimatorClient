import os
from pprintjson import pprintjson
import json
from json.decoder import JSONDecodeError
from typing import List, TextIO
import logging
import csv

# logging.root.manager.loggerDict['cpme_api']
log = logging.getLogger('cpme_api')


def fancy(json_dict: dict, line_text: str = ''):
    """
    Pretty print of dict structure as a JSON format into stdout only!
    :param json_dict: Dictionary data structure.
    :param line_text: A text to print before data structure.
    """
    if json_dict is None:
        print('\tNot defined!\n')
        return
    # if not isinstance(json_dict, dict):
    #    raise ValueError('Input must be dict for fancy()!')
    if json_dict:
        if line_text:
            print(line_text)
        pprintjson(json_dict)
    else:
        print('\tempty {}\n')


def dir_check(file_dir: str, del_files: bool = False):
    if not file_dir:
        return

    if not os.path.isdir(file_dir):
        log.warning(f'Creating the new directory {os.path.abspath(file_dir)}')
        os.makedirs(file_dir, exist_ok=True)

    if del_files:
        for file in os.listdir(file_dir):
            if os.path.isfile(file_dir + file):
                os.remove(file_dir + file)


def json_to_file(data_dict: dict, file_name: str, verbose=True, update=True) -> str:
    """
    Save dictionary structure into the JSON file.
    :param data_dict: dictionary object of json response
    :param file_name: The file_name can be string with absolute ('/.') or relative ('./') path or just a file name.
    :param verbose:  if False disable information messages
    :param update: if True it overwrites already existing file
    :return: absolute path of file_name
    """
    dir_name = os.path.dirname(file_name)
    dir_exist = os.path.isdir(dir_name)

    if not file_name.endswith('.json'):
        file_name = file_name + '.json'

    if dir_name == '':
        dir_exist = True

    file_name = os.path.abspath(file_name)
    if update and dir_exist:
        with open(file_name, 'w') as f:
            json.dump(data_dict, f, indent=4, sort_keys=True)
    elif path := find_file(path=file_name, folder=dir_name):
        if path:
            log.info(f'The file name already exists {path}. Use update=True to overwrite it.')
        return file_name
    else:
        dir_check(dir_name)
        with open(file_name, 'w') as f:
            json.dump(data_dict, f, indent=4, sort_keys=True)

    if verbose:
        log.info(f'The content saved into {file_name}')
    return file_name


def load_json_file(file_dir: str = '', file_name: str = '', path: str = None, verbose: bool = False) -> dict:
    """

    :param file_dir:
    :param file_name:
    :param path:
    :param verbose:
    :return:
    """
    """Load JSON data into dict."""
    if path is None:
        path = os.path.join(file_dir, file_name)
    path = os.path.abspath(path)

    if not os.path.isfile(path):
        log.error(f"Not such file or directory {path}!")
        return {}

    try:
        with open(path) as f:
            if verbose:
                log.info(f'Loading file {path}.')
            return json.load(f)
    except JSONDecodeError as e:
        log.error(f'Not valid JSON format in {path}. {str(e.args)}')
        return {}


def find_file(folder: str = '',
              file_name: str = '',
              path: str = '') -> str:
    if not folder:
        folder = "./example/data/"
    if os.path.isfile(path):
        pass
    elif os.path.isfile(os.path.join(folder, file_name)):
        path = os.path.join(folder, file_name)
    else:
        if path:
            log.warning(f'File {path} not found!')
        else:
            log.warning(f'File {file_name} not found in {folder}!')
        return ''
    return os.path.abspath(path)


def xml_to_str(path: str) -> str:
    """return content of xml file"""
    if not path.endswith('.xml'):
        return ''
    with open(path) as f:
        return f.read()


def csv_to_str(path: str) -> str:
    """return content of csv file"""
    if not path.endswith('.csv'):
        return ''
    with open(path) as f:
        return f.read()


def load_csv_to_list(path: str = '',
                     folder: str = '',
                     file_name: str = '') -> List[dict]:
    """"Load list of dictionaries from csv file."""
    path = find_file(file_name=file_name,
                     path=path,
                     folder=folder)
    if path == '':
        log.warning(f"File not found")
        return []
    if '.csv' not in path:
        log.warning(f"{path} is not CSV file")
        return []
    return _csv_to_data_with_open(path, ',', '"')


def _csv_to_data_with_open(file_name: str, delimiter: str, quotechar: str, mapping=None):
    """Convert general csv file to list of dictionaries using mapping dictionary applied to header fields."""
    with open(file_name, mode='r') as file_pointer:
        data = _csv_to_data(file_pointer, delimiter=delimiter, quotechar=quotechar, mapping=mapping)
    if data == ['']:
        return []
    else:
        return data


def _csv_to_data(rows: TextIO, delimiter: str, quotechar: str, mapping=None) -> List[dict]:
    """Convert general csv rows to list of dictionaries using mapping dictionary applied to header fields."""
    def digit_to_int(val: str):
        if val is None:
            return val
        if val.isdigit():
            return int(val)
        else:
            return val
    line = rows.readline()
    if not rows.readline():
        return line.split(delimiter)
    else:
        rows.seek(0)
    mapping = {} if mapping is None else mapping
    reader = csv.DictReader(rows, delimiter=delimiter, quotechar=quotechar)
    data = [{mapping.get(key, key): digit_to_int(val) for key, val in row.items()} for row in reader]
    return data
