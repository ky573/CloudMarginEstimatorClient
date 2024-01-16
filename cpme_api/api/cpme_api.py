from cpme_api.api.feature.api_client import ApiClient
from cpme_api.api.configuration import Configuration
from copy import copy
from cpme_api.models.responses import products, series


class BaseApi(object):

    _opt_params = ['async_req', 'verbose', 'request_timeout', 'api_key']

    _check_validation = True

    def __init__(self, set_validation: bool = None):
        if not set_validation:
            BaseApi.set_validation(False)

    @classmethod
    def set_validation(cls, flag : bool = True):
        cls._check_validation = flag

    @classmethod
    def _params_check(cls, params, defined_params):
        new_p = {'defined': copy(defined_params)}
        defined_params.extend(cls._opt_params)
        for key, val in params['kwargs'].items():
            if cls._check_validation and (key not in defined_params):
                raise TypeError(
                    "Got an unexpected keyword argument '%s'" % key
                )
            new_p[key] = val

        if cls._check_validation:
            # verify the required parameter 'x_dbp_apikey' is set
            if ('api_key' not in new_p.keys()) and ('x_dbp_apikey' not in new_p.keys()):
                raise ValueError("Missing the required parameter `x_dbp_apikey` when calling xxx")
            if new_p.get('api_key'):
                new_p['x_dbp_apikey'] = copy(new_p['api_key'])
                del new_p['api_key']
        return new_p


