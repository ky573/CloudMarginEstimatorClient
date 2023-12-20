
GET_ENDPOINTS = ['/products', '/series', '/securities', '/clearing_currencies', '/snapshots', '/live_snapshots', '/indicative_margin', '/config', '/global_scenarios']

POST_ENDPOINTS = ['/estimator', '/otc_trade_details', '/otc_sensitivities', '/greeks', '/stressmatrix', '/convert/etd/cp005', '/convert/otc/shorthand', '/convert/cash/csv', '/default_fund', '/stress_test']


class GET:
    products = '/products'
    series = '/series'
    securities = '/securities'
    clearing_currencies = '/clearing_currencies'
    snapshots = '/snapshots'
    live_snapshots = '/live_snapshots'
    indicative_margin = '/indicative_margin'
    config = '/config'
    global_scenarios = '/global_scenarios'


class POST:
    estimator = '/estimator'
    otc_trade_details = '/otc_trade_details'
    otc_sensitivities = '/otc_sensitivities'
    greeks = '/greeks'
    stressmatrix = '/stressmatrix'
    convert_etd_cp005 = '/convert/etd/cp005'
    convert_otc_shorthand = '/convert/otc/shorthand'
    convert_cash_csv = '/convert/cash/csv'
    default_fund = '/default_fund'
    stress_test = '/stress_test'
