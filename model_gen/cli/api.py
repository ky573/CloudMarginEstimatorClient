import copy
import sys
import click
from model_gen import factory
from model_gen.factory import list_all_attributes
from model_gen.config import settings, Environment
from cpme_api.api import CpmeApi
from cpme_api.api.input import PostInputs, GetInput, merge_body_from
from cpme_api.api.feature import (find_attr_in_response,
                               find_attr_in_body,
                               check_alias)
from cpme_api.api.definition import find_any, get_assignments, Object, array_by_name
from cpme_api.api.parser import Parameter, Attribute
from cpme_api.api.endpoints import GET_ENDPOINTS, POST_ENDPOINTS, GET, POST
from cpme_api.api.eval import validate, ApiException
from cpme_api.api.feature import Timer, get_file_size, fancy
from cpme_api.api.feature.resource import Resource
from cpme_api.api.feature.utils import (json_to_file,
                                     body_request_file_name,
                                     dir_check,
                                     update_prefix_content,
                                     UnitSize,
                                     data_folder_fix)
from model_gen.common import data_to_csv, str_to_double_quotes
from .utils import get_component_type
import os
import pprint
from itertools import groupby
from typing import List, Dict, Tuple, Union, Type


def list_endpoints(endpoint: str, env, verbose: False):
    msg = []
    if not endpoint:
        msg.append(f'You can choose endpoint name: GET:{GET_ENDPOINTS} POST:{POST_ENDPOINTS}')
    else:
        ep = endpoint[0]
        try:
            apis, inputs = factory.loader()
            list_endpoint(endpoint[0], apis[ep], inputs[ep], env, verbose)
        except KeyError:
            msg.append(f'E: Unknown endpoint {endpoint[0]}.')
            msg.append(f' You can choose endpoint name: GET:{GET_ENDPOINTS} POST:{POST_ENDPOINTS}')
    print(''.join(msg))
    # for ep, resource in apis.items():
    #    list_endpoint(ep, resource)


def format_list(items: List[str]) -> str:
    return ','.join([f"'{n}'" for n in items])


def list_endpoint(ep: str, resource: Resource, input_p: Union[PostInputs, GetInput], env, verbose):
    msg = list()
    msg.append(f'ENV:{settings(env).current_env}  URL: {settings(env).url}')
    msg.append(f"\n<{ep}>: {'GET' if resource.get else 'POST'}")
    if get := resource.get:
        msg.append("  Description:")
        msg.append(f" {get.description}\n")
        msg.append("  Parameters:")
        msg.append(f"    HEADER: {get.head_params}")
        if get.query_params:
            msg.append(f"    QUERY PARAMETERS: {format_list(get.query_params)}")
        if get.path_params:
            msg.append(f"    PATH PARAMETERS: {format_list(get.path_params)}")
        if 'extrafields' in get.query_params:
            msg.append(f"    EXTRA_FIELDS:\n"
                       f"      {format_list(input_p.get_extra_fields())}")
        if items := [p.id for p in get.params.values() if p.required]:
            msg.append(f"    *Required: {format_list(items)}")
        msg.append(f"\n  Response:")
        for resp in get.responses:
            msg.append(f"    [{resp}] example:")
            pp = pprint.PrettyPrinter(indent=4)
            msg.append(f"{pp.pformat(get.responses[resp].examples)}")
        if verbose:
            print('\n'.join(msg))
            print('\nJSON:')
            fancy(get.responses[resp].examples)
        else:
            print('\n'.join(msg))
    elif post := resource.post:
        msg.append("  Description:")
        if verbose:
            print(post._description)
        msg.append(f"    {post.summary}\n")
        msg.append("  Parameters:")
        msg.append(f"    HEADER: {format_list(list(post.params.keys()))}")
        for item in post.params.values():
            if item.required:
                msg.append(f"      *Required: {item.required}")
        msg.append(f"\n  Request Body:")
        msg.append(f"    {format_list(post.request_body.schema.get_properties())}")
        for item in post.request_body.schema.required:
            msg.append(f"    *Required: {item}")
        if 'portfolio_components' in post.request_body.schema:
            msg.append(f"\n     *Portfolio Components: "
                       f"{', '.join(post.request_body.schema['portfolio_components'].get_properties())}")
        msg.append(f"\n  Response Keys:")
        for resp in post.responses:
            msg.append(f"    {format_list(post.responses[resp].schema.get_properties())}")
        print('\n'.join(msg))
        if verbose:
            click.echo(f"\nRequest Body Example:")
            fancy(post.request_body.examples)
            click.echo(f"\nResponse Example:")
            fancy(post.responses[200].examples)