class CpmeApi(BaseApi):
    """
    class
    """

    def __init__(self, configuration: Configuration = None, set_validation: bool = None):
        super(CpmeApi, self).__init__(set_validation)
        if configuration is None:
            configuration = Configuration()
        self.configuration = configuration
        self._api_client = ApiClient(configuration)

    def close(self):
        self._api_client.close()

    def clearing_currencies_get(self, **kwargs):
        """List All Clearing Currencies

        List of clearing currencies that can be used in `estimator` request.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.clearing_currencies_get(x_dbp_apikey, async_req=True)
        >>> result = thread.get()

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param float business_date: Business date as of which the result is calculated, in YYYYMMDD format
        :param bool live: Is the snapshot live (a.k.a. intraday)? False for end-of-day.
        :param float live_timestamp: Timestamp as of which the result is calculated, in milliseconds from epoch. Zero means the first live snapshot.
        :return: RespClearingCurrencies
        """
        all_params = ['x_dbp_apikey', 'business_date', 'live', 'live_timestamp']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/clearing_currencies', 'GET',
            params,
            response_type='RespClearingCurrencies'
        )

    def securities_get(self, **kwargs):
        """Get attributes of securities

        Get attributes of securities (equities, bonds, subscription rights) for given ISIN, or all active securities known to the Risk system if ISIN is not specified.
        The margin class returned with the security is its default margin class and the currency is the default margin class currency. Bonds always have only one margin class,
        the default one. Equities may be assigned to multiple margin classes based on settlement currency of the transaction - this is intended for some ETFs.
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param float business_date: Business date as of which the result is calculated, in YYYYMMDD format
        :param bool live: Is the snapshot live (a.k.a. intraday)? False for end-of-day.
        :param float live_timestamp: Timestamp as of which the result is calculated, in milliseconds from epoch. Zero means the first live snapshot.
        :param str isin: Security ISIN
        :return: RespSecurities
        """
        all_params = ['x_dbp_apikey', 'business_date', 'live', 'live_timestamp', 'isin']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/securities', 'GET',
            params,
            response_type='RespSecurities'
        )

    def products_get(self, **kwargs):
        """List All Products

        Lists all exchange-traded products, Eurex and ECC. Only `product` and `instrument_type` are returned by default. Remaining attributes (see response) are returned only if specified in `extrafields`.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param bool async_req:
        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param list[str] extrafields: comma-separated list of optional fields that should be returned in addition to the default set of response fields. Alternatively can be specified also as multiple parameter instances instead of comma-separated list.
        :param float business_date: Business date as of which the result is calculated, in YYYYMMDD format
        :param bool live: Is the snapshot live (a.k.a. intraday)? False for end-of-day.
        :param float live_timestamp: Timestamp as of which the result is calculated, in milliseconds from epoch. Zero means the first live snapshot.
        :return: RespProducts
        """
        all_params = ['x_dbp_apikey', 'extrafields', 'business_date', 'live', 'live_timestamp']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/products', 'GET',
            params,
            response_type='RespProducts',
            collection_format={'extrafields': 'csv'}
        )

    def series_get(self, **kwargs):
        """List Series of a Product

        List all series of exchange traded product(s). Attributes upto `iid` are returned by default. Remaining attributes (see response) are returned only if specified in `extrafields`.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param list products: Product ID, there can be multiple instances of the parameter to request series for several products (required)
        :param list[str] extrafields: comma-separated list of optional fields that should be returned in addition to the default set of response fields. Alternatively can be specified also as multiple parameter instances instead of comma-separated list.
        :param float business_date: Business date as of which the result is calculated, in YYYYMMDD format
        :param bool live: Is the snapshot live (a.k.a. intraday)? False for end-of-day.
        :param float live_timestamp: Timestamp as of which the result is calculated, in milliseconds from epoch. Zero means the first live snapshot.
        :param bool flex: Return also flex series? True or false. Default setting is false.
        :return: RespSeries
        """
        all_params = ['x_dbp_apikey', 'products', 'extrafields', 'business_date', 'live', 'live_timestamp',
                      'flex']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/series', 'GET',
            params,
            response_type='RespSeries',
            collection_format={'extrafields': 'csv', 'products': 'multi'}
        )

    def snapshots_get(self, **kwargs):
        """List Available Snapshots

        List of end-of-day or first live snapshots that can be used in other requests.
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param float business_date_from: Start of a date range, in YYYYMMDD format
        :param float business_date_to: End of a date range, in YYYYMMDD format
        :return: RespSnapshots
        """
        all_params = ['x_dbp_apikey', 'business_date_from', 'business_date_to']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/snapshots', 'GET',
            params,
            response_type='RespSnapshots'
        )

    def config_param_get(self, **kwargs):
        """Read configuration parameter  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param str param: name of the parameter (required)
        :return: RespConfig
        """
        all_params = ['x_dbp_apikey', 'param']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        params['q_path'] = params.pop('param')
        return self._api_client.call_api(
            '/config/', 'GET',
            params,
            response_type='RespConfig'
        )

    def global_scenarios_get(self, **kwargs):
        """List global scenarios used by Default Fund Estimator

        The numerical id (gscnid) is used in `stress_value_per_global_scenario` array in POST `/default_fund` response.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param bool async_req:
        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :return: RespGlobalScenarios
        """
        all_params = ['x_dbp_apikey']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/global_scenarios', 'GET',
            params,
            response_type='RespGlobalScenarios'
        )

    def indicative_margin_get(self, **kwargs):
        """Indicative margin for front month future contracts

        Get indicative margin for one future contract (front month contract of given future product) in EUR. By default all Eurex futures are included, unless ECC clearing house is selected or a specific product or products is requested. The resulting long_initial_margin_cash and short_initial_margin_cash is equivalent to the margin calculated by individual /estimator requests for portfolio of one long or short contract, respectively. The relative long_initial_margin and short_initial_margin is the cash margin divided by (current underlying price converted to EUR * trade unit value). Optionally business date can be specified to get historical indicative margins, by default CPME returns the most recent values. In contrast to estimator request, which uses end-of-day for historical calculation (unless time is specified), indicative margin is by default for the first live snapshot (published in the morning to indicate margin during the day). As an alternative to selecting one business_date, time series can be requested using business_date_from, business_date_to attributes. This is available only for JSON output format.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param str clearing_house: Either EUXCDEFF (i.e. Eurex, the default choice) or EEXCDE8L (i.e. European Commodity Clearing, linked to EEX = European Energy Exchange).
        :param list products: Product ID of the future, there can be multiple instances of the parameter to request margin for several future products. If not provided the result will contain margin for all future products.
        :param str format: Required result format, JSON (default), XLS or XLSX spreadsheet.
        :param float business_date: Business date as of which the result is calculated, in YYYYMMDD format
        :param float business_date_from: Start of a date range, in YYYYMMDD format
        :param float business_date_to: End of a date range, in YYYYMMDD format
        :param bool live: Is the snapshot live (a.k.a. intraday)? False for end-of-day.
        :param bool include_components: Include breakdown of the initial margin to market risk and other components. Also include details for market risk - results on risk measure set level. Available only in JSON format.
        :return: IndicativeMargin200
        """
        all_params = ['x_dbp_apikey', 'clearing_house', 'products', 'format', 'business_date', 'business_date_from',
                      'business_date_to', 'live', 'include_components']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/indicative_margin', 'GET',
            params,
            response_type='IndicativeMargin200',
            collection_format={'products': 'multi'}
        )

    def live_snapshots_get(self, **kwargs):
        """List Available Live Snapshots for Given Day

        List of live (intraday) snapshots for given business_date.
        This method makes a synchronous HTTP request by default.

        :param async_req bool
        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param float business_date: Business date as of which the result is calculated, in YYYYMMDD format
        :return: RespLiveSnapshots
        """
        all_params = ['x_dbp_apikey', 'business_date']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/live_snapshots', 'GET',
            params,
            response_type='RespLiveSnapshots'
        )

    def estimator_post(self, body, **kwargs):
        """Margin Calculation Request

        Margin Calculation Portfolio is sent in the request and margin is returned as a response. The request can contain exchange traded derivatives (ETD) portfolio, OTC portfolio or Cash Market portfolio (equities and bonds) or any combination of these assets: - ETD is submitted as   - `etd_portfolio` JSON array, see request model   - or `etd_csv` with positions in CSV format   - or `etd_cp005`, i.e. using Eurex CP005 XML report  - OTC is submitted as   - `otc_csv` with trades in CSV format known from Margin Calculator or Prisma Margin Estimator, see description bellow   - or `otc_sensitivities` with sensitivities in CSV format   - or `otc_fpml`   - or `otc_cb202`, i.e. EurexOTC CB202 or CB207 report   - or `otc_cc233`, i.e. EurexOTC CC233 OTC Sensitivities report  - Cash Market is submitted as   - `repo_json` JSON array of `repo_json_position` objects, see the model   - other Cash Market instruments are currently not supported  ## ETD portfolio as JSON array `etd_portfolio` instruments are specified either by full key  or by technical `iid`. The technical `iid` takes precedence if both keys are sent. The position always needs `line_no` and `net_ls_balance`. The full key for series depends on instrument type, these are the mandatory fields: - Future: `product`, `contract_date` as YYYYMMDD, `version_number` (defaults to 0) - Option: `product`, `contract_date` as YYYYMMDD, `call_put_flag`, `exercise_price`, `version_number` (defaults to 0) - Flex Future: `instrument_type`: \"Flex Future\", `product`, `contract_date` as YYYYMMDD, `version_number` (defaults to 0) - Flex Option: `instrument_type`: \"Flex Option\", `product`, `contract_date` as YYYYMMDD, `call_put_flag`, `exercise_price`, `exercise_style`, `version_number` (defaults to 0)  Only already existing Flex Future or Flex Option can be submitted, not a new one (e.g. different strike or expiry day). For backward compatibility `maturity` as YYYYMM (DD added for flex) can be used instead of `contract_date`, however it is not recommended as uniqueness is not guaranteed. Example of minimal request with one future contract:  <pre> curl --header 'X-DBP-APIKEY: your-key' \\   https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0/estimator \\   -d '{\"portfolio_components\":[{\"type\":\"etd_portfolio\",\"etd_portfolio\":[{\"line_no\":1,\"product_id\":\"FEXD\",\"contract_date\":20301220,\"net_ls_balance\":1}]}]}' </pre>  ## OTC CSV format The CSV describing all trades is submitted as one string in `csv` attribute of `otc_csv` structure starting with header. Lines separated by `\\n`. One line contains all information for one trade, including both its legs. All columns must be present, although some can be empty. Mandatory columns are marked by asterisk *. For certain trade types, even some optional columns must be filled, see the description. If unsure about possible combinations of attribute values please refer to   [EurexOTC Clear IRS Product List](https://www.eurexclearing.com/resource/blob/227404/ff4638f2a3bfedbf511868ef54c6a153/data/ec15075e_Attach.pdf)   or the [OTC template description](https://github.com/Deutsche-Boerse-Risk/CloudPrismaMarginEstimator/raw/master/templates/otc/OTC_template_description.xls).   ### Basic OTC trade attributes - internalTradeID*: id of the trade to distinguish it in drilldown, must be unique - tradeType*: IRS, Basis swap, OIS, FRA, VNS, ZCIS - currency*: ISO code of currency, e.g. EUR, CHF, USD, GBP - effectiveDate*: effective date as DD/MM/YYYY, e.g. 20/12/2018 - terminationDate*: termination date as DD/MM/YYYY, e.g. 20/12/2028  ### Pay leg attributes - payLegType*: fixedLeg or floatingLeg - payLegSpread: rate for fixedLeg in %, or spread (optional) for floatingLeg in bp - payLegIndex: index for floatingLeg, if empty, default index for the currency is selected - payInterestFixedAmount: allowed for fixedLeg only, lump sum paid at maturity of zero coupon swap - payNotional*: notional - payPaymentPeriod*: 1M, 3M, 6M, 12M, 1Y, 1T (for zero-coupon); inflation swaps always use 1T no matter what period is given - payPeriodStartVNS: fill only for VNS - payCompounding: fill only for compounding swap, Flat or Straight - payCompoundingIndexPeriod: period for compounding swap, 1M, 3M, 6M, 12M, 1Y - payStub: fill only if the leg has a stub, LongFinal, LongInitial, ShortInitial, ShortFinal - payFirstRate: first pre-defined rate - payFirstInterpolationTenor: stub interpolation tenor for floatingLeg, 1W, 1M, 3M, 6M, ... - paySecondInterpolationTenor: stub interpolation tenor for floatingLeg, 1W, 1M, 3M, 6M, ... - payDayCountMethod*: 30/360, 30E/360, 30E/360.ISDA, ACT/360, ACT/365.FIXED, ACT/ACT.ISDA, ACT/365.ISDA, ACT/ACT.ICMA, ACT/ACT.ISMA, 1/1, ... - payBusinessDayConvention: MODFOLLOWING, FOLLOWING, PRECEDING, ... - payPaymentCalendar: EUTA, CHZU, GBLO, USNY, DEFR, ITMI, FRPA, ESMA, BEBR, JPTO, DKCO, NOOS, SEST, PLWA, ... calendars can be combined with \"+\"; unknown calendar is ignored - payAdjustment: ADJUSTED, UNADJUSTED, MAT_UNADJUSTED, ... - payRollMethod: Standard, IMM, EOM, ...  ### Receive leg attributes The receive leg has the same attributes as pay leg above, except prefix \"pay\" is replaced by \"rcv\". ## OTC sensitivities in CSV format The whole portfolio is described by a table of DV01 sensitivities, submitted in CSV format known from Margin Calculator. The columns are curves and rows maturities - see the example in request model. ## OTC reports CB202, CB207 See Eurex OTC member documentation for CB202 and CB207 reports. Only positions from one specified account or risk netting unit (ARNU) will be evaluated, see the attributes of `otc_cb202` structure below. We recommend using gzip compression in the request, see above. ## OTC FpML See the public definition for FpML format. It is submitted as `otc_fpml`. The `party` attribute is mandatory, see below. We recommend using gzip compression in the request, see above. ## Repo JSON `portfolio_components/repo_json` defines special Repo (single-ISIN Repo) positions. For attribute details see the model below. # What-If analysis Estimator request allows to perform what-if analysis for ETD and OTC, i.e. it answers the question what would be the portfolio margin when a set of positions or trades is added to a base portfolio. The added trades are submitted a separate portfolio component(s) marked by non-zero whatif_id. Multiple scenarios (different sets of trades to add) can be tested with one request, the scenarios are distinguished by whatif_id. Results for the base portfolio are returned in portfolio_margin as for standard request. Portfolio margins for the scenarios are returned in array whatif_portfolio_margin. They are total margins for the base portfolio plus the added trades. To learn the margin increase or decrease caused by the added trades, subtract margin of the base portfolio from the what-if portfolio margin. Drilldowns are returned only for the base portfolio.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param BodyEstimator body: (required)
        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :return: RespEstimator
        """
        all_params = ['body', 'x_dbp_apikey']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/estimator', 'POST',
            body=body,
            params=params,
            response_type='RespEstimator'
        )

    def convert_cash_csv_post(self, body, **kwargs):
        """Convert cash market portfolio in CSV format to JSON representation

        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param CashCsv body:
        :return: ResponseConvertCashCsv
        """

        all_params = ['x_dbp_apikey', 'body']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/convert/cash/csv', 'POST',
            body=body,
            params=params,
            response_type='CashJson'
        )

    def convert_etd_cp005_post(self, body, **kwargs):
        """Convert Eurex ETD CP005 position report to JSON ETD representation for CPME

        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param BodyConvertEtdCp005 body:
        :return: EtdPortfolio
        """

        all_params = ['x_dbp_apikey', 'body']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/convert/etd/cp005', 'POST',
            body=body,
            params=params,
            response_type='EtdPortfolio'
        )

    def convert_otc_shorthand_post(self, body, **kwargs):
        """Convert a short text description of the trade to OTC CSV

        Text description of a trade similar to Clarus Quick Trade format is converted to OTC CSV representation that can be used for margin calculation. Response contains also trade details. The expected trade format is contains currency, notional, maturity, side and optionaly rate. E.g. \"USD 200m 10Y pay 1.5%\". When the rate is not given, CPME uses par-rate.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param BodyOtcShorthand body:
        :return: RespConvertOtcShorthand
        """

        all_params = ['x_dbp_apikey', 'body']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/convert/otc/shorthand', 'POST',
            body=body,
            params=params,
            response_type='RespConvertOtcShorthand'
        )

    def default_fund_post(self, body, **kwargs):
        """Approximate Calculation of Default Fund contribution

        Portfolio is sent in the request and Default Fund contribution is returned as a response. The request can contain exchange traded derivatives (ETD) portfolio, or Cash Market portfolio (equities, bonds, repos) or any combination of these assets: - ETD is submitted as   - `etd_portfolio` JSON array, see request model   - or `etd_csv` with positions in CSV format   - or `etd_cp005`, i.e. using Eurex CP005 XML report  - Cash Market is submitted as   - `repo_json` JSON array of `repo_json_position` objects, see the model   - `cash_json` JSON array of `cash_json_position` objects, see the model   - or `cash_csv` with cash market positions in CSV format  See the `/estimator` request for description of the input structures Example of minimal request with one future contract:  <pre> curl --header 'X-DBP-APIKEY: your-key' \\   https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0/default_fund \\   -d '{\"portfolio_components\":[{\"type\":\"etd_portfolio\",\"etd_portfolio\":[{\"line_no\":1,\"product_id\":\"FEXD\",\"contract_date\":20301220,\"net_ls_balance\":1}]}]}' </pre>  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param BodyDefaultFund body: (required)
        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :return: RespDefaultFund
        """

        all_params = ['body', 'x_dbp_apikey']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/default_fund', 'POST',
            body=body,
            params=params,
            response_type='RespDefaultFund'
        )

    def greeks_post(self, body, **kwargs):
        """Greek Calculation Request

        Calculate analytical greeks (sensitivities) for given exchange traded instruments. The instruments are specified by a technical `iid` that can be obtained by `series` query. Two types of greeks are offered: - numerical derivative of change inprice instrument price in product currency w.r.t. change in given variable, e.g. DELTA is w.r.t. change in underlying price - the above greek converted to EUR   - EURO_DELTA, EURO_GAMMA (_underlying price + _price offset) \\offset* _greek_ \\* _fx conversion to EUR   - EURO_RHO, EURO_THETA, EURO_VEGA: _greek_ \\* _fx conversion to EUR  Optionally, vector of relative underlying shifts can be supplied to calculate stress greeks (except DV01, there shifts are ignored) in scenarios where underlying price moved. Note that the method of calculation is slightly different, therefore the result for request without shift may differ from result with zero shift. To get a position greek, the instrument greek has to be multiplied by position size and trade unit value (TUV).
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param BodyGreeks body:
        :return: RespGreeks
        """

        all_params = ['x_dbp_apikey', 'body']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/greeks', 'POST',
            body=body,
            params=params,
            response_type='RespGreeks'
        )

    def otc_sensitivities_post(self, body, **kwargs):
        """OTC Sensitivities

        Return a table of DV01 (delta) sensitivities of OTC portfolio, per curve and maturity bucket. The sensitivity table is accepted as `otc_sensitivities` input for POST /estimator request and can be used instead of the whole OTC portfolio for faster margin computation.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param BodyOtcSensitivities body:
        :return: RespOtcSensitivities
        """

        all_params = ['x_dbp_apikey', 'body']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/otc_sensitivities', 'POST',
            body=body,
            params=params,
            response_type='RespOtcSensitivities'
        )

    def otc_trade_details_post(self, body, **kwargs):
        """OTC Trade Details

        Return a short human-readable description of OTC trade, e.g. to display on a GUI. The description is not complete, i.e. it is not sufficient to evaluate the trade.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param BodyOtcTradeDetails body:
        :return: RespOtcTradeDetails
        """

        all_params = ['x_dbp_apikey', 'body']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/otc_trade_details', 'POST',
            body=body,
            params=params,
            response_type='RespOtcTradeDetails'
        )

    def stress_test_post(self, body, **kwargs):
        """Stress test calculation on system scenario level

        Portfolio is sent in the request and stress values and PnL is returned as a response. The request can contain exchange traded derivatives (ETD) portfolio, or Cash Market portfolio (equities, bonds, repos) or any combination of these assets: - ETD is submitted as   - `etd_portfolio` JSON array, see request model   - or `etd_csv` with positions in CSV format   - or `etd_cp005`, i.e. using Eurex CP005 XML report  - Cash Market is submitted as   - `repo_json` JSON array of `repo_json_position` objects, see the model   - `cash_json` JSON array of `cash_json_position` objects, see the model   - or `cash_csv` with cash market positions in CSV format  See the `/estimator` request for description of the input structures Example of minimal request with one future contract:  <pre> curl --header 'X-DBP-APIKEY: your-key' \\   https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-0/stress_test \\   -d '{\"portfolio_components\":[{\"type\":\"etd_portfolio\",\"etd_portfolio\":[{\"line_no\":1,\"product_id\":\"FEXD\",\"contract_date\":20301220,\"net_ls_balance\":1}]}]}' </pre>  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param BodyStressTest body: (required)
        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :return: RespStressTest
        """

        all_params = ['body', 'x_dbp_apikey']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/stress_test', 'POST',
            body=body,
            params=params,
            response_type='RespStressTest'
        )

    def stressmatrix_post(self, body, **kwargs):
        """Stress Matrix Request

        Calculate theoretical prices of given exchange traded instruments in stressed scenarios. The scenario can have shifted underlying price and/or volatility. In one request, vector of underlying price shifts and volatility shifts is specified and the result then contains stress matrix with prices for each combination of the underlying price and volatility shift. The volatility shift can be either relative or absolute. For example, when current volatility is 20%: - relative shift 0.1 means the stressed volatility is 20% \\* (1+0.1) = 22% - absolute shift 0.1 means stressed volatility is 20% + 0.1% = 20.1%  For futures, volatility shift has no effect and the underlying price shift changes directly the future price, theoretical pricing model is not used.  # noqa: E501
        This method makes a synchronous HTTP request by default.

        :param str x_dbp_apikey: your key, obtain it by registering at [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) (required)
        :param BodyStressmatrix body:
        :return: RespStressmatrix
        """

        all_params = ['x_dbp_apikey', 'body']
        l_params = locals()
        params = self._params_check(l_params, all_params)
        del l_params
        return self._api_client.call_api(
            '/stressmatrix', 'POST',
            body=body,
            params=params,
            response_type='RespStressmatrix'
        )

    @staticmethod
    def get_extrafields(endpoint: str):
        endpoint = endpoint.lstrip('/')
        assert endpoint in ['products', 'series'], f'extrafields is not defined for {endpoint}'
        if endpoint == 'products':
            return products.RespProductsProducts.get_properties()
        else:
            return series.RespSeriesListSeries.get_properties()
