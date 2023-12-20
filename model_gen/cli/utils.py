import click
from os import environ
import sys
from typing import List
from model_gen import __version__ as version


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

ENV_HELP = "Kedro configuration environment name. Defaults to `local`."

ENTRY_POINT_GROUPS = {
    "global": "kedro.global_commands",
    "init": "kedro.init",
    "snaptool": "kedro.cli_snap",
    "prisma_stx": "kedro.cli_stx",
}

LOGO = rf"""

     _/_/_/            _/      _/  _/_/_/_/  _/_/_/_/_/  _/_/_/_/_/
  _/          _/_/    _/_/  _/_/  _/            _/          _/
 _/        _/    _/  _/  _/  _/  _/_/_/        _/          _/
_/        _/    _/  _/      _/  _/            _/          _/
 _/_/_/    _/_/    _/      _/  _/_/_/_/      _/          _/
                                                                Ⓒⓛⓞⓤⓓ Ⓜⓐⓡⓖⓘⓝ Ⓔⓢⓣⓘⓜⓐⓣⓞⓡ Ⓣⓔⓢⓣ Ⓣⓞⓞⓛ
  v{version}
"""


def split_string(ctx, param, value):
    """Split string by comma."""
    return [item.strip() for item in value.split(",") if item.strip()]


def show_logo():
    if '--help' in sys.argv or len(sys.argv) < 3:
        click.secho(LOGO, fg='green')


def env_option(func_=None, **kwargs):
    """Add `--env` CLI option to a function."""
    default_args = dict(type=str, default=None, help=ENV_HELP)
    kwargs = {**default_args, **kwargs}
    opt = click.option("--env", "-e", **kwargs)
    return opt(func_) if func_ else opt


def get_comet_sysenv() -> List[str]:
    return [f"{key}={environ[key]}" for key in (filter(lambda x: "COMET" in x, environ))]


def store_request_body(endpoint: str, component_type: str, ):
    file_name = body_request_file_name()
    file_path = os.path.join(file_dir, file_name)
    path = to_json('cli_', json_folder)


def get_component_type(kvars: dict):
    if pc := kvars.get('portfolio_components'):
        if len(pc) == 1:
            return pc[0]
        return ''
    return ''