def find_attribute(attr_name: str, silent: bool, to_json: bool, export: bool, prefix: str, ext_dir: str):
    """
    Full search of any attribute in cache with data definition content.
    There are various attributes like Parameter or Schema defined values
    or attributes located in tree structure of particular resource content.
    An attribute can be part of query parameter, response data object or
    request body data object. Same objects can be inner of another object :-)
    """

    if attr_name == '?':
        list_all_attributes(ext_dir)
        sys.exit(0)

    if attr_name == 'ep':
        click.echo(f'Endpoints: GET={GET_ENDPOINTS} POST={POST_ENDPOINTS}')
        sys.exit(0)

    res_array, msg, obj = search_attribute(attr_name)

    if not silent:
        if alias := check_alias(attr_name):
            click.echo(f'NOTE: {attr_name} refers to {alias}')
        if attr_name == 'portfolio_components' and (f_body := find_attr_in_body(apis, attr_name, full=True)):
            msg.append(f'\nIt is BODY REQUEST object for resources:')
            for ep, body in f_body.items():
                for loc in body.keys():
                    msg.append(f'{ep}')
                    msg.append(f"  PORTFOLIO COMPONENTS: {body[loc].get_properties()}")
                    msg.append(f"  REQUIRED: {body[loc].required}")
                    msg.append(f"  DESC: {body[loc].desc}")
        print('\n'.join(list(filter(lambda x: x != "", msg))))
        if attr_name != 'portfolio_components' and (f_body := find_attr_in_body(apis, attr_name)):
            print(f'\nLocated in BODY request for resources:')
            pprint.pprint(f_body)
        if f_resp := find_attr_in_response(apis, attr_name):
            print(f'\nLocated inside response structure of resources:')
        if f_resp:
            pprint.pprint(f_resp)
    if to_json:
        if res_array:
            fancy({attr_name: res_array.value()})
            # fancy({attr_name: example_of_object(apis, attr_name).value()})
        if obj:
            if 'csv' in attr_name:
                fancy(obj.value())
            else:
                fancy({attr_name: obj.value()})
    if (obj and export and ('_csv' in attr_name))\
            or ((obj and 'csv' in obj) and export):
        export_to_csv(prefix, obj, attr_name)
    return None


def export_to_csv(prefix: str, obj: Type[Attribute], attr_name: str):
    if prefix:
        prefix = prefix + '_'
    file_name = f"{prefix}{attr_name}.csv"
    path = os.path.join(data_folder_fix(settings.requests_folder), file_name)
    dir_check(data_folder_fix(settings.requests_folder))
    if isinstance(obj, Object):
        data = obj['csv'].value()
    else:  # Parameter
        data = obj.value()
    data_to_csv(data.split('\\n'), path)
    click.echo(f'CSV content example stored into {path}. size={get_file_size(path, 2)}kB')


