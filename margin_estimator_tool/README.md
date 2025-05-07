# CLI Margin Estimator Tool

## Overview
The CLI Tool is a command-line interface designed to interact with CPME API for handling various requests like retrieving product data, series information, snapshots, live snapshots, ETD portfolio data, and margin calculations. The tool is structured into a CLI interface and an application layer component that processes requests and handles data filtering, validation, and export operations.

## Features
- Command-line interface for interacting with backend endpoints.
- Modular command factory for dynamically handling commands.
- Argument validation to ensure correctness of user inputs.
- Request handlers for different endpoints: Products, Series, Snapshots, Live Snapshots, ETD Portfolio, and Margin Calculator.
- Data filtering and exporting capabilities.
- Header validation and request body construction for specific endpoints.
- Supports multiple export formats: CSV, JSON, and Excel.

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.10+
- `pip` (Python package manager)

### Setup
1. **Clone the repository:**
    ```bash
    git clone https://github.com/ky573/CloudMarginEstimatorClient.git
    cd CloudMarginEstimatorClient
    ```

2. **Checkout to the branch:**
    ```bash
    git switch gk101_estimator_demo_tool_update
    ```

3. **Navigate to the tool directory:**
    ```bash
    cd margin_estimator_tool
    ```

4. **Create a virtual environment**  
   (see [Python venv documentation](https://docs.python.org/3/library/venv.html)):
    ```bash
    python -m venv venv
    ```

5. **Activate the virtual environment:**
    - On **Windows**:
        ```bash
        venv\Scripts\activate
        ```
    - On **macOS/Linux**:
        ```bash
        source venv/bin/activate
        ```

6. **Install dependencies:**
    - For basic usage:
        ```bash
        pip install .
        ```
    - For development (includes tools for testing and linting):
        ```bash
        pip install .[dev]
        ```

7. **Install the `cpme_api` client:**
    ```bash
    cd ..  # Go to the root project directory
    pip install .
    ```

8. **We can check the successful installation of the package by running:**
    ```bash
    margin_estimator_tool --version
    ```
   
### Environment Configuration
Create a `.env` file in the `margin_estimator_tool` directory and define the required environment variables:
```ini
API_KEY=/api key/
PROXY=/proxy/
```

This is an example of a `.env` file:

```ini
API_KEY="1234abcd-12ab-12ab-12ab-abcdef123456"
PROXY="http://proxy.company.cloud.eu:1234"
```

Without the proxy, it can look like this:

```ini
API_KEY="1234abcd-12ab-12ab-12ab-abcdef123456"
```

The API key is free and can be obtained from [DBG Digital Business Platform](https://console.developer.deutsche-boerse.com/) after signing into the company's Digital Platform. 
For our purposes, we want to choose [Prisma Margin Estimator API key](https://console.developer.deutsche-boerse.com/apis/416d7067-45dc-465b-a56a-abbabdd1467d). 
To obtain the key, we can follow the instructions on the website. It may take a few minutes for the key to be recognized.

The proxy address for requests might not be needed, as it is usually used only to bypass network restrictions in some company networks. 
Users can try the setup without the proxy first, and only in a situation when they get a time-out from a request, they can set the proxy. 

## Usage
Run the CLI tool with the desired command:
```sh
margin_estimator_tool --help
```
This will display all available commands and their usage.

### Example Commands
#### Fetch products data:
```sh
margin_estimator_tool get_products --version LIVE
```
#### Fetch series data and export to JSON:
```sh
margin_estimator_tool get_series --date 20250303 --version EOD --to_json
```

Detailed usage for each command together with tutorials can be found in directory `margin_estimator_tool/tutorials/`.

## Testing

To run the tests, ensure you have the development dependencies installed (see the installation section). 
Then, run the following command from the `margin_estimator_tool` directory:
```bash
pytest test/
```

This will execute all tests in the `test` directory.

## Documentation

The documentation for the CLI tool is available in the `margin_estimator_tool/docs` directory.
It was generated using [Sphinx](https://www.sphinx-doc.org/en/master/) from the docstrings from the codebase.
To generate html version, navigate to `docs` directory and use:

```bash
make html
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project structure

The project is structured as follows:

```chatinput
src/
├── cli/                         # Handles CLI parsing and execution
│   ├── argument_validator.py     # Validates CLI arguments
│   ├── commands.py               # Defines available CLI commands
│   ├── endpoint_handler_factory.py # Factory for request handlers
│
├── core/                        # Core functionality shared across components
│   ├── data_exporter.py          # Handles export of data
│   ├── filter_handler.py         # Manages filtering logic for specific endpoints
│   ├── request_handler_base.py   # Base class for handlers
│   ├── utils.py                  # Utility functions for common operations
│
├── export_strategy/              # Implements Strategy Pattern for data export
│   ├── csv_export_strategy.py    # Handles CSV export for general data
│   ├── etd_portfolio_csv_export_strategy.py      # Exports ETD portfolio data as CSV
│   ├── etd_portfolio_excel_export_strategy.py    # Exports ETD portfolio to Excel
│   ├── excel_export_strategy.py  # Handles Excel export for general data
│   ├── export_context.py         # Context class for strategy selection
│   ├── export_strategy.py        # Base class defining export strategy interface
│   ├── json_export_strategy.py   # Handles JSON export for general data
│   ├── margin_calculator_excel_export_strategy.py # Exports margins to Excel
│
├── estimator/                    # Handles margin estimation-related logic
│   ├── etd_portfolio/            
│   │   ├── etd_portfolio_request_handler.py      # API requests for ETD portfolios
│   ├── margin_calculator/
│   │   ├── extractor.py           # Extracts necessary data for calculations
│   │   ├── graph_exporter.py      # Exports results as graphs
│   │   ├── margin_calculator_request_handler.py  # Margin calculations handler
│   ├── estimator_request_builder.py     # Constructs request body for estimator
│   ├── portfolio_header_validator.py    # Validates portfolio headers
│
├── live_snapshots/               # Handles live snapshot data retrieval
│   ├── live_snapshots_request_handler.py # Handler for live snapshots
│
├── products/                     # Handles product-related API requests
│   ├── products_request_handler.py       # Fetches product data from the API
│
├── series/                       # Handles series-related API requests
│   ├── series_request_handler.py        # Fetches series data from the API
│
├── snapshots/                    # Handles snapshot-related API requests
│   ├── snapshots_request_handler.py     # Fetches historical snapshot data
│
├── main.py                       # Main entry point for the CLI application

```
