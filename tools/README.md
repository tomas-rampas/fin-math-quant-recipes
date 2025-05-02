# Tools Directory

This directory contains utility scripts for the FinMath project.

## Test Notebook Generator

`generate_test_notebook.py` is a utility script that creates a test Jupyter notebook to verify the proper setup of the development environment. This is particularly useful for testing the GitHub workflow and DevContainer configuration.

### Usage

Run the script to generate a test notebook:

```bash
# From the project root
python tools/generate_test_notebook.py
```

This will create a test notebook at `tests/environment_test.ipynb` that:

1. Imports all required packages
2. Downloads some sample S&P 500 ETF (SPY) data using yfinance
3. Creates a simple price chart using matplotlib
4. Calculates technical indicators using TA-Lib

### Requirements

The script requires the `nbformat` package which can be installed via:

```bash
pip install nbformat
```

Note that this package is already included in the development container.

### Integration with Workflow Testing

This generator can be used before running the GitHub actions workflow to ensure all notebooks execute correctly in the test environment. It's particularly helpful for:

- Verifying that all required packages are installed and working properly
- Testing data access functionality
- Checking that visualization components work in the headless environment
- Validating that any custom functions or modules are properly accessible
