import click
import os
from model_gen.config import settings
from model_gen.factory import generate_models


@click.group(chain=True)
def update_cli():
    pass


@update_cli.command('update', short_help='Generate request/response data classes.')
@click.option(
    "--yaml_file",
    "-y",
    "yaml_file_path",
    help="External source file name path.",
    type=str,
    default=settings.SWAGGER_YAML_FILE
)
@click.option(
    "--folder",
    "-f",
    type=str,
    help="Generate modules into another folder. [TEXT /path]",
    default=''
)
def cmd1(yaml_file_path,
         folder):
    """
    Regenerate data model classes according to the recent swagger
    yaml file definition with default values into cpme_api/api/models.
    The data objects are mutable dictionary based structures of
    body request for POST api endpoints.
    It helps to build JSON body request object during the runtime :-)
    usage:
        import cpme_api.api.models
        from cpme_api.api.models import Estimator
    """
    try:
        from comet.api.models import __date__
        from comet.api.models import __source__
        click.echo(f"Last date of object models update {__date__}.")
        click.echo(f"Models was generated from {__source__}.")
        click.echo(f"Models will be newly generated from {settings.SWAGGER_YAML_FILE}")
    except ImportError:
        click.echo('Missing cpme_api.api.models!')
    if not os.path.isfile(yaml_file_path):
        click.echo(f'E: File not found {yaml_file_path}')
        return -1
    if not folder and os.path.isdir(folder):
        click.echo(f'E: Folder not found {folder}')
        return -1
    if folder:
        generate_models(yaml_file_path, folder)
    elif click.confirm('Do you want to update current models?', default=True):
        generate_models(yaml_file_path, folder)
