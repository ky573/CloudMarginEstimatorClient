import ipdb

from model_gen.config import settings, PROJECT_ROOT
from cpme_api.api.feature.utils import dir_check
import logging
from copy import copy
import json
import os
from typing import Any, List
import importlib

log = logging.getLogger('model_gen')

MODULE_FOLDER = os.path.join(PROJECT_ROOT, 'cpme_api/api/models/')
PRIMITIVE_FOLDER = 'primitive/'
EXAMPLES_FOLDER = 'examples/'
RESPONSES_FOLDER = 'responses/'
REQUEST_BODY_FOLDER = 'request_body/'

SWAGGER_TYPES = ('number', 'string', 'boolean')

YAML_FILE = None
primitive_imports = list()
components_imports = list()
response_imports = list()
request_body_imports = list()


def load(yaml):
    global YAML_FILE
    YAML_FILE = yaml


def align_object_name(name: str) -> str:
    names = name.split('_')
    return ''.join([name.capitalize() for name in names])


def find_reference_id(ref: str):
    if 'schemas' in ref:
        ref_attr = ref.split('/')[-1]
        return ref_attr
    return None


def find_reference_obj(ref: str):
    ref_attr = ref.split('/')[-1]
    obj_ref = YAML_FILE.get(ref_attr)
    if obj_ref is None:
        raise ValueError(f"Unknown reference {ref} in yaml swagger file")
    return obj_ref


def compose_work_folder(sub_folder='', ext_dir=''):
    if ext_dir:
        if sub_folder.startswith('/'):
            path = ext_dir
        else:
            path = os.path.join(ext_dir, sub_folder)
    else:
        path = os.path.join(MODULE_FOLDER, sub_folder)
    return path


def is_primitive(data: dict) -> bool:
    if data.get('type') in SWAGGER_TYPES:
        return True
    return False


def assign_primary_keys(description: str, attr_name: str, required: list) -> List[str]:
    msg = f'Missing $primary_keys in description field for array attribute {attr_name}.'
    if description is None:
        if required:
            log.debug(msg + f' Substituted by required {required}.')
        else:
            log.warning(msg)
        return []
    keys = description.split('$primary_keys')
    if len(keys) == 1:
        if required:
            log.debug(msg + f' Substituted by required {required}.')
        else:
            log.warning(msg)
        return []
    keys = keys[-1]
    if keys.startswith('(') and keys.endswith(')'):
        f_keys = keys.lstrip('(').rstrip(')')
        return f_keys.split(',')
    else:
        log.error(f'{attr_name}: Primary keys missing opening or closing bracket e.g.: $primary_keys(key_a,key_b)')
        return []


def get_import_line_new(id_name: str, namespace='split', file_name=''):
    if namespace == 'unique':
        package = file_name
    else:
        package = id_name
    return f'from .{package} import {align_object_name(id_name)}\n'


def add_to_import(id: str, sub_module='', namespace='split', file_name=''):
    # add to import list of submodule
    global components_imports
    global request_body_imports
    global response_imports
    global primitive_imports
    if sub_module == '':
        components_imports.append(get_import_line_new(id, namespace, file_name))
    elif 'primitive' in sub_module:
        primitive_imports.append(get_import_line_new(id, namespace, file_name))
    elif 'request_body' in sub_module:
        request_body_imports.append(get_import_line_new(id, namespace, file_name))
    elif 'responses' in sub_module:
        response_imports.append(get_import_line_new(id, namespace, file_name))


def yaml_parser(yaml: dict, ext_dir: str):
    dir_check(compose_work_folder(MODULE_FOLDER, ext_dir), del_files=True)
    dir_check(compose_work_folder(PRIMITIVE_FOLDER, ext_dir), del_files=True)
    dir_check(compose_work_folder(EXAMPLES_FOLDER, ext_dir), del_files=True)
    dir_check(compose_work_folder(RESPONSES_FOLDER, ext_dir), del_files=True)
    dir_check(compose_work_folder(REQUEST_BODY_FOLDER, ext_dir), del_files=True)
    create_definition(yaml['components'], ext_dir)
    generate_inits(primitive_imports, ext_dir, sub_module=PRIMITIVE_FOLDER)
    generate_inits(components_imports, ext_dir)
    create_paths(yaml['paths'], ext_dir)
    generate_inits(response_imports, ext_dir, sub_module=RESPONSES_FOLDER)
    generate_inits(request_body_imports, ext_dir, sub_module=REQUEST_BODY_FOLDER)


