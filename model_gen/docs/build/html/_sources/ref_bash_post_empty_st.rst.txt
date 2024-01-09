.. code-block:: bash

    Environment<DEVELOPMENT> waiting for response... timeout=30.0
    2023-02-01 05:27:26,548 CoMETt WARNING input.load             No input data for request!
    I: Skipping merge option

    HEADER CONTENT:
    {
        "Content-Type": "application/json"
    }


    BODY CONTENT:
        empty {}

    2023-02-01 05:27:26,733 CoMETt INFO   eval.validate         Header content-type check = OK

    RESPONSE BODY:
    {
        "trace_id": "c0fb16cb096fa378",
        "error": "missing portfolio_components JSON array in body JSON"
    }

    E:url: https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/stress_test
    Status: True
    HTTP response headers: {'Date': 'Wed, 01 Feb 2023 04:27:26 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'cache-control': 'no-store, no-cache', 'x-content-type-options': 'nosniff', 'strict-transport-security': 'max-age=15724800; includeSubDomains', 'x-download-options': 'noopen', 'x-xss-protection': '1; mode=block', 'x-frame-options': 'DENY', 'expires': '0', 'content-encoding': 'gzip', 'x-envoy-upstream-service-time': '4'}
    HTTP response body: {'trace_id': 'c0fb16cb096fa378', 'error': 'missing portfolio_components JSON array in body JSON'}
