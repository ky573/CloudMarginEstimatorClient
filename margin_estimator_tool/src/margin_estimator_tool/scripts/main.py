#! /usr/bin/env python3

"""
Main module of the application, contains the starting point.
"""


import click
from typing import Optional
from margin_estimator_tool.src.margin_estimator_tool.products.products_request_handler import ProductsRequestHandler
from margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.margin_calculator_request_handler import MarginCalculatorRequestHandler
from margin_estimator_tool.src.margin_estimator_tool.series.series_request_handler import SeriesRequestHandler
from margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler import LiveSnapshotRequestHandler
from margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler import SnapshotRequestHandler
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.estimator.etd_portfolio.etd_portfolio_request_handler import EtdPortfolioRequestHandler
from margin_estimator_tool.src.margin_estimator_tool.core.argument_validator import (GetProductsValidator,
                                                                                     MarginCalculatorValidator,
                                                                                     GetSeriesValidator,
                                                                                     GetLiveSnapshotsValidator,
                                                                                     GetSnapshotsValidator,
                                                                                     EtdPortfolioValidator)


@click.group()
def cli():
    """Main CLI group for margin estimator tool."""
    pass


@cli.command(name="margin_calculator")
@click.option("--csv_file", required=True, type=click.Path(resolve_path=True), help="Path to the ETD portfolio CSV file.")
@click.option("--version", type=click.Choice(["SOD", "LIVE"]), help="Snapshot version.")
@click.option("--timestamp", type=int, help="Timestamp for LIVE version.")
@click.option("--date_from", required=True, type=str, help="Start date in YYYYMMDD format")
@click.option("--date_to", required=True, type=str, help="End date in YYYYMMDD format")
@click.option("--export_dir", required=True, type=click.Path(resolve_path=True), help="Directory to save output.")
def post_estimator(csv_file: str,
                   version: Optional[str],
                   timestamp: Optional[str],
                   date_from: str,
                   date_to: str,
                   export_dir: str
                   ) -> None:
    """Run estimator endpoint."""
    validator = MarginCalculatorValidator()
    validator.validate(csv_file=csv_file, date_from=date_from, date_to=date_to, export_dir=export_dir)

    handler = EndpointHandlerFactory.get_handler("margin_calculator",
                                                 csv_file=csv_file,
                                                 version=version,
                                                 timestamp=timestamp,
                                                 date_from=date_from,
                                                 date_to=date_to,
                                                 export_dir=export_dir)
    handler.process_and_provide_output()


@cli.command(name="get_products")
@click.option("--date", type=str, help="Fetch products from a specific date (YYYYMMDD).")
@click.option("--version", type=click.Choice(["SOD", "LIVE"]), help="Fetch products based on version.")
@click.option("--to_excel", is_flag=True, help="Export as Excel file.")
@click.option("--to_json", is_flag=True, help="Export as JSON file.")
@click.option("--export_dir", type=click.Path(resolve_path=True), help="Directory to save output.")
@click.option("--timestamp", type=int, help="This defines the timestamp for the products data for LIVE version.")
@click.option("--filter", type=str, help="""Filter products based on key:value pairs separated by comma.
                                                        The extrafields with examples are:\n
                                                        "clearing_house": "EUXCDEFF",\n
                                                        "prod_name": "OPT ON SWISS MARKET INDEX",\n
                                                        "prod_isin": "CH0008616382",\n
                                                        "underlying_isin": "CH0009980894",\n
                                                        "currency": "CHF",\n
                                                        "product_type": "OINX",\n
                                                        "extended_product_type": null,\n
                                                        "margin_style_flag": "T",\n
                                                        "exercise_style_flag": "E",\n
                                                        "product_settlement_type": "CASH",\n
                                                        "final_settlement_time": "09:00",\n
                                                        "product_tick_size": 0.1,\n
                                                        "product_tick_value": 1,\n
                                                        "liquidation_group": "PEQ01",\n
                                                        "xm_eligibility": false
                                                        """)
def get_products(date: Optional[str],
                 version: Optional[str],
                 to_excel: Optional[bool],
                 to_json: Optional[bool],
                 export_dir: Optional[str],
                 timestamp: Optional[int],
                 filter: Optional[str]
                 ) -> None:
    """Fetch products from the products endpoint."""
    validator = GetProductsValidator()
    validator.validate(date=date, export_dir=export_dir)

    handler = EndpointHandlerFactory.get_handler("get_products",
                                                 date=date,
                                                 version=version,
                                                 to_excel=to_excel,
                                                 to_json=to_json,
                                                 export_dir=export_dir,
                                                 timestamp=timestamp,
                                                 filters=filter)
    handler.process_and_provide_output()


@cli.command(name="get_series")
@click.option("--date", type=str, help="Fetch products from a specific date (YYYYMMDD).")
@click.option("--version", type=click.Choice(["SOD", "LIVE"]), help="Fetch products based on version.")
@click.option("--timestamp", type=int, help="This defines the timestamp for the series data.")
@click.option("--to_excel", is_flag=True, help="Export as Excel file.")
@click.option("--to_json", is_flag=True, help="Export as JSON file.")
@click.option("--export_dir", type=click.Path(resolve_path=True), help="Directory to save output.")
@click.option("--products", type=str, required=True, help="Allows filtering series by product names.")
@click.option("--type", type=click.Choice(["option", "future"]), help="Filters the series based on type.")
@click.option("--call_put_flag", type=click.Choice(["C", "P"]), help="Filters the series based on call/put.")
@click.option("--template", is_flag=True, help="Generate template for ETD portfolio.")
@click.option("--max_tte", type=int, help="Filters based on the days_to_expiration (time to expiry).")
@click.option("--min_tte", type=int, help="Filters based on the days_to_expiration (time to expiry).")
@click.option("--filter", type=str, help="""Filter series based on key:value pairs separated by comma.
                                                        The extrafields with examples are:\n
                                                        "iid": 78490800,\n
                                                        "product_id": "BMW",\n
                                                        "contract_date": 20250321,\n
                                                        "contract_maturity": 202503,\n
                                                        "expiry_maturity": 202503,\n
                                                        "version_number": "0",\n
                                                        "act_trade_unit_no": 100.0,\n
                                                        "days_to_expiration": 50,\n
                                                        "trade_unit_value": 100.0,\n
                                                        "contract_frequency": "MONTHLY",\n
                                                        "call_put_flag": "P",\n
                                                        "exercise_price": 91.0,\n
                                                        "exercise_style_flag": "A"
                                                        """)
