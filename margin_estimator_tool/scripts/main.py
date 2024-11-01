import click
from margin_estimator_tool.margin_calculator.products_request_handler import ProductsRequestHandler
from margin_estimator_tool.margin_calculator.estimator_request_handler import EstimatorRequestHandler
from margin_estimator_tool.margin_calculator.request_handler_base import RequestHandler
from typing import Optional


@click.group()
def cli():
    """Main CLI group for margin estimator tool."""
    pass


@cli.command(name="post_estimator")
@click.option('--date_from', required=True, type=str, help='Start date in YYYYMMDD format')
@click.option('--date_to', required=True, type=str, help='End date in YYYYMMDD format')
@click.option('--export_dir', required=True, type=click.Path(), help="Directory to save output.")
def post_estimator(date_from: str, date_to: str, export_dir: str) -> None:
    """Run estimator endpoint."""
    handler = EndpointHandlerFactory.get_handler("post_estimator",
                                                 date_from=date_from,
                                                 date_to=date_to,
                                                 export_dir=export_dir)
    handler.send_request()


@cli.command(name="get_products")
@click.option('--date', type=str, help='Fetch products from a specific date (YYYYMMDD).')
@click.option('--version', type=click.Choice(['SOD', 'LIVE']), help='Fetch products based on version.')
@click.option('--to_excel', is_flag=True, help='Export as Excel file.')
@click.option('--to_json', is_flag=True, help='Export as JSON file.')
@click.option('--export_dir', type=click.Path(), help="Directory to save output.")
@click.option('--filter', type=str, help='Filter products based on key:value pairs.')
def get_products(date: Optional[str],
                 version: Optional[str],
                 to_excel: Optional[bool],
                 to_json: Optional[bool],
                 export_dir: Optional[str],
                 filter: Optional[str]) -> None:
    """Fetch products from the products endpoint."""
    handler = EndpointHandlerFactory.get_handler("get_products",
                                                 date=date,
                                                 version=version,
                                                 to_excel=to_excel,
                                                 to_json=to_json,
                                                 export_dir=export_dir,
                                                 filters=filter)

    # so far works just because of python ducktyping and only for products, needs a rework of structure
    handler.process_and_export()


class EndpointHandlerFactory:
    """Factory for creating desired request handler based on CLI."""

    @staticmethod
    def get_handler(endpoint: str, **kwargs) -> RequestHandler:
        """Creates and returns desired handler."""
        if endpoint == "post_estimator":
            return EstimatorRequestHandler(**kwargs)
        elif endpoint == "get_products":
            return ProductsRequestHandler(**kwargs)
        else:
            raise ValueError(f"No handler defined for endpoint: {endpoint}")


if __name__ == '__main__':
    cli()
