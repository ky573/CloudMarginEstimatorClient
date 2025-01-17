"""Module to load the portfolio data from a CSV file."""

import os
import click


class PortfolioLoader:
    """Class to load the portfolio data from a CSV file."""
    def __init__(self, file: str = 'estimator_etd_csv.csv'):
        self.file = file

    def load_portfolio(self) -> str:
        """Loads portfolio data from a CSV file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        portfolio_path = os.path.join(current_dir, '..', 'data', self.file)

        try:
            with open(portfolio_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError as e:
            raise click.BadParameter(f"Portfolio file '{portfolio_path}' not found.") from e
        except Exception as e:
            raise click.BadParameter(f"Error loading portfolio file: {e}") from e