def create_definition(yaml_dict: dict, ext_dir: str) -> None:
    log.debug('Building openapi components into the cache')
    load(yaml_dict['schemas'])
    for id, schema in yaml_dict['schemas'].items():
        generate_struct(id, schema, ext_dir)


def generate_struct(id: str,
                    yaml: dict,
                    ext_dir: str = '',
                    sub_module: str = '',
                    namespace: str = 'split',
                    root: str = '',
                    level: int = 0):
    if root == '':
        root = id
    data = yaml
    ext_dir = ext_dir
    sub_module = sub_module
    namespace = namespace
    root = root
    level = level
    queue = []
    counter = 0
    while True:
        if queue:
           params = queue.pop()
           id = params[0]
           data = params[1]
           ext_dir = params[2]
           sub_module = params[3]
           namespace = params[4]
           root = params[5]
           level = params[6]
        elif counter > 0:
            break
        counter += 1
        if data.get('type') == 'number':
            generate_primitive(id, data, ext_dir)
        elif data.get('type') == 'string':
            generate_primitive(id, data, ext_dir)
        elif data.get('type') == 'boolean':
            generate_primitive(id, data, ext_dir)
        elif data.get('type') == 'object':
            queue = generate_object(id, data, ext_dir, sub_module, namespace, root, level)
        elif data.get('type') == 'array':
            id, data, sub_module = generate_array(id, data, ext_dir)
            queue.append((id, data, "", sub_module, 'split', '', 0, ''))
            continue
        elif one_of := data.get('oneOf'):
            generate_oneof(id, one_of, ext_dir)
        else:
            print('Error: Not generated attribute:' + id)


def generate_oneof(id: str, data: Any, ext_dir: str = ''):
    if not isinstance(data, list):
        raise ValueError(f'Unsupported type of {type(data)} of `OneOf` structure in {id}')
    out = list()
    out.append(f"class {align_object_name(id)}():\n\n")
    out.append("    one_of = [\n")
    p_keys = None
    for item in data:
        if ref := item.get('$ref'):
            obj_name = align_object_name(find_reference_id(ref))
        else:
            _, data_desc, submodule = generate_array(f"{id}_inner", item, ext_dir, RESPONSES_FOLDER, namespace='unique')
            obj_name = align_object_name(f'{id}_inner')
            if desc := data_desc.get('description'):
                p_keys = assign_primary_keys(desc, id, data_desc.get('required', []))
        out.append(f"        '{obj_name}',\n")
    out.append("    ]\n\n")
    if p_keys:
        out.append(f"    primary_keys = {str(p_keys)}\n\n")
    add_to_import(id)
    save_lines_to_pymodule(out, ext_dir, RESPONSES_FOLDER, id, 'a')


def create_paths(paths: dict, ext_dir: str):
    for id, schema in paths.items():
        generate_endpoints(id, schema, ext_dir)


def generate_inits(lines: list,
                   ext_dir: str = '',
                   sub_module=''):
    global EXT_DIR
    EXT_DIR = ext_dir
    # lines = sorted(lines)
    lines.append("from cpme_api.api.feature.models import set_data_validation\n")
    if sub_module == '':
        lines.append("from .responses import *\n")
        lines.append("from .primitive import *\n")
        lines.append("from .request_body import *\n")

    lines = list(set(lines))
    lines.sort()
    cls_names = [l.rsplit(' ')[-1].rstrip('\n') for l in lines if '*' not in l]
    lines.append(f'\n\n__all__ = {sorted(list(cls_names))}\n')
    #out.append(meta_info_date())
    #out.append(meta_info_source())

    save_lines_to_pymodule(lines,
                           ext_dir,
                           sub_module=sub_module,
                           file_name='__init__')


def generate_primitive(id: str, data: dict, ext_dir: str = '') -> None:
    print('PRIMITIVE: ' + id)
    out = list()
    out.append(f'"""\n{data.get("description")}\n"""\n\n\n')
    out.append(f"class {align_object_name(id)}(BaseContent):\n\n")
    out.append(f"    _primitive = '{data['type']}'\n\n")
    if enum := data.get('enum'):
        out.append(f"    _enum = {str(enum)}\n\n")
    out.append(f"    def __init__(self):\n")
    example = data.get('example')
    if isinstance(example, str):
        out.append(f"        self.example = '{data.get('example')}'\n")
    else:
        out.append(f"        self.example = {data.get('example')}\n")
    module = list()
    module.append(f'from cpme_api.api.feature.models import BaseContent\n')
    module.append('\n\n')
    module.extend(out)
    add_to_import(id, PRIMITIVE_FOLDER)
    save_lines_to_pymodule(module, ext_dir, PRIMITIVE_FOLDER, id)