def get_series(date: Optional[str],
               version: Optional[str],
               timestamp: Optional[int],
               to_excel: Optional[bool],
               to_json: Optional[bool],
               export_dir: Optional[str],
               products: Optional[str],
               type: Optional[str],
               call_put_flag: Optional[str],
               filter: Optional[str],
               template: Optional[bool],
               max_tte: Optional[int],
               min_tte: Optional[int]
               ) -> None:
    """Fetch series from the series endpoint."""
    validator = GetSeriesValidator()
    validator.validate(date=date, export_dir=export_dir)

    handler = EndpointHandlerFactory.get_handler("get_series",
                                                 date=date,
                                                 version=version,
                                                 timestamp=timestamp,
                                                 to_excel=to_excel,
                                                 to_json=to_json,
                                                 export_dir=export_dir,
                                                 products=products,
                                                 type=type,
                                                 call_put_flag=call_put_flag,
                                                 filters=filter,
                                                 template=template,
                                                 max_tte=max_tte,
                                                 min_tte=min_tte)

    handler.process_and_provide_output()


@cli.command(name="get_live_snapshots")
@click.option("--date", required=True, type=str, help="Fetch live snapshots from a specific date (YYYYMMDD).")
def get_live_snapshots(date: str) -> None:
    """Fetch live snapshots and display information."""
    validator = GetLiveSnapshotsValidator()
    validator.validate(date=date)

    handler = EndpointHandlerFactory.get_handler("get_live_snapshots", date=date)
    handler.process_and_provide_output()


@cli.command(name="get_snapshots")
@click.option("--date_from", required=True, type=str, help="Start date in YYYYMMDD format.")
@click.option("--date_to", type=str, help="End date in YYYYMMDD format. Defaults to the current date.")
def get_snapshots(date_from: Optional[str], date_to: Optional[str]) -> None:
    """Fetch SOD snapshots (non-live) for the specified date range."""
    validator = GetSnapshotsValidator()
    validator.validate(date_from=date_from, date_to=date_to)

    handler = EndpointHandlerFactory.get_handler("get_snapshots", date_from=date_from, date_to=date_to)
    handler.process_and_provide_output()


@cli.command(name="etd_portfolio")
@click.option("--csv_file", required=True, type=click.Path(resolve_path=True), help="Path to the ETD portfolio CSV file.")
@click.option("--date", type=str, help="Specific business date (YYYYMMDD).")
@click.option("--version", type=click.Choice(["SOD", "LIVE"]), help="Snapshot version.")
@click.option("--timestamp", type=int, help="Timestamp for LIVE version.")
@click.option("--to_excel", is_flag=True, help="Export results to an Excel file.")
@click.option("--to_json", is_flag=True, help="Export results to a JSON file.")
@click.option("--export_dir", type=click.Path(resolve_path=True), help="Output directory for exported files.")
def etd_portfolio(csv_file: str,
                  date: Optional[str],
                  version: Optional[str],
                  timestamp: Optional[int],
                  to_excel: Optional[bool],
                  to_json: Optional[bool],
                  export_dir: Optional[str]
                  ) -> None:
    """Uploads an ETD portfolio from a CSV file and processes it."""
    validator = EtdPortfolioValidator()
    validator.validate(csv_file=csv_file, date=date, export_dir=export_dir)

    handler = EndpointHandlerFactory.get_handler("etd_portfolio",
                                                 csv_file=csv_file,
                                                 date=date,
                                                 version=version,
                                                 timestamp=timestamp,
                                                 to_excel=to_excel,
                                                 to_json=to_json,
                                                 export_dir=export_dir)
    handler.process_and_provide_output()


class EndpointHandlerFactory:
    """Simple Factory for creating desired request handler based on CLI."""

    @staticmethod
    def get_handler(endpoint: str, **kwargs) -> RequestHandler:
        """
        Creates and returns desired handler.

        Args:
            endpoint: desired enpoint for which the concrete request handler will be created
            **kwargs: arguments from the CLI

        Returns:
            RequestHandler: concrete instance of the request handler
        """
        if endpoint == "margin_calculator":
            return MarginCalculatorRequestHandler(**kwargs)
        elif endpoint == "get_products":
            return ProductsRequestHandler(**kwargs)
        elif endpoint == "get_series":
            return SeriesRequestHandler(**kwargs)
        elif endpoint == "get_live_snapshots":
            return LiveSnapshotRequestHandler(**kwargs)
        elif endpoint == "get_snapshots":
            return SnapshotRequestHandler(**kwargs)
        elif endpoint == "etd_portfolio":
            return EtdPortfolioRequestHandler(**kwargs)
        else:
            raise ValueError(f"No handler defined for endpoint: {endpoint}")


if __name__ == "__main__":
    cli()
