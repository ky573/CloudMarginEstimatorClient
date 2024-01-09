Library usage
=============

Namespaces
----------
There are three main namespaces of functions.

* comet.api     - resource loader
* comet.models  - data classes of request body and response of particular resources
* comet.evals   - evaluation functions

The usual comet flow
--------------------
    1. selection of proper resource
    2. input definition
        - query/path parameters of GET requests
        - JSON request body structure of POST requests
    3. sending a request
    4. validation or comparison of JSON result

Select resource
+++++++++++++++
The core function is the loader() which creates all resource objects of cpME according to the yaml file and returns two dictionary based objects contains inputs and apis, where the key is the resource name.
The available resource names are predefined by GET and POST enum and you can select the corresponding resource objects by returned from
loader.

Available resource names:

.. code-block:: python

    GET.products                    POST.estimator
    GET.series                      POST.otc_trade_details
    GET.securities                  POST.otc_sensitivities
    GET.clearing_currencies         POST.greeks
    GET.snapshots                   POST.stressmatrix
    GET.live_snapshots              POST.default_fund
    GET.indicative_margin           POST.stress_test
    GET.config
    GET.global_scenarios

Example to access the instance of products api:

.. code-block:: python

    from comet.api import loader, GET, validate, fancy
    apis, inputs = loader()
    products_api = apis[GET.products]
    products_params = inputs[GET.products]


.. note::
    The default yaml source file is fetched by setting as a default. You can define **yaml_path** string as an optional parameter of **loader** function.


Input definition
++++++++++++++++
You can easily predefine input query parameters as a simple dict and pass them into get_default function which check valid parameters according to the spec.

.. code-block:: python

    API_KEY = 'b953e6e4-235e-4217-a7b0-ceb071a4541'
    PARAM_PROD = {'business_date': '20220906',
                  'live': 'false',
                  'extrafields': ['underlying_isin', 'product_type'],
                  'x_dbp_apikey': API_KEY
                  }
    default_p = products_params.get_default(**PARAM_PROD)

You can pass optional query parameters with values as an function parameters.

.. code-block:: python

    default_p = products_params.get_default(business_date='20221108', live='false', extrafields=params.get_extra_fields())

    out:
        {
            "business_date": "20220906",
            "live": "false",
            "extrafields": [
                "underlying_isin",
                "product_type"
            ],
            "x_dbp_apikey": "b953e6e4-235e-4217-a7b0-ceb071a9dba1"
        }

In case that resource supports **extrafields** you can get all of them like.

.. code-block:: python

    default_p = products_params.get_default(extrafields=params.get_extra_fields())

    out:
        {
        "extrafields": [
            "product",
            "instrument_type",
            "clearing_house",
            "prod_name",
            "prod_isin",
            "underlying_isin",
            "currency",
            "product_type",
            "extended_product_type",
            "margin_style_flag",
            "exercise_style_flag",
            "product_settlement_type",
            "final_settlement_time",
            "product_tick_size",
            "product_tick_value",
            "liquidation_group",
            "xm_eligibility"
        ]
    }

The **required** input parameters you can return with none function parameters.

.. code-block:: python

    default_p = products_params.get_default()

    out:
        {}

.. note::
    You can add header parameter like x_dbp_apikey='xxx-yyy-zzz'

Auto validation of input parameters and their value types.

.. code-block:: python

    default_p = products_params.get_default(live=False)

    out:
        ***ValueError: wrong value of live=1 must be 'true' or 'false'


.. note::
    You can disable auto validation for all resources of input parameters with function set_type_falidation.

        from comet.api.models import set_type_validation

Global setting
++++++++++++++
You can define parameters for all GET resources.

.. code-block:: python

    set_type_validation(False)
    from comet.api import GetInput

    GetInput.set_param(business_date='20220906')


Sending Request
+++++++++++++++
The loader assigned to api corresponding type of request (post, get) according to the specification. Sending request with default parameters.

.. code-block::

    resp = api.get.sync_request(default_p)

.. note::
    The sync_request supports **verbose** and **env** optional parameters.

.. code-block::

    resp = api.get.sync_request(default_p, verbose=True)

    out:
        2023-03-09 14:20:56,545 CoMETt INFO   resource.sync_request     GET: HEADER:{'Content-Type': 'application/json', 'x_dbp_apikey': 'kolo-kolo'} PARAMS:{'business_date': '20220906', 'live': 'false', 'extrafields': ['underlying_isin', 'product_type']} URL:https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/products


Validation
++++++++++
There is **validate()** function which evaluate JSON response structure and type values according to the yaml specification.
If there is some inconsistency then the exception **ApiException** is risen otherwise it returns dictionary object with JSON content.


.. code-block::

    val = validate(resp)

    out:
        2023-03-09 15:33:43,183 CoMETt INFO   eval.validate         Header content-type check = OK
        2023-03-09 15:33:43,199 CoMETt INFO   eval.validate         Root fields validation in json response = OK
        2023-03-09 15:33:43,199 CoMETt INFO   eval.validate         /products response keys body validation = OK


.. code-block::

    val = validate(resp, verbose=True)

    out:
        2023-03-09 15:34:35,279 CoMETt INFO   eval.validate         Header content-type check = OK
        2023-03-09 15:34:35,297 CoMETt INFO   eval.validate         Root fields validation in json response = OK
        2023-03-09 15:34:35,297 CoMETt INFO   eval.validate         REQUEST in ENV:development URL: https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/products?business_date=20220906&live=false&extrafields=underlying_isin&extrafields=product_type
        2023-03-09 15:34:35,297 CoMETt INFO   eval.validate         RESPONSE HEADER: {'Date': 'Thu, 09 Mar 2023 14:33:34 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'cache-control': 'no-store, no-cache', 'x-content-type-options': 'nosniff', 'strict-transport-security': 'max-age=15724800; includeSubDomains', 'x-download-options': 'noopen', 'x-xss-protection': '1; mode=block', 'x-frame-options': 'DENY', 'expires': '0', 'content-encoding': 'gzip', 'x-envoy-upstream-service-time': '2'}
        2023-03-09 15:34:35,297 CoMETt INFO   eval.validate         /products response keys body validation = OK


