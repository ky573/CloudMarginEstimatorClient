# Cloud Margin Estimator Test Tool (CoMETT)

## Introduction
The motivation is to simplify testing of cpME api in form of python library and user friendly command line interface. The main goal is auto generated code to avoid a boiler code and get access into all attributes in request and response data structure for easy manipulation and validation. 
The code generator is some kind of tree resource object model (like DOM) from swagger definition file of open api standard. The tool can be used by developers and testers to avoid manual routines
and provide an api specification in available from CLI.
The library helps regression testing with pytest framework for corresponding environment.
The python test framework COMET for cpME api test (system, regression and business tests). It is based on CLI interface with python library. The main goal is to use CLI to interact with test scanario development with fast and flexible way. Intuitive commands and test approach with auto validation will simplify test process and improve quality of our cpME product.


## Features
- Support of all cpme endpoints, get and post requests, exporting data to csv/json/xls
- Support of snaptool api (only for development)
- Support of mocking data
- Generic code for all endpoints from swagger file according to open api 3.0
- Auto validation of expected response format according to the swagger specification
- Auto validation of expected type and items in response JSON structure according to the swagger specification
- CLI interface for quick API info, requests and snaptool (master data and market data) fetching from S3 drive
- Global configuration via (environment variables, docker .env or toml, yaml, json file)
- Independent configuration for different environments DEV, PROD, SIMU, ACT, SNAP or ANY which can be switchable during runtime

