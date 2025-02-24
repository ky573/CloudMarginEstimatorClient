import csv
import click
from cpme_api.models import BodyEstimator
import cpme_api.models as spec


class EstimatorRequestHandlerBase:
    GUI_HEADER = "Product ID,Contract Date,Call Put Flag,Exercise Price,Version Number,Net LS Balance"
    INNER_HEADER = "call_put_flag,component_margin,component_margin_currency,contract_date,exercise_price,exercise_style,iid,instrument_type,line_no,liquidation_group,liquidation_group_split,maturity,net_ls_balance,premium_margin,premium_margin_currency,product_id,version_number"

    def __init__(self):
        self.gui_header = False
        self.inner_header = False

    def setup_estimator_request_gui(self,
                                    business_day: int,
                                    portfolio: str,
                                    version: bool,
                                    timestamp: int
                                    ) -> BodyEstimator:
        """
        Sets up the body for the POST request to /estimator endpoint.

        Args:
            business_day: required business date
            portfolio: portfolio to be sent to endpoint
            version: desired version
            timestamp: desired timestamp

        Returns:
            Estimator body to be used in request and sent to endpoint
        """
        request_body = self.setup_request_body(business_day, timestamp, version)

        etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=self.load_portfolio(portfolio))

        request_body.portfolio_components.append(etd_csv_comp)
        return request_body

    def setup_estimator_request_inner(self,
                                      business_day: int,
                                      portfolio: str,
                                      version: bool,
                                      timestamp: int
                                      ) -> BodyEstimator:
        """
        Sets up the body for the POST request to /estimator endpoint.

        Args:
            business_day: required business date
            portfolio: portfolio to be sent to endpoint
            version: desired version
            timestamp: desired timestamp

        Returns:
            Estimator body to be used in request and sent to endpoint
        """
        request_body = self.setup_request_body(business_day, timestamp, version)

        etd_p_comp = spec.BodyEstimatorPortfolioComponents(type='etd_portfolio')

        with open(portfolio, mode='r', newline='', encoding="utf-8") as file:
            reader = csv.reader(file)

            header = next(reader)

            for row in reader:
                pc_etd = spec.EtdPositionsInner()

                for key, value in zip(header, row):
                    setattr(pc_etd, "_" + key, value)

                etd_p_comp.etd_portfolio.append(pc_etd)

        request_body.portfolio_components.append(etd_p_comp)
        return request_body

    @staticmethod
    def setup_request_body(business_day: int, timestamp: int, version: bool) -> BodyEstimator:
        """
        Sets up the body for the POST request to /estimator endpoint.

        Args:
            business_day: required business date
            version: desired version
            timestamp: desired timestamp

        Returns:
            Estimator body to be used in request and sent to endpoint
        """
        request_body = BodyEstimator()
        request_body.snapshot = spec.Snapshot()
        request_body.snapshot.live = version
        request_body.snapshot.business_date = business_day
        request_body.snapshot.live_timestamp = timestamp
        request_body.clearing_currency = "EUR"

        return request_body

    def create_correct_request_body(self,
                                    business_date: int,
                                    csv_file: str,
                                    version: bool,
                                    timestamp: int
                                    ) -> BodyEstimator:
        if self.gui_header:
            estimator_request_body = self.setup_estimator_request_gui(business_date,
                                                                      csv_file,
                                                                      version,
                                                                      timestamp)
        else:
            estimator_request_body = self.setup_estimator_request_inner(business_date,
                                                                        csv_file,
                                                                        version,
                                                                        timestamp)

        return estimator_request_body

    @staticmethod
    def load_portfolio(portfolio: str) -> str:
        """Loads and returns the portfolio as a string."""
        with open(portfolio, 'r', encoding="utf-8") as f:
            return f.read()

    def _validate_header(self, csv_file: str) -> bool:
        """Validates the CSV file headers against the required format."""
        try:
            with open(csv_file, mode='r', newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)
                if headers is None:
                    raise ValueError("CSV file is empty.")

                headers_str = ",".join(headers)
                if headers_str == self.GUI_HEADER:
                    self.gui_header = True
                elif headers_str == self.INNER_HEADER:
                    self.inner_header = True

                if not self.gui_header and not self.inner_header:
                    raise ValueError(f"Headers mismatch. Expected: either '{self.GUI_HEADER}' "
                                     f"or '{self.INNER_HEADER}', Found: '{headers_str}'.")

            click.echo("Headers validated successfully.")
            return True
        except (ValueError, FileNotFoundError) as e:
            click.echo(f"Error validating CSV headers: {e}")
            return False