def generate_properties(id, properties: dict):
    out = list()
    for attr, value in properties.items():
        out.append('\n')
        out.append(f'    @property\n')
        out.append(f'    def {attr}(self):\n')
        out.append(f'        return self._{attr}\n\n')
        out.append(f'    @{attr}.setter\n')
        out.append(f'    def {attr}(self, value):\n')
        out.append(f'        self._assign("{attr}", value)\n')
        if "portfolio_components" in id:
            out.append(f'        if not self.type:\n')
            out.append(f'            self.type = "{attr}"\n')
    return out


def generate_object(id: str,
                    data: dict,
                    ext_dir: str = '',
                    sub_module: str = '',
                    namespace: str = 'split',
                    root: str = '',
                    level: int = 0) -> tuple:
    assert namespace in ['split', 'unique'], f"Invalid {namespace} use `split` or `unique`"
    if id.endswith('_200'):
        id = id.rstrip('_200')
    if root.endswith('_200'):
        root = root.rstrip('_200')
    out = list()
    out.append(f'"""\n{data.get("description")}\n"""\n\n\n')
    if 'response' in sub_module:
        if not id.startswith('resp'):
            id = 'resp_' + id
    elif 'request_body' in sub_module:
        if not id.startswith('body'):
            id = 'body_' + id
    print('Object: ' + id)
    out.append(f"class {align_object_name(id)}(BaseContent):\n\n")
    properties = data.get('properties')
    out.append(f"    _swagger_types = " + '{\n')
    queue_objects = []
    file_name = copy(id)
    for attr in sorted(properties.keys()):
        if ref := properties[attr].get('$ref'):
            out.append(f"        '{attr}': '{align_object_name(find_reference_id(ref))}',\n")
        else:  # Parameter
            if properties[attr].get('type') == 'array':
                if ref := properties[attr].get('items').get('$ref'):
                    obj_name = align_object_name(find_reference_id(ref))
                else:
                    if id == attr:
                        new_id = f"{attr}_{level}"
                    elif level >= 0:
                        # merge nested structures into the same namespace file
                        namespace = 'unique'
                        file_name = root if root else id
                        new_id = f"{root}_{attr}"
                    else:
                        new_id = f"{root}_{attr}"
                    if root == '':
                        # workaround for _inner structures
                        root = id
                    if 'response' in sub_module:
                        new_id = 'resp_' + new_id
                    elif 'request_body' in sub_module:
                        new_id = 'body_' + new_id
                    obj_name = align_object_name(new_id)
                    queue_objects.append((new_id,
                                          properties[attr]['items'],
                                          ext_dir,
                                          sub_module,
                                          namespace,
                                          root,
                                          level + 1,
                                          file_name))
                out.append(f"        '{attr}': 'list[{obj_name}]',\n")
            else:
                out.append(f"        '{attr}': '{properties[attr].get('type')}',\n")

    if namespace == 'unique':
        # merge data structures into a same file_name
        file_name = root if root else id

    res = {}
    for attr, val in properties.items():
        if ref := properties[attr].get('$ref'):
            res[attr] = find_reference_obj(ref)
            res[attr].update({'$ref': align_object_name(find_reference_id(ref))})
        else:
            res[attr] = val
    properties = res
    out.append(f"    " + '}\n\n')
    out.append(f"    _default_values = " + '{\n')
    for attr in sorted(properties.keys()):
        if properties[attr].get('type') in ['object', 'array']:
            type_link = properties[attr].get('example', 'object')
            if isinstance(type_link, list):
                out.append(f"        '{attr}': {type_link},\n")
            else:
                out.append(f"        '{attr}': '{type_link}',\n")
        elif 'csv' in attr:
            out.append(f"        '{attr}': \"\"\"{properties[attr].get('example')}\"\"\",\n")
        else:
            # check type of example value
            e_val = properties[attr].get('example')
            if 'date' in attr:
                out.append(f"        '{attr}': '{e_val}',\n")
            elif isinstance(e_val, (int, float)):
                out.append(f"        '{attr}': {e_val},\n")
            else:
                out.append(f"        '{attr}': '{e_val}',\n")
    out.append(f"    " + '}\n\n')

    if req := data.get('required'):
        out.append(f"    _required = {str(req)}" + '\n\n')

    if p_keys := assign_primary_keys(data.get('description'), id, data.get('required', [])):
        out.append(f"    _primary_keys = {str(p_keys)}\n\n")

    if 'csv' in id:
        out.append(f"    def __init__(self, csv=''):\n")
    else:
        out.append(f"    def __init__(self, **kwargs):\n")
    for attr in sorted(properties.keys()):
        out.append(f"        self._{attr} = None\n")
    if 'csv' in id:
        out.append(f"        super({align_object_name(id)}, self).__init__(csv=csv)\n")
    else:
        out.append(f"        super({align_object_name(id)}, self).__init__(**kwargs)\n")
    module = list()
    if namespace == 'split' or level == 0:
        module.append(f'from cpme_api.api.feature.models import BaseContent\n')
    module.append('\n\n')
    module.extend(out)
    module.extend(generate_properties(id, properties))
    add_to_import(id, sub_module, namespace, file_name)
    save_lines_to_pymodule(module,
                           ext_dir,
                           sub_module=sub_module,
                           file_name=file_name,
                           mode='w' if namespace == 'split' else 'a')
    return queue_objects


