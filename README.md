# Cloud Margin Estimator API Client

## Introduction
The motivation is to provide user-friendly interface to cpME api in form of python library. The main goal is auto generated code to avoid a boiler code and get access into all attributes of particular request and response data structure for easy manipulation and validation.

The code generator is some kind of tree resource object model (like DOM) from swagger definition file of open api standard. The tool can be used by developers and testers to avoid manual routines
and provide an api specification in available from CLI.

The library is part of [COMET](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-Tests) tool and helps regression testing with pytest framework for corresponding environment.


## Features
### cpme_api module
- Support of all cpme endpoints, get and post requests, exporting data to csv/json/xls
- Synchronous or asynchronous switch
- Data Models 
- Example of scripts
- Rich documentation of setup and usage
- Easy configuration of client setting with logging

### model_gen module
- Support of mocking data
- Generic code for all endpoints from swagger file according to open api 3.0
- Auto validation of expected response format according to the swagger specification
- Auto validation of expected type and items in response JSON structure according to the swagger specification
- Global configuration via (environment variables, toml file)
- Independent configuration for different environments DEV, PROD, SIMU .

## Installation
### Virtual environments
The main purpose of Python virtual environments is to create an isolated environment for a Python project to have its own dependencies, regardless of other projects. [Read more about Python Virtual Environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
Python 3 already has the venv module installed with the standard library.

Depending on your preferred Python installation. You can create virtual environment to use cpme_api client as follows:

```
python3 -m venv cpme-environment  # macOS/ Linux
python3 -m venv cpme-environment  # Windows
```

Activate this virtual environment:

```
source cpme-environment/bin/activate  # macOS/ Linux
cpme-environment/Scripts/activate     # Windows
```

To exit the environment:

```deactivate```

### Install
- To try out a stable version of Comet direct from the Github repository:

```git clone https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-PythonAPIClient --depth 1 -b master```

- Enter the downloaded folder

``cd <local_folder>/DAVe-MarginEstimator-PythonAPIClient``

- and run inside the virtual environment

```pip install .``` or ```python . install```

- set up **PYTHONPATH**

```export PYTHONPATH=<local_folder>/DAVe-MarginEstimator-PythonAPIClient```

- To check that api client is installed:

```python -m cpme_api``` or call just ``cpme_api``

# CPME API library

## Connection

As default the url is static address of [DBP](https://console.developer.deutsche-boerse.com/apis/afdc9fa5-767a-49ac-b834-ee92ea0ac040)

Default url is https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-2-0-0

You can change url with instance of **Configuration** class.

```
from cpme_api.api Configuration

config = Configuration()
config.url = 'https://eurexmargins.prod.dbgservice.com/api/v2.0'
```

For more details use [documentation](https://pages.github.deutsche-boerse.de/dev/DAVe-MarginEstimator-PythonAPIClient/model_gen/docs/build/html/index.html)

# Model Generator

Data class generator from swagger yaml file base on open api 3.0 standard generates models with data classe for cpme_api client.
It creates namespaces like (examples, primitive, request_body, responses) into cpme_api/models folder.


## Model Update with command line interface (CLI)
After the installation you can call generator:

```
$ model_gen update

                                                                      
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

# Examples

Example requests you can find in [examples](https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-PythonAPIClient/tree/master/example). 

## Request of /products snapshots:

Get request of products (resource) and save the response into csv file.

 1. Load the api dictionary definition with all endpoints  
```
from cpme_api.api import CpmeApi, fancy, Configuration, GET
from cpme_api.api.feature.utils import json_to_file
```
2. Define api_key and enable logging
```
config = Configuration()
config.api_key = 'U953e6r4-777e-4353-cfgf-ctrrtetres2'
config.enable_logging = True
```
3. Create client
```
api = CpmeApi(configuration=config)
```
a) explicitly with reference:
```
BD = '20220906'

API_KEY = 'U953e6r4-777e-4353-cfgf-ctrrtetres2'

PARAM_PROD  = {
    'business_date': '20220623,
    'live': 0,
    'extrafields': ['underlying_isin', 'product_type'],
    'x_dbp_apikey': API_KEY,
}

resp = api.products_get.get_default(**PARAM_PROD)
```

b) directly 
```
resp = api.products_get(business_date=20220623, live=0, extrafields=api.get_extrafields(GET.products))
```

4. save results
```
json_to_file(resp['products'], 'products')
```
5. close api
```
api.close()
```






