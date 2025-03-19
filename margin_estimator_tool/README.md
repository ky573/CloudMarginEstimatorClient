# CLI Margin Estimator Tool

## Overview
The CLI Tool is a command-line interface designed to interact with CPME API for handling various requests like retrieving product data, series information, snapshots, live snapshots, ETD portfolio data, and margin calculations. The tool is structured into a CLI interface and a backend component that processes requests and handles data filtering, validation, and export operations.

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
- Python 3.8+
- `pip` (Python package manager)

### Setup
Clone the repository and install the required dependencies:
```sh
# Clone the repository
git clone https://github.deutsche-boerse.de/dev/DAVe-MarginEstimator-PythonAPIClient.git
cd DAVe-MarginEstimator-PythonAPIClient/margin_estimator_tool

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install .
```

### Environment Configuration
Create a `.env` file in the project root directory and define the required environment variables:
```ini
API_KEY=/api key/
PROXY=/proxy/
```

Also ensure that Python path is set up correctly
```shell
export PYTHONPATH=<local_folder>/DAVe-MarginEstimator-PythonAPIClient
```

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
margin_estimator_tool get_series --date 20250303 --version SOD --to_json
```

## Architecture
The tool is structured into two main components:
### CLI
- **Commands**: Handles user inputs and requests.
- **Command Factory**: Dynamically generates commands.
- **Argument Validator**: Ensures proper user input.

### Backend
- **Request Handlers**: Processes requests for various endpoints.
- **Filter Handler**: Used by Products and Series request handlers.
- **Data Exporter**: Used by multiple handlers to export data.
- **Header Validator**: Ensures validity of headers for estimator endpoints.
- **Request Body Builder**: Constructs request bodies for estimator endpoints.
- **Export Strategies**: Handles exporting data in different formats.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
