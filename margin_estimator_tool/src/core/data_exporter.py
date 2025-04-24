"""
Module to handle exporting of data to different formats. Strategies are defined in dictionary,
and can be easily modified or extended.
"""

from typing import Dict, Any, List
import click
from export_strategy.export_context import ExportContext
from export_strategy.export_strategy import ExportStrategy
from export_strategy.json_export_strategy import JSONExportStrategy
from export_strategy.csv_export_strategy import CSVExportStrategy
from export_strategy.excel_export_strategy import ExcelExportStrategy
from export_strategy.etd_portfolio_csv_export_strategy import (
    EtdPortfolioCSVExportStrategy,
)
from export_strategy.etd_portfolio_excel_export_strategy import (
    EtdPortfolioExcelExportStrategy,
)
from export_strategy.margin_calculator_excel_export_strategy import (
    MarginCalculatorExcelExportStrategy,
)


class DataExporter:
    """Class to handle exporting of data into various formats."""

    EXPORT_STRATEGIES: Dict[str, Dict[str, ExportStrategy]] = {
        "Products": {
            "csv": CSVExportStrategy("products"),
            "excel": ExcelExportStrategy("products"),
            "json": JSONExportStrategy("products"),
        },
        "Series": {
            "csv": CSVExportStrategy("series"),
            "excel": ExcelExportStrategy("series"),
            "json": JSONExportStrategy("series"),
        },
        "Template": {
            "csv": CSVExportStrategy("etd_portfolio_template"),
            "excel": ExcelExportStrategy("etd_portfolio_template"),
            "json": JSONExportStrategy("etd_portfolio_template"),
        },
        "Portfolio": {
            "csv": EtdPortfolioCSVExportStrategy("estimator"),
            "excel": EtdPortfolioExcelExportStrategy("estimator"),
            "json": JSONExportStrategy("estimator"),
        },
        "Margins": {
            "excel": MarginCalculatorExcelExportStrategy("margins"),
        },
    }

    @staticmethod
    def export(
        data: List[Dict[str, Any]] | Dict[str, Any],
        export_name: str,
        export_dir: str,
        to_excel: bool | None,
        to_json: bool | None,
        business_date: str,
        version: bool,
    ) -> None:
        """
        Exports data based on the requested format, using endpoint-specific strategies.

        Args:
            data: data from the request to be exported
            export_name: defines what kind of endpoint-specific strategies to pick from in EXPORT_STRATEGIES
            export_dir: directory where the data should be exported
            to_excel: whether to export to excel
            to_json: whether to export to json
            business_date: desired business date, to be used in file name
            version: desired version, to be used in file name
        """
        try:
            if to_json and to_excel:
                raise click.UsageError(
                    "Options --to_json and --to_excel are mutually exclusive. Please choose only one."
                )

            context = ExportContext()

            if export_name in DataExporter.EXPORT_STRATEGIES:
                strategies = DataExporter.EXPORT_STRATEGIES[export_name]

                if to_excel:
                    context.set_strategy(strategies["excel"])
                elif to_json:
                    context.set_strategy(strategies["json"])
                else:
                    context.set_strategy(strategies["csv"])

                if context.export_data(business_date, version, data, export_dir):
                    click.echo(f"{export_name} exported to {export_dir}")
                else:
                    click.echo("No data found.")
            else:
                raise ValueError(f"Unknown export name: {export_name}")
        except Exception as e:
            click.echo(f"Export failed: {e}")
