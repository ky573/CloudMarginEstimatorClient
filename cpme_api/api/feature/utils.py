import time
import enum
import os
import functools
from pprintjson import pprintjson
import json
from json.decoder import JSONDecodeError
from model_gen.config import settings, Environment
from typing import Tuple, Any, List, TextIO
import logging
import csv

# logging.root.manager.loggerDict['cpme_api']
log = logging.getLogger('cpme_api')


class Timer(object):
    def __init__(self):
        self.main_timer = None
        self.timer = None

    def start(self):
        self.main_timer = time.time()
        self.timer = time.time()

    def reset(self, main_timer=False):
        if main_timer:
            self.main_timer = time.time()
        else:
            self.timer = time.time()

    def get_time_str(self, main_timer=False):
        end = time.time()
        if main_timer:
            if not self.main_timer:
                self.main_timer = end
            start_time = self.main_timer
        else:
            if not self.timer:
                self.timer = end
            start_time = self.timer
        m, s = divmod(end - start_time, 60)
        h, m = divmod(m, 60)
        return "%02dh:%02dm:%02ds" % (h, m, s)


def data_folder_fix(path: str):
    """Check if a folder variable name is relative
    path starts with . and add global SCENARIO_PATH_FOLDER."""
    if path.startswith('./'):
        path = os.path.join(settings.scenario_path_folder, path.lstrip("./"))
    return path


class UnitSize(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes: int, unit=UnitSize.BYTES):
    """ Convert the size from bytes to other units like KB, MB or GB"""
    if unit == UnitSize.KB:
        return size_in_bytes/1024
    elif unit == UnitSize.MB:
        return size_in_bytes/(1024*1024)
    elif unit == UnitSize.GB:
        return size_in_bytes/(1024*1024*1024)
    else:
        return size_in_bytes


def get_file_size(file_path: str, size_type=UnitSize.MB):
    """ Get file in size in given unit like KB, MB or GB"""
    assert os.path.isfile(file_path), f'{file_path} not found'
    size = os.path.getsize(file_path)
    return round(convert_unit(size, size_type), 3)


def fancy(json_dict: dict, line_text: str = ''):
    """Pretty print of dict structure into stdout only!"""
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


def body_request_file_name(ep: str,
                           component_type: str,
                           env: str,
                           prefix: str = '',
                           suffix='json') -> str:
    if prefix:
        prefix += '_'
    return f'{prefix}{ep}.{suffix}'


def json_to_file(data_dict: dict, file_name: str, verbose=True, update=True):
    if not file_name.endswith('.json'):
        file_name = file_name + '.json'
    if update:
        with open(file_name, 'w') as f:
            json.dump(data_dict, f, indent=4, sort_keys=True)
        if verbose:
            log.info(f'Response saved in {file_name}')
    elif path := find_file(path=file_name):
        if path:
            log.info(f'Response already stored {path}')
    else:
        with open(file_name, 'w') as f:
            json.dump(data_dict, f, indent=4, sort_keys=True)
        if verbose:
            log.info(f'Response saved in {file_name}')
    return file_name


def load_json_file(file_dir: str = '', file_name: str = '', path: str = None, verbose: bool = False) -> dict:
    """Load JSON data into dict."""
    if path is None:
        path = os.path.join(file_dir, file_name)
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


def dir_check(file_dir: str, del_files: bool = False):
    if not os.path.isdir(file_dir):
        log.warning(f'Creating the new directory {file_dir}')
        os.makedirs(file_dir, exist_ok=True)
    if del_files:
        for file in os.listdir(file_dir):
            if os.path.isfile(file_dir + file):
                os.remove(file_dir + file)


def align_prefix(prefix: str = ''):
    if prefix:
        return prefix + '_'
    else:
        return ''


def update_prefix_content(prefix: str) -> str:
    if '_' in prefix:
        prefix = prefix.replace('_', '-')
    return prefix


def files_in_folder(folder=data_folder_fix(settings.requests_folder)):
    filenames = []
    for (_, _, filenames) in os.walk(folder):
        break
    return sorted(filenames)


def find_file_by_prefix(prefix: str, folder=data_folder_fix(settings.requests_folder)):
    prefix = update_prefix_content(prefix)
    f_files = []
    for file in files_in_folder(folder):
        if prefix in file:
            f_files.append(file)
    if len(f_files) == 1:
        return f_files[0]
    elif (l:=len(f_files)) > 1:
        log.warning(f'Found {l} files {f_files}. Loaded only the first one!')
        return f_files[0]
    else:
        return ''


