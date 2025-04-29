#! /usr/bin/env python3

"""Main module of the application, contains the starting point."""


import click
from cli.commands import (
    register_margin_calculator_command,
    register_get_products_command,
    register_get_series_command,
    register_get_live_snapshots_command,
    register_get_snapshots_command,
    register_etd_portfolio_command,
)


@click.group()
@click.version_option(version="1.0")
def cli():
    """Main CLI group for margin estimator tool."""
    pass


register_margin_calculator_command(cli)
register_get_products_command(cli)
register_get_series_command(cli)
register_get_live_snapshots_command(cli)
register_get_snapshots_command(cli)
register_etd_portfolio_command(cli)


if __name__ == "__main__":
    cli()