## Installation
### Virtual environments
The main purpose of Python virtual environments is to create an isolated environment for a Python project to have its own dependencies, regardless of other projects. [Read more about Python Virtual Environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
Python 3 already has the venv module installed with the standard library.

Depending on your preferred Python installation, you can create virtual environments to work with Comet as follows:

```
python3 -m venv comet-environment  # macOS/ Linux
python3 -m venv comet-environment  # Windows
```

Activate this virtual environment:

```
source env/comet-environment/bin/activate  # macOS/ Linux
.\comet-environment/Scripts/activate       # Windows
```

To exit the environment:

```deactivate```

### Install Comet

To try out a stable version of Comet direct from the Github repository:

```git clone https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests --depth 1 -b master```

Enter the downloaded folder

``cd /local_repository_folder/DAVe-MarginEstiamtor-Test``

and run inside the virtual environment

```pip install .```

set up PYTHONPATH

```to_dict PYTHONPATH=/local_repository_folder/DAVe-MarginEstimator-Tests```

To check that Comet is installed:

```python -m comet```

You should see the ASCII art graphic with help. If you do not want to see the graphic, set `false` in the config parameter in `comet_conf.toml`.

```cli_logo=false```


# Configuration
There is quite rich configuration setup where you can choose if the global settings parameters are initialize from environment variables, toml/yaml or json file. The missing global parameters will be loaded with default values. The settings can be changed during runtime according to the selected environment.

Follow more details ./docs/build/html/config.html.


# Command Line Interface (CLI)
After the installation you can call CLI by simple call with library module parameter `-m`

```
$ python -m comet

                                                                      
     _/_/_/            _/      _/  _/_/_/_/  _/_/_/_/_/  _/_/_/_/_/   
  _/          _/_/    _/_/  _/_/  _/            _/          _/        
 _/        _/    _/  _/  _/  _/  _/_/_/        _/          _/         
_/        _/    _/  _/      _/  _/            _/          _/          
 _/_/_/    _/_/    _/      _/  _/_/_/_/      _/          _/           
                                                                Ⓒⓛⓞⓤⓓ Ⓜⓐⓡⓖⓘⓝ Ⓔⓢⓣⓘⓜⓐⓣⓞⓡ Ⓣⓔⓢⓣ Ⓣⓞⓞⓛ
  v2.0.0

Usage: python -m comet.python -m comet [OPTIONS] COMMAND [ARGS]...

  This CLI provides data fetching from CPME resources with user defined
  options for quick data check of CPME API.

Options:
  --help  Show this message and exit.

Commands:
  api     Resources for cpME.
  config  Show configuration parameters.
  info    More information about CLI.
  snap    Snaptool client for cpME.
  tutorial  Open html documentation of COMET usage.
  update  Generate body request data classes.
  web     Open the cpme UI for specific environment.
```
## Tutorial

Open the tutorial web page with ```$ python -m comet tutorial```


## Command config

```
$ python -m comet config -e dev

Available environments: ['development', 'acceptance', 'simulation', 'production', 'prod-k8s', 'snaptool', 'prod-whatif']
Available from system env:

Setting for current environment <DEVELOPMENT>:
SWAGGER_YAML_DEFINITION_FILE = //abs_path/DAVe-MarginEstimator-Tests/comet/api/yaml/marginestimator2.yaml
SNAPSHOTS_FOLDER = //abs_path/DAVe-MarginEstimator-Tests/example/data/snapshots
REQUESTS_FOLDER = //abs_path/DAVe-MarginEstimator-Tests/example/data/requests
RESPONSES_FOLDER = //abs_path/DAVe-MarginEstimator-Tests/example/data/responses
SNAPTOOL_FOLDER = //abs_path/DAVe-MarginEstimator-Tests/example/data/snapexport
SCENARIO_PATH_FOLDER = //abs_path/DAVe-MarginEstimator-Tests
URL_API = https://cpme-lz567.risk.dev.fra.aws.dbgcloud.io/api/v2.0
REQUEST_TIMEOUT = 30
LOGGING = True
PRECISION_POINTS = 2
cert_for_verify = False
Configuration source: //abs_path/DAVe-MarginEstimator-Tests/comet_conf.toml;//abs_path/DAVe-MarginEstimator-Tests/.secrets.toml

Note: You can overwrite configuration source via COMET_CONFIG variable with optional configuration toml file.

Note: It is recommended to define env variable ENVIRONMENT_FOR_COMET for environment switch.Use: to_dict ENVIRONMENT_FOR_COMET=development

```

## Command api
```
$ python -m comet api --help

Usage: python -m comet.python -m comet api [OPTIONS] [ENDPOINT]...

  Commands for API:
  
  $ python -m comet api products

  $ python -m comet api products -p business_date=20220111 -p
  extrafields=instrument_type,currency -t 20

  $ python -m comet api series -p products=FME,D2TE -p business_date=20220111

  $ python -m comet api default_fund --body portfolio_components=etd_csv
  --prefix TC-001-df --to-json -V

  $ python -m comet api ?

  $ python -m comet api estimator -i -V

Options:
  -i, --info                 Show available entities of snapshot.
  -d, --dates INTEGER RANGE  List available snapshots dates [options: 0 =
                             current, 1 = prev, <number_of_last_bd>]
                             [0<=x<=20]
  --find TEXT                Find attribute information. Use with '?' to list
                             available attributes.
  --to-json                  Export snapshots into .json file  [.csv is
                             default]
  --print                    Print response content into stdout
  -V, --verbose              Show more detail
  -S, --silent               Stop all info messages, show only exported data,
                             useful with pipe command stream
  -R, --required             Use by --with command to generate only minimum
                             required fields according to the specification
  --to_dict                   Export body request input data into the json/csv
  --no-body-check            Disable default check of body json structure
                             load. Use for negative scenarios.
  --compare                  Comparison between JSON response vs stored with
                             --prefix command.
  -s, --store TEXT           Location to store json response. [default:
                             //abs_path/DAVe-MarginEstimator-
                             Tests/example/data/snapshots for get results,
                             //abs_path/DAVe-MarginEstimator-
                             Tests/example/data/responses for post results]
  -F, --file-name TEXT       File name to find with body request content.
  --prefix TEXT              The alias name for to_dict files.  [default: cli]
  -p, --params TEXT          Input parameters for query. For all `extrafields`
                             use '-p extrafields all'.
  -b, --body TEXT            Input parameters for response body. For DEFAULT[s
                             napshot,portfolio_components=etd_csv?csv_json]
  -M, --from-merge TEXT      Merge loaded body prefix file with prefix string
                             or file name string [example: --from-merge=TC-
                             Currency or -M x-y_currency.json]
  -t, --timeout FLOAT        Request timeout. To wait forever for a response,
                             use 0 value  [default: 30]
  -e, --env TEXT             Request of corresponding endpoint with parameter.
                             Default input is used from setting toml file.
                             Available keys:  ['dev', 'prod', 'simu', 'act',
                             'k8s', 'snap'].[default: development]
  --help                     Show this message and exit.

```

## Command snap

```
$ python -m comet snap --help


Usage: python -m comet.python -m comet snap [OPTIONS] [ENTITY_NAME]...

  Simple client to fetch data from S3 Prisma snapshots for cpME

  Hints:

  $ python -m comet snap -l -b 20220111

  $ python -m comet snap -l -b 20220111 -e prod -V

  $ python -m comet snap liquidity_factor margin_group -v SOD -b 20220111 -s
  /home/<folder>

Options:
  -l, --list_snap           Show available entities of snapshot.
  -b, --business_date TEXT  Filter snapshots according to date 'YYYYMMDD'
  -v, --version TEXT        Filter version from available list ['CONFIG',
                            'EOD', 'LIVE', 'OTC_EOD', 'OTC_SOD', 'RFF', 'SOD']
                            [default: EOD]
  -t, --timestamp TEXT      Filter for timestamp  [default: 0]
  -s, --save_to TEXT        Save content into csv file into user defined
                            location  [default: //abs_path/DAVe-
                            MarginEstimator-Tests/regression_test/snapexport]
  -V, --verbose             Show more info messages.
  -e, --env TEXT            Request of corresponding endpoint with parameter.
                            Default input is used from setting toml file.
                            Available keys:  ['dev', 'prod', 'simu', 'act',
                            'k8s', 'snap']  [default: development]
  -t, --timeout INTEGER     Request timeout. To wait forever for a response,
                            use 0 value  [default: 60]
  --help                    Show this message and exit.
```


# Library Usage

Library usage with examples you can find in [examples](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests/tree/master/example). 

## Example:

### Get request of products (resource) with auto validation and compare response with expected result

1. Load the api dictionary definition with all endpoints  
```
from comet.api import factory, GET, validate, fancy
from comet.api.feature.resource import Resource
from comet.api.feature import catch_exception
from comet.api.input import GetInput


apis, inputs = factory.loader()
```
2. Choose product/ resource name api
```
api = apis[GET.products]
```
3. you can define input parameters
```
params = inputs[GET.products]
```
a) explicitly:
```
BD = '20220906'

API_KEY = 'A953e6e4-235e-4217-a7b0-ceb071a9dba9'

PARAM_PROD  = {
    'business_date': '20220623,
    'live': 0,
    'extrafields': ['underlying_isin', 'product_type'],
    'x_dbp_apikey': API_KEY,
}

default_p = params.get_default(**PARAM_PROD)
```

