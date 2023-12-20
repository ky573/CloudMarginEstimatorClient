import click
import sys
import webbrowser
from model_gen.cli.utils import CONTEXT_SETTINGS, get_comet_sysenv, show_logo
from model_gen.config import settings, Environment, PROJECT_ROOT
from .update_cli import update_cli
import io

# need to change namespaces
from cpme_api.api.feature.utils import data_folder_fix
from model_gen.common import host_from_url


MAIN_TEXT = """
This CLI provides data fetching from CPME resources with user defined options for quick data check of CPME API
"""


class HelpfulCmd(click.Command):
    def format_help(self, ctx, formatter):
        click.echo("My custom help message")


class RichGroup(click.Group):
    def format_help(self, ctx, formatter):
        sio = io.StringIO()
        console = rich.Console(file=sio, force_terminal=True)
        console.print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:")
        formatter.write(sio.getvalue())


@click.group(cls=RichGroup, context_settings=CONTEXT_SETTINGS, name="Comet", chain=True)
def cli():
    pass


@cli.command(short_help="Open the cpme UI for specific environment.")
@click.option(
    "--env",
    "-e",
    type=str,
    help="Select environment. "
         f"Default input is used from setting toml file. "
         f"Available keys: \n{Environment.environments()}."
         f"[default: {settings.current_env}]",
    default=Environment.alias(settings.current_env)
)
def web(env):
    """Open the online cpME via default browser."""
    new_settings = settings(env)
    click.echo(f"ENV: {new_settings.current_env} Opening {host_from_url(new_settings.url)}")
    webbrowser.open(host_from_url(new_settings.url))
    return 0


@cli.command(short_help="Open html documentation of COMET usage.")
def tutorial():
    """Open the html tutorial via default browser."""
    index_path = f'{PROJECT_ROOT}/docs/build/html/index.html'
    click.echo(index_path)
    webbrowser.open(f'file://{index_path}')
    return 0


@cli.command()
def info():
    """More information about CLI."""
    click.echo(
        "Comet is a Python test tool for rapid validation and data requests\n"
        "of cpME API. The main goal is simple api control via command line \n"
        "and library with rich functions and generated data models.\n"
        "The code generator is some kind of tree resource object model (like DOM)\n"
        "from swagger definition file of open api standard. The tool can be used by\n"
        "developers and testers to avoid manual routines and provide an api specification\n"
        "from CLI. The library helps to create regression tests with pytest framework\n"
        "for corresponding environment. The examples of library usage you can find in ./example \n"
        "folder or you can open html tutorial with command 'python -m cpme_api tutorial'"
    )
    return 0


@cli.command('config', short_help='Show configuration parameters of environment.')
@click.option(
    "--env",
    "-e",
    type=str,
    help="Request of corresponding endpoint with parameter.\n"
         f"Default input is used from setting toml file. Available keys: \n{Environment.environments()}",
    show_default=True,
    default=settings.env_for_dynaconf.lower()
)
def list_settings(env):
    _settings = settings(env)
    msg = list()
    conf = ';'.join(filter(lambda x: x is not None, _settings.settings_file))
    msg.append(f'Available environments: {_settings.environments_for_dynaconf}')
    msg.append(f'Available from system env:')
    msg.extend(get_comet_sysenv())
    msg.append(f'\nSetting for current environment <{_settings.current_env}>:')
    msg.append(f'SWAGGER_YAML_DEFINITION_FILE = {_settings.SWAGGER_YAML_FILE}')
    msg.append(f'SNAPSHOTS_FOLDER = {data_folder_fix(_settings.SNAPSHOTS_FOLDER)}')
    msg.append(f'REQUESTS_FOLDER = {data_folder_fix(_settings.REQUESTS_FOLDER)}')
    msg.append(f'RESPONSES_FOLDER = {data_folder_fix(_settings.RESPONSES_FOLDER)}')
    msg.append(f'SNAPTOOL_FOLDER = {data_folder_fix(_settings.SNAPTOOL_FOLDER)}')
    msg.append(f'SCENARIO_PATH_FOLDER = {_settings.SCENARIO_PATH_FOLDER}')
    msg.append(f'URL_API = {_settings.URL}')
    msg.append(f'REQUEST_TIMEOUT = {_settings.REQUEST_TIMEOUT}')
    msg.append(f'LOGGING = {_settings.LOGGING}')
    msg.append(f'PRECISION_POINTS = {_settings.PRECISION_POINTS}')
    msg.append(f'cert_for_verify = {_settings.cert_for_verify()}')
    if hasattr(settings, 'api_key'):
        msg.append(f'api_key = {settings.api_key}')
    msg.append(f'Configuration source: {conf}')
    msg.append('\nNote: You can overwrite configuration source via COMET_CONFIG variable with optional configuration toml file.')
    msg.append('\nNote: It is recommended to define env variable ENVIRONMENT_FOR_COMET for environment switch.'
               'Use: export ENVIRONMENT_FOR_COMET=development')
    click.echo('\n'.join(msg))
    return 0


def main():
    show_logo()
    cli_collection = click.CommandCollection(sources=[cli,
                                                      update_cli],
                                             help=MAIN_TEXT)
    return sys.exit(cli_collection())