def search_attribute(attribute: str):
    msg = []
    res_list = []
    obj = None
    # search in query parameters
    if res_param := find_any(attribute, fill='param'):
        msg.extend(compose_info(res_param['parameter'], 'param'))
        res_list.append(res_param)
        obj = res_param.get('parameter')
    # search in schema definition
    if res_schema := find_any(attribute, fill='schema'):
        if not res_schema.get('schema').is_equal(res_param.get('parameter')):
            msg.extend(compose_info(res_schema['schema'], 'schema'))
            res_list.append(res_schema)
            obj = res_schema.get('schema')
    # search inside data structures
    if res_inner := find_any(attribute, fill='inner'):
        child_nodes = list(res_inner.keys())
        attr = res_inner[child_nodes[0]]
        if not (attr.is_equal(res_param.get('parameter')) or attr.is_equal(res_schema.get('schema'))):
            msg.extend(compose_info(attr, 'inner', child_nodes))
            res_list.append(res_inner)
    # check if it is defined in response
    # find in arrays
    res_array = array_by_name(attribute)
    # check if defined in request body
    if not all(res_list):
        click.echo(f'Attribute not found :-(')
    return res_array, msg, obj


def process_attribute(attribute, verbose: bool, store: str):
    return 0


def compose_info(attr: dict, fill: str = None, child_node: list = []):
    assert fill in ['param', 'schema', 'inner', 'endpoint', None], f'Undefined filter value {fill}'
    msg = []
    if isinstance(attr, Parameter):
        if fill in ['param']:
            msg.append(f'\nThe query {fill} of open api specification.')
        if isinstance(attr, Parameter) and fill in ['schema', 'inner']:
            msg.append(f'\nThe child nodes {fill} of open api specification.')
        msg.append(f'  Name: {attr.id} <{attr.__class__.__name__}>')
        msg.append(f"  Doc: {attr.get('description')}")
        msg.append(f'  Type: {attr.type}')
        msg.append(to_dict_str('example', attr))
        msg.append(to_dict_str('in', attr))
        msg.append(to_dict_str('default', attr))
        if attr.is_array:
            msg.append(f'  IsArray: {attr.is_array}')
        msg.append(to_dict_str('is_array', attr))
        if ret := get_assignments(attr.id, from_path=True):
            msg.append(f'\n It is query parameter for endpoints: {ret}')
        if ret := get_assignments(attr.id):
            msg.append(f'\n It is nested in these objects/arrays: {ret}')

    if isinstance(attr, Object):
        msg.append(f'\nObject Located in Object of open api specification.')
        msg.append(f'Name: {attr.id} <{attr.__class__.__name__}>')
        msg.append(f"Doc: {attr.desc if attr.desc else ''}")
        msg.append(f'Type: {attr.type}')
        msg.append(f'Array: {attr.is_array}')
        msg.append(f'Required: {attr.required}')
        for item in attr.get_properties():
            attr.get_type(item)
            msg.append(f"\nAttribute: {item}")
            msg.append(f"\tType: {attr.get_type(item) if attr.get_type(item) else ''}")
            msg.append(f"\tDoc: {attr.get_description(item) if attr.get_description(item) else ''}")
            msg.append(f"\tExample: {attr.get_example(item) if attr.get_example(item) else ''}")
            if hasattr(attr[item], 'enum') and attr[item].enum:
                msg.append(f"\tEnum: {str_to_double_quotes(attr[item].enum)}")
    return msg


def to_dict_str(key: str, attribute):
    return f"  {key}: {str_to_double_quotes(attribute.get(key))}" if attribute.get(key) else ''


