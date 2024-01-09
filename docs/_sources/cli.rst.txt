Command Line Interface usage
============================

Main CLI parameters
-------------------
There are seven subcommands.

::

    python -m comet

*  **api** - cpME api interface (requests, validation, to_dict, search).
*  **config** - Show configuration parameters.
*  **info** - More information about CLI.
*  **snap** - Snaptool (AWS S3) client for cpME.
*  **tutorial** - Open documentation page via default web browser
*  **update** - Generate request/response data classes.
*  **web** - Open the cpme UI for specific environment via default web browser.

.. note::
    With --help command you can see more info.

Let's start with simple CLI feature. In the beginning you need to setup the global configuration.


config
++++++

.. code-block:: bash

    python -m comet config


As an precondition the global setting needs to be setup and check.

1. check if the variables are correctly defined in **comet_conf.toml** if you do not want to use default setting.

.. note::
    The main configuration file comet_conf.toml is located inside project folder. If you want to change file location
    you need to to_dict COMET_CONFIG=/absolute_path_to/new_comet_conf.toml.


2. Define environment switch with system variable ENVIRONMENT_FOR_COMET. In our example we use development.

.. important::
    Available environemnts: development, acceptance, simulation, production, k8sprod, snaptool

::

    to_dict ENVIRONMENT_FOR_COMET=development

If you want to test different open-api schema you need to create COMET_SWAGGER_YAML_DEFINITION_FILE.

::

    to_dict COMET_SWAGGER_YAML_DEFINITION_FILE = /absolute_path_to/marginestimator.yaml

Stdout of config command:

.. include:: ref_bash_config.rst


api
++++
List the subcommands.

.. code-block:: bash

    $ python -m comet api --help

.. include:: ref_bash_api_help.rst

List all available endpoints

.. code-block:: bash

    $ python -m comet api ?

output:

.. code-block:: bash

    E: Unknown endpoint ?. You can choose: GET:['products', 'series', 'securities', 'clearing_currencies', 'snapshots', 'live_snapshots', 'indicative_margin', 'config', 'global_scenarios'] POST:['estimator', 'otc_trade_details', 'otc_sensitivities', 'greeks', 'stressmatrix', 'convert_etd_cp005', 'convert_otc_shorthand', 'convert_cash_csv', 'default_fund', 'stress_test']


GET request
-----------
Let's try /series endpoint.

.. note::
    If you are not familiar with query or path parameters of get request you can get complete description with
    ***python -m comet api series --info*** .

Request series and save the snapshot into the csv file.

.. code-block:: bash

    python -m comet api series

output:

.. code-block:: bash

    Environment<DEVELOPMENT> waiting for response... timeout=30.0
    2023-01-31 19:52:09,674 CoMETt WARNING input.get_param        api-key head parameter should be defined!
    2023-01-31 19:52:23,078 CoMETt INFO   eval.validate         Header content-type check = OK
    2023-01-31 19:52:27,735 CoMETt INFO   eval.validate         Root fields validation in json response = OK
    2023-01-31 19:52:27,735 CoMETt INFO   eval.validate         /series response keys body validation = OK
    GET https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/series
    Response stored into /default_folder/DAVe-MarginEstimator-Tests/example/data/snapshots/cli_20220906_0_0_series.csv. size=26.488MB duration=00h:00m:20s

The response message is validated and stored with default prefix = 'cli'.

.. note::
    You can change prefix name with parameter --prefix=the_name


Use query parameters of /series
+++++++++++++++++++++++++++++++

You can use hints to see list of available parameters.

.. code-block:: bash

    $ python -m comet api series -p ?

output:

.. code-block:: bash

    You can use ['extrafields', 'business_date', 'live', 'live_timestamp', 'products'] or for header ['x_dbp_apikey']

Let's query business_date, products like (OGBL & FDAX) and all extrafields (columns).

.. code-block:: bash

    python -m comet api series -p business_date=20220906 -p products=OGBL,FDAX -p extrafields=all

output:

.. code-block:: bash

    Environment<DEVELOPMENT> waiting for response... timeout=30.0
    2023-01-31 20:12:00,365 CoMETt INFO   input.get_default      Note: Query of historical snapshots might take a long time.	business_date=20220906
    2023-01-31 20:12:00,365 CoMETt WARNING input.get_param        api-key head parameter should be defined!
    Waiting for request for bd=20220906. Historical requests can take a time.
    2023-01-31 20:12:00,675 CoMETt INFO   eval.validate         Header content-type check = OK
    2023-01-31 20:12:00,698 CoMETt INFO   eval.validate         Root fields validation in json response = OK
    2023-01-31 20:12:00,698 CoMETt INFO   eval.validate         /series response keys body validation = OK
    GET https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/series?business_date=20220906&products=OGBL&products=FDAX&extrafields=product_id&extrafields=contract_date&extrafields=contract_maturity&extrafields=expiry_maturity&extrafields=call_put_flag&extrafields=exercise_price&extrafields=version_number&extrafields=iid&extrafields=act_trade_unit_no&extrafields=days_to_expiration&extrafields=trade_unit_value&extrafields=exercise_style_flag&extrafields=contract_frequency
    Response stored into /default_folder/DAVe-MarginEstimator-Tests/example/data/snapshots/cli_20220906_0_0_series.csv. size=0.042MB duration=00h:00m:00s


