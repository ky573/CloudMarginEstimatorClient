from model_gen.config import settings
import yaml
import os
import urllib
import logging
from model_gen.package import yaml_parser, SwaggerAttributes

log = logging.getLogger('swageger-gen')

END_POINTS = []


def get_ep_url(end_point: str) -> str:
    return urllib.parse.urljoin(settings.url, end_point)


def yaml_load(yaml_path: str = '', ext_dir=''):
    """
    The function create:
     1. definition.Container with available features
        to handle definitions like like type, description, example, list of properties of objects and arrays
        After the load the Container will exist as a single ton
    """
    if not (yaml_path and os.path.isfile(yaml_path)):
        yaml_path = settings.SWAGGER_YAML_FILE
    log.debug(f'Loading swagger template {yaml_path}')
    with open(yaml_path, 'r') as stream:
        try:
            res = yaml.safe_load(stream)
            yaml_parser(res, ext_dir)
        except yaml.YAMLError as exc:
            log.error(exc)


def loader(yaml_path: str = '', ext_dir=''):
    """
    Function loads and translate yaml file into the Objects
    and return map of all resource objects and map of all input objects like.
    """
    yaml_load(yaml_path, ext_dir)


def list_all_attributes(ext_dir):
    msg = list()
    attributes = SwaggerAttributes(ext_dir)
    msg.append(f'All defined attributes which are used in API data model.\n')
    msg.append(f"\nArray data structures: \n{attributes.get_swagger_array_names()}\n")
    msg.append(f"\nObject data structures: \n{attributes.get_swagger_object_names()}\n")
    msg.append(f"\nPrimitive Numbers: \n{attributes.get_swagger_primitive_names('number')}\n")
    msg.append(f"\nPrimitive Strings: \n{attributes.get_swagger_primitive_names('string')}\n")
    msg.append(f"\nPrimitive Booleans: \n{attributes.get_swagger_primitive_names('boolean')}\n")
    msg.append(f"\nBody Objects: \n{attributes.get_swagger_body_names()}\n")
    msg.append(f"\nResponse Objects: \n{attributes.get_swagger_response_names()}\n")
    # msg.append(f"\nCSV structures: \n{list(map(lambda x: x, con.get_csv_map()))}\n")
    print(''.join(msg))


def generate_models(yaml_file='', ext_dir=''):
    if ext_dir:
        ext_dir = os.path.join(ext_dir, '../cpme_api/api/models/')
        os.makedirs(ext_dir, exist_ok=True)

    loader(yaml_file, ext_dir)


