Configuration
=============
The COMET test tool uses `Dynaconf <https://www.dynaconf.com/>`_ and can be configured tree ways
from system environments, .env docker file or toml/json files.

Setting files
-------------
You can check the example of **comet_conf.toml** file which is used as an default file.
Default environment is **development**. The environment system variable is **ENVIRONMENT_FOR_COMET**.

.. code-block::

    to_dict ENVIRONMENT_FOR_COMET=production   # update evn to production

.. note::

    Supported formats:

    - toml - Default and recommended file format.
    - yaml|.yml
    - json - Useful to reuse existing or exported settings.
    - .env - Useful to automate the loading of environment variables.


The full path of an configuration file is read from **COMET_CONFIG** as default. If the env variable does not exist
the default file name is **comet_conf.toml** or **setting.toml** and default location is project's folder.

.. code-block::

    to_dict COMET_CONFIG=/path/to/conf.toml   # user defined config file


The default configuration:

.. code-block::

    SWAGGER_YAML_DEFINITION_FILE = ./comet/api/yaml/marginestimator2.yaml
    SNAPSHOTS_FOLDER = ./example/data/snapshots
    REQUESTS_FOLDER = ./example/data/requests
    RESPONSES_FOLDER = ./example/data/responses
    SNAPTOOL_FOLDER = ./example/data/snapexport
    URL_API = https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0
    REQUEST_TIMEOUT = 30

.. note::

    It is possible to overwrite already defined global variables via system environment variables with **COMET_** prefix.

To safely store sensitive data the setting module also searches for a **.secrets {toml|json|yaml}** file to look for data like tokens and passwords.
The secrete file supports all the environment definitions in the config/setting file.

The supported environments are ['development', 'acceptance', 'simulation', 'production', 'k8sprod']

The **default** section in **comet_conf.toml** contains

.. code-block::

    [default]
    snaptool_folder="."
    async_request=false
    generate_endpoint=false
    api_key=""