.. note::
    You can to_dict JSON snapshots into .json file with additional command **--to-json**.

    You can save response csv file with user defined file name with additional command **--out=user_file_name**

    You can print out response JSON content into the terminal with additional command **--print**.

.. important::
    Default to_dict folder is defined in global variable **SNAPSHOTS_FOLDER**.

    You can change folder with command **--store /tmp**


Use path parameters of /config
+++++++++++++++++++++++++++++++

You can use hints to see output parameters.

.. code-block:: bash

    $ python -m comet api config -i

output:

.. code-block:: bash

     <config>: GET
     Description: None

      Parameters:
        HEADER: {'x_dbp_apikey': 'X-DBP-APIKEY'}
        PATH PARAMETERS: 'param'
        *Required: 'x_dbp_apikey','param'

      Response:
        [200] example:
            {'max_body_size': 262144000}

There is only one parameter **max_body_size**.

.. code-block:: bash

    $ python -m comet api config max_body_size


POST request
------------
The flow of post requests is composed from input body definition, out put file definition and optional comparison.
The CLI supports creation of body request content with portfolio components and merging of JSON, CSV, XML files with initial
JSON body structure. There is a file prefix feature which helps to build any body request with different files with strict
rules according to the specific portfolio defined in open api yaml file.


empty request of /stress_test
+++++++++++++++++++++++++++++

.. code-block:: bash

    python -m comet api stress_test --verbose

output:

.. include:: ref_bash_post_empty_st.rst

The body request is empty and backend sent error message.

.. important::
    There is always first validation of header content.

Description of endpoint definition
++++++++++++++++++++++++++++++++++

.. code-block:: bash

    python -m comet api stress_test --info

output:

.. include:: ref_bash_post_info_st.rst

.. note::

    With parameter **--verbose/-V** you can see example of JSON response structure.


Build the new JSON body
+++++++++++++++++++++++
if you do not have any JSON content of body request CLI can to_dict it. Let's assume
we want to to_dict body content with clearing_currency and one portfolio_components like etd_csv.

.. code-block:: bash

    python -m comet api stress_test --body 'clearing_currency','portfolio_components'=etd_csv

.. note::

    You can use **--body ?** to see available attributes of proper endpoint.

    You can add combination of portfolio components like  --body 'portfolio_components'=etd_csv?etd_portfolio

.. code-block:: bash

    {
        "clearing_currency": "EUR",
        "portfolio_components": [
            {
                "type": "etd_csv",
                "etd_csv": {
                    "csv": "Product ID,Contract Date,Version Number,Call Put Flag,Exercise Price,Net LS Balance\\nFEXD,20311219,0,,,100\\nOESX,20311219,0,C,5000,-100"
                }
            }
        ]
    }

To to_dict JSON response into the file you have to use **--to-json** with **--prefix=tc_alias**

.. code-block:: bash

    $ python -m comet api stress_test --body 'clearing_currency','portfolio_components'=etd_csv --prefix TC-001-st --to-json
    >> Body request stored into /default_folder/DAVe-MarginEstimator-Tests/example/data/requests/TC-001-st__stress_test.json. size=0.316kB


.. warning::

    Default prefix is **cli**

.. important::

    The generated content is an example from definition. In case of csv example the COMET split the lines only
    with **/n** anything else will be ignored. In previous example is generated **//n**!

Send a request
++++++++++++++
The body content is loaded according to the prefix name from external file located in the REQUESTS_FOLDER.
The response content is automatically stored into the file name composed from **<prefix>_<business_date>_<live_flag>_<live_timestamp>_<endpoint>.json**

.. code-block:: bash

    python -m comet api stress_test --prefix TC-001-st

    Environment<DEVELOPMENT> waiting for response... timeout=30.0
    2023-02-01 06:29:40,684 CoMETt INFO   input.load             Body content loaded from /default_folder/DAVe-MarginEstimator-Tests/example/data/requests/TC-001-st_stress_test.json
    2023-02-01 06:29:41,160 CoMETt INFO   eval.validate         Header content-type check = OK
    2023-02-01 06:29:41,200 CoMETt INFO   eval.validate         /stress_test response keys body validation = OK
    2023-02-01 06:29:41,203 CoMETt INFO   eval.to_json          Response saved in /default_folder/DAVe-MarginEstimator-Tests/example/data/responses/TC-001-st_20220906_0_0_stress_test.json
    POST URL https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/stress_test