def api_request(endpoint: str,
                json_folder: str = None,
                params: dict = {},
                timeout: int = None,
                to_json=False,
                env=None,
                print_out=False,
                verbose=False,
                prefix='',
                check=True,
                from_merge=tuple(),
                file_name: str = '',
                compare: bool = False,
                out_file: str = '',
                only_body: bool = False):
    if not json_folder:
        json_folder = data_folder_fix(settings.snapshots_folder)
    if Environment.alias(env) == 'Unknown':
        click.echo(f'E: Unknown env {env}')
        return -1
    if endpoint in GET_ENDPOINTS:
        get_flag = True
    elif endpoint in POST_ENDPOINTS:
        get_flag = False
    else:
        click.echo(f'E: Unknown endpoint {endpoint}. You can choose: GET:{GET_ENDPOINTS} POST:{POST_ENDPOINTS}')
        return -1
    apis, inputs = factory.loader()
    api = apis[endpoint]
    if params == '?':
        click.echo(f'You can use {inputs[api.ep].query_params} or for header {inputs[api.ep].header_params}')
        return 0
    for k in params.keys():
        if params[k] == '?':
            click.echo(f'Use [ -p PARAM1 [-p PARAM2]] for query parameters or just PARAM '
                       f'for path parameter or --help or -p ? or -i/--info for hint.')
            return 0
        if 'business_date' in k:
            params[k] = int(params[k])
    timer = Timer()
    timer.start()
    click.echo(f'Environment<{env.upper()}> waiting for response... timeout='
               f'{timeout if timeout else settings.REQUEST_TIMEOUT}')
    response = None
    if get_flag:
        try:
            params = correct_params(params, inputs[endpoint])
            input_params = inputs[api.ep].get_default(**params)
            if verbose:
                click.echo('\nHEADER CONTENT:')
                fancy(api.get.get_header(input_params))
                fancy(input_params, 'QUERY_PARAMS:')
            if 'business_date' in input_params:
                click.echo(f"Waiting for request for bd={input_params['business_date']}. "
                           f"Historical requests can take a time.")
            response = api.get.sync_request(params=input_params,
                                            timeout=timeout,
                                            env=env)
            val = validate(response, env, input_params=params)
            click.echo(f'GET {response.url}')
            if not prefix:
                prefix = 'cli'
            # for indicative_margin only
            if res := input_params.get('include_component', 'false'):
                if res == 'true':
                    to_json = True
                else:
                    to_json = False
            if 'indicative_margin' in endpoint \
                    and 'business_date_from' in input_params \
                    and 'business_date_to' in input_params:
                to_json = True
            if to_json:
                path = val.to_json(file_prefix=prefix,
                                   file_dir=json_folder,
                                   verbose=verbose,
                                   out_file=out_file)
            else:
                path = val.to_csv(file_prefix=prefix,
                                  file_dir=json_folder,
                                  out_file=out_file)
            if path == '':
                # try to check XLS, XLSX content in header_params
                path = val.to_xls(file_prefix=prefix,
                                  file_dir=json_folder,
                                  out_file=out_file)
        except ApiException as api_exp:
            click.echo(f'E:{api_exp}')
            return -1
        except Exception as e:
            click.echo(f'E:{e.args}')
            return -1
        if not path:
            pass
            # click.echo('Try to store into xls/xlsx.')
            # path = val.to_xls()  # if format <> JSON try to check xls in header
        else:
            click.echo(f'Response stored into {path}. size={get_file_size(path)}MB duration={timer.get_time_str()}')
        if verbose:
            if hasattr(response, 'json'):
                fancy(response.json(), 'RESPONSE:')
            else:
                click.echo(response.text)
    else:  # post
        try:
            request_content = inputs[endpoint]
            # params = correct_params(params, request_content)
            request_body = request_content.load(prefix, check=check, env=env, file_name=file_name)
            if from_merge and request_body:
                request_body = merge_body_from(request_body, from_merge, check=check)
            if not request_body:
                click.echo('I: Skipping merge option')
            if verbose:
                click.echo('\nHEADER CONTENT:')
                fancy(api.post.get_header())
                click.echo('\nBODY CONTENT:')
                fancy(request_body)
            response = api.post.sync_request(timeout=timeout,
                                             env=env,
                                             json_body=request_body)
            val = validate(response, env, verbose=verbose)
            if compare:
                val.compare(prefix=prefix)
            else:
                val.to_json(file_dir=data_folder_fix(settings.RESPONSES_FOLDER),
                            file_prefix=prefix,
                            verbose=True,
                            out_file=out_file)
            click.echo(f'POST URL {response.url}')
        except ApiException as api_exp:
            click.echo(f'E:{api_exp}')
            return -1
        except Exception as e:
            click.echo(f'Exception: {e}')
            return -1
        if verbose and hasattr(response, 'json') and not only_body:
            click.echo('\nJSON RESPONSE:')
            fancy(response.json())


