.. code-block:: bash

    $ python -m comet api stress_test --prefix TC-002-st -M currency-GBP.json --verbose --only-body --compare

    Environment<DEVELOPMENT> waiting for response... timeout=30.0
    2023-03-15 18:18:44,085 CoMETt INFO   input.load             Body content loaded from /home/parimir/workspace/DAVe-MarginEstimator-Tests/example/data/requests/TC-002-st_stress_test.json
    2023-03-15 18:18:44,085 CoMETt INFO   input._update_portfolio_components  Body content loaded from TC-002-st_etd_portfolio.json
    2023-03-15 18:18:44,085 CoMETt INFO   input._update_portfolio_components  Body content loaded from TC-002-st_cash_csv.csv
    2023-03-15 18:18:44,086 CoMETt INFO   merge.merge_from       Starting to merge from file /home/parimir/workspace/DAVe-MarginEstimator-Tests/example/data/requests/currency-GBP.json

    HEADER CONTENT:
    {
    "Content-Type": "application/json"
    }


    BODY CONTENT:
    {
    "portfolio_components": [
        {
            "etd_csv": {
                "csv": "Product ID,Contract Date,Version Number,Call Put Flag,Exercise Price,Net LS Balance\nFEXD,20311219,0,,,100\nOESX,20311219,0,C,5000,-100"
            },
            "type": "etd_csv"
        },
        {
            "type": "etd_portfolio",
            "etd_portfolio": [
                {
                    "line_no": "1",
                    "product_id": "OESX",
                    "contract_date": 20281215,
                    "maturity": 202812,
                    "call_put_flag": "P",
                    "exercise_price": 2400,
                    "version_number": "0",
                    "iid": 27471356,
                    "instrument_type": "Flex Option",
                    "exercise_style": "AMERICAN",
                    "net_ea": 1,
                    "net_ls_balance": -100
                }
            ]
        },
        {
            "type": "cash_csv",
            "cash_csv": {
                "csv": "Security ISIN,Settlement Date,Settlement Currency,Payable Cash Amount,Traded Price,Security Quantity,CCP Trade Number,Leg Type\nDE0005810055,20220630,,,100.23,100,,\n"
            }
        }
    ],
    "clearing_currency": "GBP"
    }

    2023-03-15 18:18:44,485 CoMETt INFO   eval.validate         Header content-type check = OK
    2023-03-15 18:18:44,537 CoMETt INFO   eval.validate         REQUEST in ENV:development URL: https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/stress_test
    2023-03-15 18:18:44,537 CoMETt INFO   eval.validate         RESPONSE HEADER: {'Date': 'Wed, 15 Mar 2023 17:18:44 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'cache-control': 'no-store, no-cache', 'x-content-type-options': 'nosniff', 'strict-transport-security': 'max-age=15724800; includeSubDomains', 'x-download-options': 'noopen', 'x-xss-protection': '1; mode=block', 'x-frame-options': 'DENY', 'expires': '0', 'content-encoding': 'gzip', 'x-envoy-upstream-service-time': '7'}
    2023-03-15 18:18:44,537 CoMETt INFO   eval.validate         /stress_test response keys body validation = OK
    2023-03-15 18:18:44,537 CoMETt INFO   eval.compare_log      Loading compare data from /home/parimir/workspace/DAVe-MarginEstimator-Tests/example/data/responses/TC-002-st_20220906_0_0_stress_test.json
    2023-03-15 18:18:44,839 CoMETt INFO   eval.compare_log      Deep comparison (JSON response vs expected) result = True
    POST URL https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0/stress_test
