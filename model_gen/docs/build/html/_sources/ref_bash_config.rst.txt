.. code-block:: bash

    $ python -m comet config

         _/_/_/            _/      _/  _/_/_/_/  _/_/_/_/_/  _/_/_/_/_/
      _/          _/_/    _/_/  _/_/  _/            _/          _/
     _/        _/    _/  _/  _/  _/  _/_/_/        _/          _/
    _/        _/    _/  _/      _/  _/            _/          _/
     _/_/_/    _/_/    _/      _/  _/_/_/_/      _/          _/
                                                                    Ⓒⓛⓞⓤⓓ Ⓜⓐⓡⓖⓘⓝ Ⓔⓢⓣⓘⓜⓐⓣⓞⓡ Ⓣⓔⓢⓣ Ⓣⓞⓞⓛ
      v2.0.0

    Available environments: ['development', 'acceptance', 'simulation', 'production', 'k8sprod', 'snaptool']
    Available from system env:
    ENVIRONMENT_FOR_COMET=development

    Setting for current environment <development>:
    SWAGGER_YAML_DEFINITION_FILE = <absolute_path>/DAVe-MarginEstimator-Tests/comet/api/yaml/marginestimator2.yaml
    SNAPSHOTS_FOLDER = <absolute_path>/DAVe-MarginEstimator-Tests/example/data/snapshots
    REQUESTS_FOLDER = <absolute_path>/DAVe-MarginEstimator-Tests/example/data/requests
    RESPONSES_FOLDER = <absolute_path>/DAVe-MarginEstimator-Tests/example/data/responses
    SNAPTOOL_FOLDER = <absolute_path>/DAVe-MarginEstimator-Tests/example/data/snapexport
    URL_API = https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0
    REQUEST_TIMEOUT = 30
    cert_for_verify = False
    Configuration source: <absolute_path>/DAVe-MarginEstimator-Tests/settings.toml;<absolute_path>/DAVe-MarginEstimator-Tests/comet_conf.toml;<absolute_path>/DAVe-MarginEstimator-Tests/.secrets.toml

    Note: It is recommended to define env variable ENVIRONMENT_FOR_COMET for environment switch.
        to_dict ENVIRONMENT_FOR_COMET=development