It is possible to predefine general parameters for all endpoints as a precondition for all parameters instances 
```
params.set_param(live=0, business_date='20220623')
```

b) implicitly if the endpoint support extra-fields, you can assign all of them
```
default_p = params.params.get_default(extrafields=params.get_extra_fields())
```

4. get request options
```
resp = api.get.sync_request(params=PARAM_PROD, timeout=0.5)


resp = api.get.sync_request(params=default_p, verbose=True)


resp = api.get.sync_request(params=PARAM_PROD, verbose=True)

# or

resp = api.get.sync_request(**PARAM_PROD)
```

5. validation of response message according to the swagger definition (header, all fields, types, structure)
```
val = validate(resp, verbose=True)

val.to_xls()

# val.to_json(file_prefix="example")
# val.to_json(resp, file_dir="/abs_path/tmp")
# val.to_csv(file_prefix="example")

val.validate_items(randomize=True)
```

It is possible to store a response of some snapshot get request into the csv file for next time self auto comparison with
expected request. Useful in regression for example. 

```
val.compare_snapshot_or_save(refresh=False, file_prefix=prefix)
```

The exception raises if there is any error. You can wrap your code inside function and apply decorator @catch_exception(enable=True) for pretty exception handling.

The default location of output file is in the project folder `regression_test/data/dev_20220623_0_0_products.csv`.
You can change it via env var `COMET_SNAPSHOTS_FOLDER` or `toml` setting file.

# Regression test for cloud Margin Estimator (cPME)

Regression test for Margin Estimator [API](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-API)


- How to use comett library for flexible api testing with pytest you can find the example in [pytest_example.py](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests/blob/master/example/pytest_example.py)

- tests are written in python, run them by `pytest`, e.g.:
```
python3 -m pytest -s -v -rA ./pytest_example.py -k test_sample_api_get_endpoints
```

<span style="color:yellow">The new format of test content performed by GitHub Action will be updated soon.</span>



# Obsolete

### Liveness Test of PROD instance of cPME
[![cPME Liveness Test](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests/actions/workflows/ci.yaml/badge.svg?event=schedule)](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests/actions/workflows/ci.yaml)

> as of 2021-12-13

- Run against deployed instance of the application, they do not deploy anything themselves
- Performed by [this GitHub Action](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests/actions/workflows/ci.yaml)
- Scheduled by cron '30 8-15 * * 1-5' - [see here](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests/blob/master/.github/workflows/ci.yaml#L7)
- The GitHub Action Can be extended to other environments, type of command run, etc.  
  If interested please ask @dev/riskit-cloud-adoption team for assistance.


- For UI regression test there is AWS cloud watch wrapper with the puppeteer Node.js [UI](https://github.deutsche-boerse.de/RiskIT/aws-infrastructure/blob/master/environments/risk-production/cpme-monitoring/files/ui_recording.js).





