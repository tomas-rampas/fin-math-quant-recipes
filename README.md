# Financial Mathematics in Algorithmic Trading

[![DevContainer & Jupyter Notebook Tests](https://github.com/tomas-rampas/fin-math-quant-recipes/actions/workflows/notebook-tests.yml/badge.svg)](https://github.com/tomas-rampas/fin-math-quant-recipes/actions/workflows/notebook-tests.yml) [![Made with Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=flat&logo=Jupyter)](https://jupyter.org/try) [![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Financial mathematics is the application of mathematical methods to financial markets and investment decision-making. It combines mathematical models, statistical analysis, and computational techniques to understand market behavior, price financial instruments, and optimize investment strategies.

In algorithmic trading specifically, financial mathematics provides the theoretical foundation and practical tools that drive automated trading systems. Here's how it's applied:

## Core Areas of Financial Mathematics in Algo Trading

Mathematical modeling forms the backbone of algorithmic trading. It involves creating mathematical representations of financial markets and instruments to make predictions about future price movements and identify trading opportunities.

### Pricing Models
- Option pricing models (Black-Scholes, binomial trees)
- Bond pricing and yield curve modeling
- Derivatives valuation techniques

### Statistical Analysis
- Time series analysis of price data
- Regression models
- Volatility modeling (GARCH, stochastic volatility)

### Stochastic Processes
- Random walks and Brownian motion
- Markov processes
- Jump diffusion models

### Optimization Techniques
- Portfolio optimization (Markowitz model)
- Trade execution optimization
- Risk-return optimization algorithms

## Practical Applications in Algorithmic Trading

### Signal Generation
Financial mathematics helps develop quantitative indicators that trigger buy/sell decisions based on statistical patterns and price movements.

### Risk Management
Mathematical models quantify various risks (market, credit, liquidity) and help set position sizes and stop-loss levels for algorithmic strategies.

### Execution Algorithms
Mathematical optimization helps minimize market impact and transaction costs when executing large orders.

### High-Frequency Trading
Advanced mathematical models analyze tiny price inefficiencies that can be exploited at millisecond timeframes.

### Machine Learning Integration
Financial mathematics provides the foundation for applying machine learning techniques to market prediction and pattern recognition.

Financial mathematics enables traders to move beyond intuition to data-driven, systematic approaches that can be backtested and continuously improved based on quantitative metrics.

## Development Environment

This project includes a development container configuration that provides a consistent and reproducible environment for financial mathematics and algorithmic trading research.

### Running the Dev Container on GitHub Codespaces

1. **Open in Codespaces**:
   - Navigate to the GitHub repository
   - Click on the "Code" button
   - Select the "Codespaces" tab
   - Click "Create codespace on main"

2. **Wait for Environment Setup**:
   - GitHub will automatically detect the .devcontainer configuration
   - The container will be built with all required dependencies
   - This process takes a few minutes for the first setup

3. **Verification**:
   - Once loaded, open a terminal in Codespaces
   - Run `conda env list` to confirm the finmath environment is active
   - Run `python -c "import talib, yfinance; print(f'TA-Lib: {talib.__ta_version__}, YFinance: {yfinance.__version__}')"` to verify key packages

4. **Jupyter Notebooks**:
   - Open any notebook from the 'jupiters' directory
   - Select the 'finmath' kernel when prompted
   - All dependencies should be available for import and use

5. **Development**:
   - Make changes to code and notebooks directly in the browser
   - All changes are automatically saved to your GitHub codespace
   - Commit and push changes directly from the Codespaces interface

### Running the Dev Container Locally with VSCode and Docker Desktop

#### Prerequisites

1. **Install Docker Desktop**:
   - Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Ensure Docker is running on your system

2. **Install VSCode**:
   - Download and install [Visual Studio Code](https://code.visualstudio.com/)
   
3. **Install Required VSCode Extensions**:
   - Open VSCode
   - Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

#### Setup and Run

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Open in VSCode**:
   - Open VSCode
   - Go to File > Open Folder and select the cloned repository folder
   - VSCode will detect the .devcontainer configuration
   - You should see a notification in the bottom right corner asking if you want to reopen the folder in a container
   - Click "Reopen in Container"
   - Alternatively, you can press F1, type "Remote-Containers: Reopen in Container" and press Enter

3. **Wait for Container Build**:
   - VSCode will build the container according to the Dockerfile and devcontainer.json
   - This process may take several minutes for the initial build
   - The status is shown in the bottom right corner of VSCode

4. **Verification**:
   - Once the container is built and running, open a new terminal in VSCode (Terminal > New Terminal)
   - Run `conda env list` to confirm the finmath environment is active
   - Run `python -c "import talib, yfinance; print(f'TA-Lib: {talib.__ta_version__}, YFinance: {yfinance.__version__}')"` to verify key packages

5. **Working with Jupyter Notebooks**:
   - Open any notebook from the 'jupiters' directory
   - VSCode will automatically use the finmath environment
   - If prompted, select the 'finmath' kernel
   - All dependencies should be available for import and use

6. **Development Workflow**:
   - All files in the repository are mounted into the container
   - Changes you make are automatically saved to your local filesystem
   - You can use git commands in the terminal within the container
   - All VSCode extensions specified in devcontainer.json are automatically installed

7. **Stopping the Container**:
   - When you're done working, you can close VSCode
   - The container will be stopped automatically
   - You can also manually stop the container from Docker Desktop

### GitHub Container Registry Authentication (Optional)

This repository uses GitHub Container Registry (GHCR) to cache container images for faster builds:

1. **How It Works**:
   - In GitHub Codespaces: Authentication happens automatically
   - In GitHub Actions: The workflow authenticates with GHCR using repository secrets
   - For local development: You can provide a GitHub token

2. **Setting Up Local Authentication** (for faster builds):
   - Generate a GitHub Personal Access Token with `read:packages` permission
   - Set it as an environment variable in VS Code settings or a local `.env` file
   - See detailed instructions in [.devcontainer/README.md](.devcontainer/README.md)

3. **Fallback Behavior**:
   - If no token is available, the container will still build successfully
   - It just won't use cached layers, so the first build may take longer
   - Subsequent builds within the same session will be faster due to local Docker caching

This setup ensures everyone working on the project has identical dependencies and configuration, eliminating "works on my machine" issues, whether working locally or in the cloud.
