import click
from comet.config import settings, Environment
from .api import (list_endpoints,
                  find_attribute,
                  api_request,
                  list_snapshot_info,
                  process_attribute,
                  compose_body)
from comet.api.feature.utils import data_folder_fix
from typing import List


@click.group(chain=True)
def resource_cli():
    pass


def validate(ctx, param, value):
    p_list = []
    if isinstance(value, tuple):
        for item in value:
            if '?' in item:
                return '?'
            elif item.count('=') != 1:
                raise click.BadParameter("format must be param=value or ? or you can set extrafields=all")
            p_list.append(item.split("="))
        return dict(p_list)
    """
    try:
        rolls, _, dice = value.partition("d")
        return int(dice), int(rolls)
    except ValueError:
        raise click.BadParameter("format must be 'NdM'")
    """


def str_to_list(value: str) -> List[str]:
    if '?' in value:
        return value.split('?')
    return [value]


def validate_with(ctx, param, value):
    if isinstance(value, str):
        if items := value.split(','):
            p_dict = {}
            for item in items:
                if '=' in item:
                    if (pair := item.split('=')) and len(pair) == 2:
                        p_dict[pair[0]] = str_to_list(pair[1])
                else:
                    p_dict[item] = None
            return p_dict
        raise click.BadParameter("Missing body parameter")
    else:
        return None


@resource_cli.command('api', short_help='cpME api interface (requests, validation, export, search)')
@click.option(
    "--info",
    "-i",
    "list_ep",
    help="Show info of proper endpoint.",
    is_flag=True,
    default=False
)
@click.option(
    "--dates",
    "-d",
    "list_dates",
    help="List available snapshots dates [options: 0 = current, 1 = prev, <number_of_last_bd>]",
    type=click.IntRange(0, 20),
    default=None
)
@click.option(
    "--find",
    help="Find attribute information. Use with '?' to list available attributes.",
    type=str,
    default=None
)
@click.option(
    "--to-json",
    "to_json",
    help="Export snapshots into .json file  [.csv is default]",
    is_flag=True,
    default=False
)
@click.option(
    "--print",
    "print_out",
    help="Print response content into stdout",
    is_flag=True,
    default=False
)
@click.option(
    "--verbose",
    "-V",
    "verbose",
    help="Show more detail",
    is_flag=True,
    default=False
)
@click.option(
    "--only-body",
    help="Use together with verbose and show only JSON body content.",
    is_flag=True,
    default=False
)
@click.option(
    "--silent",
    "-S",
    "silent",
    help="Obsolete, limited usage! Stop all info messages, show only exported data, useful with pipe command stream",
    is_flag=True,
    default=False
)
@click.option(
    "--required",
    "-R",
    "only_required",
    help="Use by --with command to generate only minimum required fields according to the specification",
    is_flag=True,
    default=False
)
@click.option(
    "--export",
    "body_export",
    help="Export body request input data into the json/csv",
    is_flag=True,
    default=False
)
@click.option(
    "--no-body-check",
    "check_flag",
    help="Disable default check of body json structure load. Useful for negative scenarios.",
    is_flag=True,
    default=False
)
@click.option(
    "--compare",
    "compare",
    help="Comparison between JSON response vs stored with --prefix command.",
    is_flag=True,
    default=False
)
@click.option(
    "--path",
    help=f"Full path where to save json response. [default: {data_folder_fix(settings.SNAPSHOTS_FOLDER)} for get results,"
         f" {data_folder_fix(settings.RESPONSES_FOLDER)} for post results]",
    type=str,
    default=''
)
@click.option(
    "--file-name",
    "-F",
    help=f"File name to find with body request content.",
    type=str,
    default='',
)
@click.option(
    "--out",
    "-O",
    "out_file",
    help=f"Output file name of response.",
    type=str,
    default='',
)
@click.option(
    "--prefix",
    help=f"The alias name for export files.",
    type=str,
    default='cli',
    show_default=True
)
@click.option(
    "--params",
    "-p",
    type=click.UNPROCESSED, #type=(str, str),
    multiple=True,
    callback=validate,
    help=f"Input parameters for query. You can use query parameters with option -p. For all `extrafields` use '-p extrafields all'. "
         f"For path parameters type just parameter name without -p. For hints use `-p ?`"
)
@click.option(
    "--body",
    "-b",
    'with_body',
    type=click.UNPROCESSED,
    callback=validate_with,
    help=f"Input parameters for response body. For DEFAULT[snapshot,portfolio_components=etd_csv?csv_json]"
)
@click.option(
    "--from-merge",
    "-M",
    'from_merge',
    multiple=True,
    type=str,
    help=f"Merge loaded body prefix file with prefix string or file name string"
         f" [example: --from-merge=TC-Currency or -M x-y_currency.json]"
)
@click.option(
    "--timeout",
    "-t",
    type=float,
    help=f"Request timeout. To wait forever for a response, use 0 value",
    show_default=True,
    default=settings.request_timeout
)
@click.option(
    "--env",
    "-e",
    type=str,
    help="Request of corresponding endpoint with parameter.\n"
         f"Default input is used from setting toml file. "
         f"Available keys: \n{Environment.environments()}."
         f"[default: {settings.current_env}]",
    default=Environment.alias(settings.current_env)
)
@click.argument('endpoint', nargs=-1, type=str, default=None)
def cmd2(list_ep,
         endpoint,
         find,
         path,
         params: dict,
         timeout,
         to_json,
         env,
         list_dates,
         print_out,
         silent,
         verbose,
         with_body,
         only_required,
         body_export,
         prefix,
         check_flag,
         from_merge,
         file_name,
         compare,
         out_file,
         only_body):
    """Commands of api section

    $ python -m cpme_api api products

    $ python -m cpme_api api products -p business_date=20220111 -p extrafields=instrument_type,currency -t 20

    $ python -m cpme_api api series -p products=FME,D2TE -p business_date=20220111

    $ python -m cpme_api api default_fund --body portfolio_components=etd_csv --prefix TC-001-df --to-json -V

    $ python -m cpme_api api ?

    $ python -m cpme_api api estimator -i -V

    $ python -m cpme_api api estimator --prefix TC-001-es
    """
    check_flag = not check_flag
    if list_dates is not None:
        return list_snapshot_info(list_dates, env)
    if timeout == 0:
        timeout = None
    if list_ep:
        list_endpoints(endpoint, env, verbose)
        return 0
    if find:
        attr = find_attribute(find.lower(), silent, to_json, body_export, prefix, path)
        return process_attribute(attr, verbose, path)
    if with_body:
        compose_body(endpoint[0],
                     with_body,
                     only_required,
                     to_json,
                     path,
                     prefix)
        return 0
    if endpoint:
        if len(endpoint) == 2:
            params.update({'q_path': endpoint[1]})
        endpoint = endpoint[0]
        api_request(endpoint,
                    path,
                    params,
                    timeout=timeout,
                    to_json=to_json,
                    env=env,
                    print_out=print_out,
                    verbose=verbose,
                    prefix=prefix,
                    check=check_flag,
                    from_merge=from_merge,
                    file_name=file_name,
                    compare=compare,
                    out_file=out_file,
                    only_body=only_body)
        return 0
    click.echo('Use --help for commands')