def find_file(prefix: str = None,
              folder: str = '',
              file_name: str = '',
              path: str = '') -> str:
    if prefix:
        prefix = update_prefix_content(prefix)
    if not folder:
        folder = data_folder_fix("./example/data/")
    else:
        folder = data_folder_fix(folder)
    if os.path.isfile(path):
        pass
    elif os.path.isfile(os.path.join(folder, file_name)):
        path = os.path.join(folder, file_name)
    elif prefix and (file_name := find_file_by_prefix(prefix, folder)):
        path = os.path.join(folder, file_name)
    else:
        if prefix:
            log.warning(f'File with prefix = {prefix} not found in {folder}!')
        elif path:
            log.warning(f'File {path} not found!')
        else:
            log.warning(f'File {file_name} not found in {folder}!')
        return ''
    return path


def data_from_path(path: str) -> Tuple[str, str]:
    f_format = ''
    if not os.path.isfile(path):
        return None
    if '.json' in path:
        data = load_json_file(path=path)
        f_format = 'json'
    elif '.csv' in path:
        data = csv_to_str(path)
        f_format = 'csv'
    elif '.xml' in path:
        data = xml_to_str(path)
        f_format = 'xml'
    else:
        log.warning('Not supported file format [csv,xml,json]')
        data = ''
    return data, f_format


def xml_to_str(path: str) -> str:
    if not path.endswith('.xml'):
        return ''
    with open(path) as f:
        return f.read()


def csv_to_str(path: str) -> str:
    if not path.endswith('.csv'):
        return ''
    with open(path) as f:
        return f.read()


def truncate_list(vector: list, max_size: int = 100000) -> list:
    """Truncate list size with max_size"""
    assert isinstance(vector, list), 'Vector must by instance of list!'
    if len(vector) < max_size:
        max_size = len(vector)
    return vector[:max_size]


def isfloat(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_float(value) -> bool:
    if isinstance(value, float):
        return True
    else:
        return False


def isnumber(value: str):
    if value is None:
        return value
    if isinstance(value, int) or isinstance(value, float):
        return value
    if 'False' == value:
        return False
    elif 'True' == value:
        return True
    if value.isdigit():
        return int(value)
    elif isfloat(value):
        return float(value)
    else:
        return value


def catch_exception(enable: bool = False) -> Tuple[Any, bool]:
    """Catch Comet exceptions if enable == True. And return tuple of result state"""
    def decorator(func):
        if not enable:
            return func

        @functools.wraps(func)
        def raiser(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                if res or res is None:
                    print(f'func {func.__name__}: result => PASSED')
                else:
                    print(f'func {func.__name__}: result => FAILED')
                return res, True
            except Exception as e:
                print(f'func {func.__name__}: result => FAILED EXP_MSG:{e}')
                return e, False
        return raiser

    return decorator


def env_equal(envs: list = []):
    al_env = [Environment.alias(e) for e in envs]
    if envs is [] or (settings.current_env in al_env):
        return True
    else:
        return False


def use_for_env(envs: list = []):
    """Catch Comet exceptions if enable == True. And return tuple of result state"""
    def decorator(func):
        al_env = [Environment.alias(e) for e in envs]
        if envs is [] or (settings.current_env in al_env):
            return func

        @functools.wraps(func)
        def raiser(*args, **kwargs):
            log.warning(f'Skipping testcase {func.__name__} because it is valid only for {al_env}')
            return
            #res = func(*args, **kwargs)

        return raiser

    return decorator


def narrative(func):
    """decorator to print a doc string"""
    @functools.wraps(func)
    def raiser(*args, **kwargs):
        log.info(f'[ {func.__name__} ]: ===SCENARIO DESCRIPTION=== < {func.__doc__} >')
        return func(*args, **kwargs)

    return raiser


def check_response_model(func):
    def pattern(*args, **kwargs):
        class Status:
            def __init__(self):
                self._attrs = list()
                self._register = dict()

            def exist(self, model):
                self._attrs.append(model.id)

            def add(self, model):
                self._register[model.id] = str(model)

        status = Status()
        kwargs.update({'state': status})
        func(*args, **kwargs)
        res = list()
        tc_num = int()
        for key in status._register:
            tc_num += 1
            if key in status._attrs:
                log.info(f'TestSuite-{func.__name__}<TestCase-{tc_num}>: {key} found, records={status._attrs.count(key)}')
            else:
                res.append(f'Attribute Not found {status._register[key]}')
                log.error(f'TestSuite-{func.__name__}<TestCase-{tc_num}>: '
                          f'Attribute Not found {status._register[key]}')
        if res:
            raise Exception('\n'.join(res))
        return True
    return pattern


def load_csv_to_list(path: str = '',
                     folder: str = '',
                     file_name: str = '',
                     prefix: str = None) -> List[dict]:
    """"Load list of dictionaries from csv file."""
    path = find_file(file_name=file_name,
                     path=path,
                     folder=folder,
                     prefix=prefix)
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
