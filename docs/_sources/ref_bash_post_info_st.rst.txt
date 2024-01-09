.. code-block:: bash

    ENV:development  URL: https://cpme.risk.dev.fra.aws.dbgcloud.io/api/v2.0

    <stress_test>: POST
      Description:
        Stress test calculation on system scenario level

      Parameters:
        HEADER: 'x_dbp_apikey'
          *Required: True

      Request Body:
        'clearing_currency','is_cross_margined','portfolio_components'
        *Required: portfolio_components

         *Portfolio Components: type, etd_portfolio, etd_csv, etd_cp005, repo_json, cash_json, cash_csv

      Response Keys:
        'business_date','live','live_timestamp','errors','cash_stress_test_liqu_value','position_stress_test','cash_stress_test_liqu_summary'
