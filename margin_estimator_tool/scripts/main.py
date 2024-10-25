import click
from margin_estimator_tool.margin_calculator.calculator import MarginCalculator
from margin_estimator_tool.margin_calculator.utils import check_click_arguments
from margin_estimator_tool.margin_calculator.portfolio_loader import PortfolioLoader
from margin_estimator_tool.margin_calculator.products_request_handler import ProductsRequestHandler


@click.command()
@click.option('--date_from', required=True, type=str, help='Start date in YYYYMMDD format')
@click.option('--date_to', required=True, type=str, help='End date in YYYYMMDD format')
@click.option('--export_dir', required=True, type=click.Path(), help="Directory to save the graph and Excel file.")
@click.option('--get_product', is_flag=True, help='Export products data.')
@click.option('--date', type=str, help='Fetch products from a specific date (YYYYMMDD).')
@click.option('--version', type=click.Choice(['SOD', 'LIVE']), help='Fetch products based on version.')
@click.option('--to_excel', is_flag=True, help='Export as Excel file.')
@click.option('--to_json', is_flag=True, help='Export as JSON file.')
@click.option('--filter', type=str, help='Filter products based on key:value pairs.')
def main(date_from: str, date_to: str, export_dir: str, get_product: bool, date: str, version: str, to_excel: bool, to_json: bool, filter: str) -> None:
    """Main function to run the margin calculation."""
    if not get_product:
        portfolio = PortfolioLoader().load_portfolio()
        calculator = MarginCalculator(portfolio)
        calculator.run(date_from, date_to, export_dir)
    else:
        handler = ProductsRequestHandler(
            date=date,
            version=version,
            filters=filter,
            to_excel=to_excel,
            to_json=to_json,
            export_dir=export_dir
        )
        handler.process_and_export()


if __name__ == '__main__':
    main()