.. note::
    You can use **--verbose** to show body request and response JSON structure into the terminal.

    Together with verbose you can use **--only-body** to see only body request.

    You can force to change default output file name with **--out new_file_name**


Body loader logic
+++++++++++++++++
The logic of body content load base on the prefix name is feature that keeps various set of testcases under the one
folder defined via REQUESTS_FOLDER. The specific scenario can be identified as a composition of files with unique prefix name.
There can be loaded two kind of files with specific prefix. The first one is an initial file and second one is a portfolio component file.
The initial file is searched according to the file name equal to **<prefix_name>_<endpoint>.json**.
The portfolio component file is searched according to the file name equal to **<prefix_name>_<portfolio_component_name>_<endpoint>.json**.
There is auto evaluation logic which check if the portfolio_component is part of specific endpoint and if yes then the file
structure is aggregated with the initial file.
The final JSON request body validation can be disabled before request flow.
The COMET can process portfolio component files with csv, xml or json content.

.. note::
    To disable validation of JSON request body you can use command with parameter **--no-body-check**.
    It can be useful for negative scenario case to check vulnerability of back end.

.. note::
    The portfolio_component_name depends on endpoint type and for /stress_test it can be like etd_portfolio, etd_csv, etd_cp005, repo_json, cash_json, cash_csv

In the example below the REQUESTS_FOLDER contains three files with one prefix name (**TC-002-st**) as an one scenario.

.. code-block:: bash

    TC-002-st_stress_test.json  -> contains root JSON structure like currency, snapshot
    TC-002-st_etd_portfolio.json    -> contains JSON structure of etd_portfolio component only
    TC-002-st_cash_csv.csv  --> contains csv data only of cash_csv portfolio component


Example of INFO messages during the body load flow.

.. code-block:: bash

    2023-02-01 08:54:51,666 CoMETt INFO   input.load     Body content loaded from /default_folder/DAVe-MarginEstimator-Tests/example/data/requests/TC-002-st_stress_test.json
    2023-02-01 08:54:51,666 CoMETt INFO   input._update_portfolio_components  Body content loaded from TC-002-st_etd_portfolio.json
    2023-02-01 08:54:51,666 CoMETt INFO   input._update_portfolio_components  Body content loaded from TC-002-st_cash_csv.csv


Merge feature
+++++++++++++
There is possibility to merge specific JSON file with correct structure with **--from-merge/-M** parameter.
The parameter value can be different prefix of a file or full file name located in REQUESTS_FOLDER.

.. code-block:: bash

    2023-02-01 09:28:00,505 CoMETt INFO   merge.merge_from       Starting to merge from file /default_folder/DAVe-MarginEstimator-Tests/example/data/requests/currency-GBP.json

Request flow
++++++++++++
When request body content is found it is sent to specific URL based on environment type.
The response is stored into the default folder defined in RESPONSES_FOLDER.


Comparison of response
++++++++++++++++++++++
The previously saved response file can be compared in second execution with response message.
Use parameter **--compare**.

.. code-block:: bash

    2023-02-01 09:33:46,643 CoMETt INFO   eval.compare_log      Loading compare data from /defaut_folder/DAVe-MarginEstimator-Tests/example/data/responses/TC-002-st_20220906_0_0_stress_test.json
    2023-02-01 09:33:46,925 CoMETt INFO   eval.compare_log      Deep comparison (JSON response vs expected) result = True

The comparison is very useful and it provide complex evaluation between two nested JSON structures.
Here is an example where 4 kinds of differences has been identified. The error message shows location of the difference.

.. code-block:: bash

    Exception: Resource: /stress_test, Error Numbers: 4
    Error_msg:
         1. ValueError "position_stress_test[2.item]/stress_value[7.item]/stress_pnl_product_currency/amount" response value 85386.845 != compared value 85386.84566
         2. ValueError "position_stress_test[2.item]/stress_value[368.item]/system_scn_text" response value 20220311 != compared value 202203111
         3. ValueError "cash_stress_test_liqu_summary[0.item]/currency" response value EUR != compared value EURE
         4. ValueError: Response attribute cash_stress_test_liqu_summary[0.item]/scenario[4.item]: {'scenario_id': 'HS04_CMM', 'liqu_value_sum': -7518.71062349722, 'liqu_value_eur': -7518.71062349722, 'diff2current': -806.6308453086895} not found in in compared data. Search keys = ['scenario_id']

**Scenario example to compare response of stress_test post request with already saved structured**

.. include:: ref_bash_example01.rst

API_KEY setting
---------------
The api_key is initialised from hidden configuration file **.secrets.toml** and it can
be defined individually for every environment. No api key is defined as default.

.. code-block:: bash

    ['development']
    api_key = "super-secret-key"

Validation flow logic
---------------------
There are three kind of auto validation after the request flow.

1. Header content check
2. Response structure check with expected attributes
3. Comparison check





