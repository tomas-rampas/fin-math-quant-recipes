#!/usr/bin/env python
"""
Test Notebook Generator

This script generates a simple test Jupyter notebook that imports
all required packages and runs basic operations to verify the environment.
"""

import os
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

def generate_test_notebook(output_path):
    """Generate a simple test notebook that imports and tests key packages."""
    
    # Create a new notebook
    nb = new_notebook()
    
    # Add markdown header
    nb.cells.append(new_markdown_cell("""# Environment Test Notebook
    
This notebook tests if the key packages required for financial math in algorithmic trading are properly installed and functioning.
"""))
    
    # Test imports
    nb.cells.append(new_code_cell("""# Test basic imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import statsmodels.api as sm
import sklearn
import talib
import yfinance as yf
import pytz
import arch

print("All required packages successfully imported!")
"""))
    
    # Test yfinance
    nb.cells.append(new_code_cell("""# Test yfinance data fetching
spy = yf.download("SPY", period="5d")
print(f"Downloaded {len(spy)} rows of SPY data")
spy.head()
"""))
    
    # Test matplotlib and pandas
    nb.cells.append(new_code_cell("""# Test matplotlib visualization
plt.figure(figsize=(10, 5))
spy['Close'].plot()
plt.title('SPY Close Price (Last 5 days)')
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.grid(True)
plt.show()
"""))
    
    # Test TA-Lib
    nb.cells.append(new_code_cell("""# Test TA-Lib functions
spy['SMA_20'] = talib.SMA(spy['Close'], timeperiod=20)
spy['RSI'] = talib.RSI(spy['Close'], timeperiod=14)
spy[['Close', 'SMA_20', 'RSI']].tail()
"""))
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the notebook
    with open(output_path, 'w') as f:
        nbf.write(nb, f)
    
    print(f"Test notebook created at: {output_path}")

if __name__ == "__main__":
    # Create test notebook in a tests directory
    os.makedirs("tests", exist_ok=True)
    generate_test_notebook("tests/environment_test.ipynb")
