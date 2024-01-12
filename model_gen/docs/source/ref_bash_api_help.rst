.. code-block:: bash

    python -m comet api --help
         _/_/_/            _/      _/  _/_/_/_/  _/_/_/_/_/  _/_/_/_/_/
      _/          _/_/    _/_/  _/_/  _/            _/          _/
     _/        _/    _/  _/  _/  _/  _/_/_/        _/          _/
    _/        _/    _/  _/      _/  _/            _/          _/
     _/_/_/    _/_/    _/      _/  _/_/_/_/      _/          _/
                                                                    Ⓒⓛⓞⓤⓓ Ⓜⓐⓡⓖⓘⓝ Ⓔⓢⓣⓘⓜⓐⓣⓞⓡ Ⓣⓔⓢⓣ Ⓣⓞⓞⓛ
      v2.0.0

    Usage: python -m comet.python -m comet api [OPTIONS] [ENDPOINT]...

      Commands of api section

      $ python -m comet api products

      $ python -m comet api products -p business_date=20220111 -p
      extrafields=instrument_type,currency -t 20

      $ python -m comet api series -p products=FME,D2TE -p business_date=20220111

      $ python -m comet api default_fund --body portfolio_components=etd_csv
      --prefix TC-001-df --to-json -V

      $ python -m comet api ?

      $ python -m comet api estimator -i -V

      $ python -m comet api estimator --prefix TC-001-es

    Options:
      -i, --info                 Show info of proper endpoint.
      -d, --dates INTEGER RANGE  List available snapshots dates [options: 0 =
                                 current, 1 = prev, <number_of_last_bd>]
                                 [0<=x<=20]
      --find TEXT                Find attribute information. Use with '?' to list
                                 available attributes.
      --to-json                  Export snapshots into .json file  [.csv is
                                 default]
      --print                    Print response content into stdout
      -V, --verbose              Show more detail
      --only-body                Use together with verbose and show only JSON body
                                 content.
      -S, --silent               Obsolete, limited usage! Stop all info messages,
                                 show only exported data, useful with pipe command
                                 stream
      -R, --required             Use by --with command to generate only minimum
                                 required fields according to the specification
      --to_dict                   Export body request input data into the json/csv
      --no-body-check            Disable default check of body json structure
                                 load. Useful for negative scenarios.
      --compare                  Comparison between JSON response vs stored with
                                 --prefix command.
      --path TEXT                Full path where to save json response. [default:
                                 /home/parimir/workspace/DAVe-CPME-API-
                                 Regression/development/snapshots for get results,
                                 /home/parimir/workspace/DAVe-CPME-API-
                                 Regression/development/responses for post
                                 results]
      -F, --file-name TEXT       File name to find with body request content.
      -O, --out TEXT             Output file name of response.
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