def load_from_file():
    pass


def ep_from_alias(alias: str, get_flag: bool):
    if get_flag:
        return getattr(GET, alias)
    else:
        return getattr(POST, alias)


def correct_params(params: dict, input_p: Union[GetInput, PostInputs]):
    if 'extrafields' in params:
        fields = params.pop('extrafields').split(',')
        if 'all' in fields:
            params['extrafields'] = input_p.get_extra_fields()
        else:
            params['extrafields'] = fields
    # workaround should be fix in Parameter class in default check
    new_params = copy.copy(params)
    for key in params:
        if isinstance(params[key], str) and ',' in params[key]:
            new_params[key] = params[key].split(',')
    return new_params


def list_snapshot_info(params: str, env: str):
    new_settings = settings(env)
    api = CpmeApi(set_validation=False)
    click.echo(f'ENV<{env.upper()}> waiting for response... timeout={new_settings.request_timeout}')
    try:
        response = api.snapshots_get(_env=env, _timeout=new_settings.request_timeout)
        res = response.json()['snapshots']
    except ApiException as api_exp:
        click.echo(f'E:{api_exp}')
        return -1
    except Exception as e:
        click.echo(f'E:{e.args}')
        return -1
    bd_list = [k for k, _ in groupby((x["business_date"] for x in res))]
    if params == 1:
        prev = bd_list[-2]
        bds = list(filter(lambda x: x["business_date"] == prev, res))
        click.echo(f'Snapshots for prev bd:{detect_snaphost(bds)}')
        return 0
    if params == 0:
        prev = bd_list[-1]
        bds = list(filter(lambda x: x["business_date"] == prev, res))
        click.echo(f'Snapshots for current bd:{detect_snaphost(bds)}')
        return 0
    else:
        bds = bd_list[-params:]
        bds = list(filter(lambda x: x["business_date"] in bds, res))
        click.echo(detect_snaphost(bds))
        return 0


def detect_snaphost(bds: List[dict]) -> Dict[Tuple[str, str], dict]:
    msg = ["\n\n"]
    for snap in bds:
        if snap['live'] is True:
            msg.append(f"business_date = {snap['business_date']} SOD:\n")
        else:
            msg.append(f"business_date = {snap['business_date']} EOD:\n")
        msg.append(f"\tlive = {snap['live']}\n")
        msg.append(f"\tcash_available = {snap['cash_available']}\n")
    return ''.join(msg)


def compose_body(endpoint: str,
                 kwargs: Dict[str, Union[None, List[str]]],
                 required=False,
                 to_json=False,
                 json_folder: str = None,
                 prefix: str = None):
    assert endpoint != '', 'Endpoint must exists'
    if prefix:
        prefix = update_prefix_content(prefix)
    if endpoint in GET_ENDPOINTS:
        click.echo(f'GET request {endpoint} does not support --with parameter. Use for POST requests.')
        return
    if not json_folder:
        json_folder = data_folder_fix(settings.requests_folder)
    _, _inputs = factory.loader()
    try:
        json_dict = _inputs[endpoint].build_body(kwargs, required)
        fancy(json_dict)
        if to_json:
            file_name = body_request_file_name(endpoint,
                                               get_component_type(kwargs),
                                               Environment.alias(settings.current_env),
                                               prefix)
            dir_check(json_folder)
            path = os.path.join(json_folder, file_name)
            json_to_file(json_dict, path)
            click.echo(f'Body request stored into {path}. size={get_file_size(path, UnitSize.KB)}kB')
    except ValueError as e:
        click.echo(f'E:{e.args}')
        msg = list()
        msg.append(f"Available attributes for body:")
        msg.append(f"    {format_list(_inputs[endpoint].body.get_properties())}")
        msg.append(f"\nUse -i for more info")
        click.echo(''.join(msg))
    except Exception as e:
        click.echo(f'E:{e.args}')
        return -1
    return 0
