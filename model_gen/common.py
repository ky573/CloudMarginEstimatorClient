"""
This namespace contains useful functions
"""
from typing import List, TextIO
from model_gen.config import log
import csv
import json
from urllib import parse
from typing import Union
from cpme_api.api.feature.utils import find_file


def endpoint_to_str(endpoint: str) -> List[str]:
    # remove chars ['/', '{', '}'] or concatenate
    endpoint = endpoint.translate({ord("{"): None, ord("}"): None})
    ep_list = endpoint.split('/')
    if len(ep_list) > 2:
        return "_".join(ep_list[1:])
    else:
        return endpoint[1:]


def ep_strip_path(endpoint: str) -> str:
    if '{' in endpoint:
        endpoint = endpoint.split('{')[0].rstrip('/')
    return endpoint


def get_ep_from_url(url: str) -> str:
    """
    converts ../api/v2.0/products?business_date=20230101&live=false -> /products
    converts ../api/v2.0/convert/otc/shorthand -> /convert/otc/shorthand
    """
    if 'convert' in url:
        items = url.split("/")[-3:]
    else:
        items = url.split("/")[-1:]
    eps = list()
    for item in items:
        ep = '/' + item
        if '?' in ep:
            ep = ep.split("?")[0]
        eps.append(ep)
    return ''.join(eps)


def get_param_name(ref_name: str) -> str:
    return ref_name.split('/')[-1]


def load_csv_to_list(path: str = '',
                     folder: str = '',
                     file_name: str = '',
                     prefix: str = None) -> List[dict]:
    """"Load list of dictionaries from csv file."""
    # TODO check if file exists
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


def data_to_json(data, file_name, indent):
    """Store list of dictionaries to json file."""
    with open(file_name, 'w') as file_pointer:
        json.dump(data, file_pointer, indent=indent)


def data_to_csv(data: list, file_name: str):
    """Store list of dictionaries to csv file."""
    def one_dim_dict(data_: Union[dict, list]) -> bool:
        if isinstance(data_, list):
            return False
        return all(list(map(lambda x: not isinstance(x, dict), data_.values())))

    if 'clearing_currencies' in file_name:
        with open(file_name, 'w', newline='') as file_pointer:
            file_pointer.write(','.join(data))
    elif one_dim_dict(data):
        with open(file_name, 'w', newline='') as file_pointer:
            writer = csv.DictWriter(file_pointer, fieldnames=data.keys())
            writer.writeheader()
            writer.writerows([data])
    elif data == [] or isinstance(data[0], str):  # check if do not harm snapshot storage
        with open(file_name, 'w', newline='') as file_pointer:
            for line in data:
                file_pointer.write(line + '\n')
    elif not isinstance(data[0], dict):
        with open(file_name, 'w', newline='') as file_pointer:
            file_pointer.write(','.join(data))
    else:
        fieldnames = sorted(set(key for dct in data for key in dct))
        with open(file_name, 'w', newline='') as file_pointer:
            writer = csv.DictWriter(file_pointer, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    log.debug(f'The file {file_name} was updated.')


def get_snapshot_name_from_resource(schema: dict) -> str:
    if isinstance(schema, list):
        properties = schema[0]
    else:
        properties = schema
    for params in properties.get_properties():
        if properties[params].is_array:
            return params
    return None  # no snapshots only simple dict


def get_snapshot_ts_to_str(response: dict) -> str:
    is_live = response.get('live', '')
    if isinstance(is_live, bool):
        is_live = int(is_live)
        return f"_{is_live}_{response.get('live_timestamp', '')}"
    else:
        return ''


def host_from_url(url: str) -> str:
    return parse.urljoin(url, '/')


def str_to_double_quotes(value: Union[str, List[str]]):
    if value is None:
        return None
    if isinstance(value, str):
        return "\"" + value + "\""
    else:
        return str(value).replace("'", "\"")
