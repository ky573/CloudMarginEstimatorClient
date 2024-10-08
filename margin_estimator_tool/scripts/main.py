import click
from margin_estimator_tool.margin_calculator.calculator import MarginCalculator
from margin_estimator_tool.margin_calculator.utils import check_click_arguments
from margin_estimator_tool.margin_calculator.portfolio_loader import PortfolioLoader


@click.command()
@click.option('--date_from', required=True, type=str, help='Start date in YYYYMMDD format')
@click.option('--date_to', required=True, type=str, help='End date in YYYYMMDD format')
@click.option('--export_dir', required=True, type=click.Path(), help="Directory to save the graph and Excel file.")
def main(date_from: str, date_to: str, export_dir: str) -> None:
    """Main function to run the margin calculation."""
    check_click_arguments(date_from, date_to, export_dir)
    portfolio = PortfolioLoader().load_portfolio()
    calculator = MarginCalculator(portfolio)
    calculator.run(date_from, date_to, export_dir)


if __name__ == '__main__':
    main()
