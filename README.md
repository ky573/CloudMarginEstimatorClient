# Cloud Margin Estimator API Client

## Introduction
The motivation is to simplify testing of cpME api in form of python library and user friendly command line interface. The main goal is auto generated code to avoid a boiler code and get access into all attributes in request and response data structure for easy manipulation and validation. 
The code generator is some kind of tree resource object model (like DOM) from swagger definition file of open api standard. The tool can be used by developers and testers to avoid manual routines
and provide an api specification in available from CLI.
The library helps regression testing with pytest framework for corresponding environment.
The python test framework COMET for cpME api test (system, regression and business tests). It is based on CLI interface with python library. The main goal is to use CLI to interact with test scanario development with fast and flexible way. Intuitive commands and test approach with auto validation will simplify test process and improve quality of our cpME product.


## Features
- Support of all cpme endpoints, get and post requests, exporting data to csv/json/xls
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

To check that api client is installed:

```python -m cpmeapi```

# CPME API library

## Connection

As default the url is static address of [DBP](https://console.developer.deutsche-boerse.com/apis/afdc9fa5-767a-49ac-b834-ee92ea0ac040)

Default url is https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-2-0-0

You can change url with instance of Config class.

```
from cpme_api.api Configuration

config = Configuration()
config.url = 'https://eurexmargins.prod.dbgservice.com/api/v2.0'
```

# Model Generator

Data class generator from swagger yaml file base on open api 3.0 standard generates models with data classe for cpme_api client.
It creates namespaces like (examples, primitive, request_body, responses) into cpme_api/models folder.


## Model Update with command line interface (CLI)
After the installation you can call CLI by simple call with library module parameter `-m`

```
$ python -m model_gen update

                                                                      
     _/_/_/            _/      _/  _/_/_/_/  _/_/_/_/_/  _/_/_/_/_/   
  _/          _/_/    _/_/  _/_/  _/            _/          _/        
 _/        _/    _/  _/  _/  _/  _/_/_/        _/          _/         
_/        _/    _/  _/      _/  _/            _/          _/          
 _/_/_/    _/_/    _/      _/  _/_/_/_/      _/          _/           
                                                                Ⓒⓛⓞⓤⓓ Ⓜⓐⓡⓖⓘⓝ Ⓔⓢⓣⓘⓜⓐⓣⓞⓡ Ⓣⓔⓢⓣ Ⓣⓞⓞⓛ
  v2.0.0


Usage: model_gen update [OPTIONS]

  Regenerate data model classes according to the recent swagger yaml file
  definition with default values into cpme_api/api/models. The data objects
  are mutable dictionary based structures of body request for POST api
  endpoints. It helps to build JSON body request object during the runtime :-)
  usage:     import cpme_api.api.models     from cpme_api.api.models import
  Estimator

Options:
  -y, --yaml_file TEXT  External source file name path.
  -f, --folder TEXT     Generate modules into another folder. [TEXT /path]
  --help                Show this message and exit.
```

# Library Usage

Library usage with examples you can find in [examples](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests/tree/master/example). 

## Example:

### Get request of products (resource) with auto validation and compare response with expected result

1. Load the api dictionary definition with all endpoints  
```
from cpme_api.api import CpmeApi, fancy, Configuration, GET
from cpme_api.api.feature.utils import json_to_file


apis, inputs = factory.loader()
```
2. Define api_key and enable logging
```
config = Configuration()
config.api_key = API_KEY
config.enable_logging = True

```
3. Create client
```
api = CpmeApi(configuration=config)

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
resp = api.products_get('business_date': '20220623, 'live': 0, timeout=5)
```

b) implicitly if the endpoint support extra-fields, you can assign all of them
```
resp = api.products_get(extrafields=api.get_extrafields(GET.products))
```

4. save results
```
json_to_file(resp, 'products')
```





