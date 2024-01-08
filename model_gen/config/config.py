"""
export PEANUT_DB={name='foo', port=2000}
export PEANUT_DB__SCHEME=main

rules:
 - environment variables overide variables defined in post loaded config file
 - define project path into PYTHONPATH
 - define comet_conf path COMET_CONFIG=/home/parimir/workspace/DAVe-MarginEstimator-Tests/comet_conf.toml
"""
from dynaconf import LazySettings, Dynaconf
from dynaconf.validator import Validator
import os
from pathlib import Path
import sys
from typing import Union, Type
from os import environ


_ENVIRONMENTS = ['production']

_ENVIRONMENTS_MAP = {
    'prod': 'production'
}


class Environment:
    PROD = 'production'

    @staticmethod
    def alias(env_name: str):
        if env_name.lower() in _ENVIRONMENTS:
            return env_name.lower()
        else:
            return _ENVIRONMENTS_MAP.get(env_name.lower(), 'Unknown')

    @staticmethod
    def environments():
        return list(_ENVIRONMENTS_MAP.keys())


_ROOT_DIR = Path(__file__).parent.parent.parent

PROJECT_ROOT = str(_ROOT_DIR)


_swagger_file_name = 'marginestimator2.yaml'


def _swagger_yaml_definition_file():
    path = os.path.join(_ROOT_DIR, 'model_gen', 'yaml', _swagger_file_name)
    if 'COMET_SWAGGER_YAML_DEFINITION_FILE' in environ:  # priority assign from system variable
        return environ['COMET_SWAGGER_YAML_DEFINITION_FILE']
    elif os.path.isfile(path):
        return path
    else:
        print(f'ERROR: swagger yaml file not found {path}')


def init_config_file():
    confs = list()
    if os.getenv('COMET_CONFIG'):
        confs.append(os.getenv('COMET_CONFIG'))
    else:
        confs.append(os.path.join(_ROOT_DIR, 'comet_conf.toml'))

    confs.append(os.path.join(_ROOT_DIR, '.secrets.toml'))
    return confs


class Settings(Dynaconf):
    """Define all settings available for users to configure in COMET,
    along with their validation rules and default values.
    Use Dynaconf's LazySettings as base.
    """

    _CONF_SOURCE = Validator("CONF_SOURCE", default="conf")
    _SWAGGER_YAML_FILE = Validator("SWAGGER_YAML_FILE",
                                   default=_swagger_yaml_definition_file(),
                                   must_exist=True)
    _SCENARIO_PATH_FOLDER = Validator('SCENARIO_PATH_FOLDER',
                                      must_exist=True,
                                      default=PROJECT_ROOT)
    _CONFIG = Validator("CONFIG", must_exist=True)
    _SNAPSHOTS_FOLDER = Validator('SNAPSHOTS_FOLDER',
                                  default=os.path.join(_ROOT_DIR,
                                                       'example',
                                                       'data',
                                                       'snapshots'),
                                  must_exist=True)
    _REQUESTS_FOLDER = Validator('REQUESTS_FOLDER',
                                 default=os.path.join(_ROOT_DIR,
                                                      'example',
                                                      'data',
                                                      'requests'),
                                 must_exist=True)
    _RESPONSES_FOLDER = Validator('RESPONSES_FOLDER',
                                  default=os.path.join(_ROOT_DIR,
                                                       'example',
                                                       'data',
                                                       'responses'),
                                  must_exist=True)
    _SNAPTOOL_FOLDER = Validator('SNAPTOOL_FOLDER',
                                 default=os.path.join(_ROOT_DIR,
                                                      'example',
                                                      'data',
                                                      'snapexport'),
                                 must_exist=True)
    _PRECISION_POINTS = Validator('PRECISION_POINTS', must_exist=True, default=2)
    _URL = Validator('URL', must_exist=True)
    _REQUEST_TIMEOUT = Validator('REQUEST_TIMEOUT', default=20, must_exist=True)
    _GEN_EP = Validator('GENERATE_ENDPOINTS', must_exist=True, default=False)
    _LOGGING = Validator('LOGGING', must_exist=True, default=True)
    _CLI_LOGO = Validator('CLI_LOGO', default=True)

    def __init__(self, *args, **kwargs):
        kwargs.update(
            validators=[
                self._CONF_SOURCE,
                self._SWAGGER_YAML_FILE,
                self._SNAPSHOTS_FOLDER,
                self._RESPONSES_FOLDER,
                self._REQUESTS_FOLDER,
                self._SNAPTOOL_FOLDER,
                self._SCENARIO_PATH_FOLDER,
                self._URL,
                self._PRECISION_POINTS,
                self._REQUEST_TIMEOUT,
                self._CLI_LOGO,
                self._LOGGING
            ],
            environments=_ENVIRONMENTS,
            core_loaders=['YAML', 'TOML', 'JSON'],
            default_env="default",
            envvar_prefix="COMET",
            env_switcher="ENVIRONMENT_FOR_COMET",
            settings_files=init_config_file()
        )
        try:
            super().__init__(*args, **kwargs)
            self._environment = None
            self.validators.validate_all()
        except Exception as e:
            print(f"E: parse configuration: {str(e)} Check if you defined all"
                  f" required settings correctly in {init_config_file()}")
            sys.exit(1)

    def __call__(self, env: str) -> Type[LazySettings]:
        if env in self.environments_for_dynaconf:
            # for 'DEV', 'PROD' ..
            return self._switch_settings(env)
        elif Environment.alias(env) != 'Unknown':
            # for 'development', 'production'...
            return self._switch_settings(Environment.alias(env))
        else:
            print(f'<{env}> not known, current env {self.current_env} loaded')
            return self

    def _switch_settings(self, env: str):
        if env.upper() == self.current_env:
            return self
        # print(f'I: Switching global settings for {env.upper()}')
        return BetterLazy(self.from_env(env, keep=True))

    @property
    def env(self) -> str:
        # TODO del
        return self.current_env

    def cert_for_verify(self) -> Union[str, bool]:
        if hasattr(self, 'CERT_PATH') and hasattr(self, 'CERT_NAME'):
            if cert_path := os.path.join(self.CERT_PATH, self.CERT_NAME):
                return cert_path
            else:
                return False
        else:
            return False

    def env_equal(self, envs: list = []):
        al_env = [Environment.alias(e) for e in envs]
        if envs is [] or (self.current_env in al_env):
            return True
        else:
            return False


class BetterLazy(LazySettings):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def cert_for_verify(self) -> Union[str, bool]:
        if hasattr(self, 'CERT_PATH') and hasattr(self, 'CERT_NAME'):
            if cert_path := os.path.join(self.CERT_PATH, self.CERT_NAME):
                return cert_path
            else:
                return False
        else:
            return False