def generate_array(id: str, data: dict, ext_dir: str = '', sub_module: str = '', namespace: str = 'split'):
    out = list()
    print('ARRAY: ' + id)
    out.append(f'"""\n{data.get("description")}\n"""\n\n\n')
    out.append(f"class {align_object_name(id)}(BaseContent):\n\n")
    properties = data.get('properties')
    if properties:
        ValueError(f"Swagger error: `properties` defined in `array` for {id}")
    if not data.get('items'):
        ValueError(f"Swagger error: missing `items` in `array` for {id}")
    p_keys = assign_primary_keys(data.get('description'), id, [])
    if p_keys:
        if not isinstance(data['items'], dict):
            ValueError(f"Definition missmatch: private_keys {p_keys} is defined for array {id} but missing nested object")
        p_keys = data.get('description')

    if ref := data.get('items').get('$ref'):
        obj_name = find_reference_id(ref)
        data = find_reference_obj(ref)
    else:
        obj_name = id + '_' + 'inner'
        data = data.get('items')
    if p_keys:
        data['description'] = p_keys
    out.append(f"    _swagger_types = " + '{\n')
    out.append(f"        'ref': 'list[{align_object_name(obj_name)}]',\n")
    out.append("    }\n\n")
    out.append(f"    def __init__(self):\n")
    out.append(f"        super({align_object_name(id)}, self).__init__()\n")
    module = list()
    module.append(f'from cpme_api.api.feature.models import BaseContent\n')
    module.append('\n\n')
    module.extend(out)
    add_to_import(id, sub_module, namespace, id)
    save_lines_to_pymodule(module,
                           ext_dir,
                           sub_module=sub_module,
                           file_name=id,
                           mode='w' if namespace == 'split' else 'a')

    if is_primitive(data):
        sub_module = 'primitive'
    return obj_name, data, sub_module


def generate_endpoints(id: str, data: dict, ext_dir: str = ''):
    if 'get' in data:
        generate_get_request(id, data['get'], ext_dir)
    elif 'post' in data:
        generate_post_request(id, data['post'], ext_dir)
    else:
        # TODO define YAML parser  exeption
        raise ValueError(f"Unsupported path {id} in swagger yaml")


def generate_get_request(id: str, data: dict, ext_dir: str) -> list:
    generate_response(id.lstrip('/'), data, 'get', ext_dir)


def generate_response(id: str, data: dict, method: str, ext_dir: str) -> list:
    # TODO decorator for checking None data
    assert isinstance(data, dict), f'Swagger Parser error: Missing `{method}` section for {id} path'
    responses = data.get('responses')
    if responses is None:
        raise ValueError(f"SP error: Missing `responses` section for get for {id} path")
    for res in responses:
        id = id.rstrip('/{param}')
        generate_content(f"{id}_{res}", responses[res], RESPONSES_FOLDER, ext_dir)


#@swagger_check('application/json')
def generate_content(id: str, data: dict, sub_folder: str, ext_dir: str) -> None:
    generate_example(id, data['content']['application/json'], ext_dir)
    data = data['content']['application/json']['schema']
    # if ref := data.get('$ref'):
    #    data = find_reference_obj(ref)
    generate_struct(f"{id}",
                    data,
                    ext_dir=ext_dir,
                    sub_module=sub_folder,
                    namespace='unique',
                    root=id)


#@swagger_check()
def generate_example(id: str, data: dict, ext_dir: str) -> None:
    if 'example' not in data:
        return
    generate_example_module(id, data['example'], ext_dir)


def generate_example_module(id: str, data: dict, ext_dir: str) -> None:
    out = list()
    print('New Example Constant: ' + id)
    out.append(f"\n\n{id} = {{\n")
    out_j = json.dumps(data, indent=4, sort_keys=True)
    out_j = out_j.replace('false', "'false'")
    out_j = out_j.replace('true', "'true'")
    out_j = out_j.replace('null', "'null'")
    out.extend(out_j.lstrip('{\n'))
    save_lines_to_pymodule(out,
                           ext_dir,
                           sub_module=EXAMPLES_FOLDER,
                           file_name=f'examples',
                           mode='a')


def generate_post_request(id: str, data: dict, ext_dir: str) -> list:
    id = id.lstrip('/')
    id = id.replace('/', '_')
    # TODO decorator for checking None data
    assert isinstance(data, dict), f'Swagger Parser error: Missing `method` section for {id} path'
    bodies = data.get('requestBody')
    if bodies is None:
        raise ValueError(f"SP error: Missing `requestBody` section for get for {id} path")
    generate_content(id, bodies, REQUEST_BODY_FOLDER, ext_dir)
    for res in data['responses']:
        generate_content(f"{id}_{res}", data['responses'][res], RESPONSES_FOLDER, ext_dir)


def save_lines_to_pymodule(lines: list,
                           ext_dir: str = '',
                           sub_module: str = '',
                           file_name='',
                           mode='w'):
    assert mode in ['w', 'a'], f"Invalid mode {mode} use `w` or `a`"
    if ext_dir:
        path = ext_dir
    else:
        path = MODULE_FOLDER

    if sub_module:
        path += os.path.join(sub_module)
    if not os.path.isdir(path):
        raise Exception(f"Directory not exists {path}")
    path += os.path.join(f'{file_name}.py')
    with open(path, mode) as f:
        f.writelines(lines)
        print(f'Generating {path}')


def cls_names_itter(module):
    for cls in (module.__dict__[file] for file in module.__all__):
        if cls.__name__ == 'set_data_validation':
            continue
        yield cls

        # cls_name = getattr(MODEL_MODULE, 'kolo', None)


class SwaggerAttributes(object):
    def __init__(self, ext_dir=None):
        self._ext_dir = ext_dir

    def _get_package_path(self, sub_module=''):
        package_path = 'cpme_api.api.models'
        if self._ext_dir:
            package_path = self._ext_dir.replace('/', '.').lstrip('.')

        if sub_module:
            package_path = package_path + '.' + sub_module.rstrip('/')
        return package_path

    def _get_module_object(self, sub_module=''):
        try:
            module = importlib.import_module(self._get_package_path(sub_module))
        except ModuleNotFoundError:
            raise ValueError(f"Unknown path {self._ext_dir}")
        return module

    def get_swagger_primitive_names(self, s_type=''):
        return [
            cls_name.__name__
            for cls_name in cls_names_itter(self._get_module_object(PRIMITIVE_FOLDER))
            if cls_name.is_primitive(s_type)
        ]

    def get_swagger_object_names(self):
        return [
            cls_name.__name__
            for cls_name in cls_names_itter(self._get_module_object())
            if not cls_name.is_primitive()
        ]

    def get_swagger_array_names(self):
        return [
            cls_name.__name__
            for cls_name in cls_names_itter(self._get_module_object(PRIMITIVE_FOLDER))
            if cls_name.is_array()
        ]

    def get_swagger_body_names(self):
        return [
            cls_name.__name__
            for cls_name in cls_names_itter(self._get_module_object(REQUEST_BODY_FOLDER))
            if not cls_name.is_primitive()
        ]

    def get_swagger_response_names(self):
        return [
            cls_name.__name__
            for cls_name in cls_names_itter(self._get_module_object(RESPONSES_FOLDER))
            if not cls_name.is_primitive()
        ]
