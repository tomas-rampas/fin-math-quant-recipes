# Financial Mathematics Examples for S&P 500 Algorithmic Trading

## 1. Time Series Analysis Models

### ARIMA Model for S&P 500 Index Forecasting
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

# Get S&P 500 historical data
sp500 = pdr.get_data_yahoo('^GSPC', start='2020-01-01')
returns = sp500['Close'].pct_change().dropna()

# Fit ARIMA model
model = ARIMA(returns, order=(5,1,2))
model_fit = model.fit()

# Forecast next 10 days
forecast = model_fit.forecast(steps=10)
print("Forecasted returns for next 10 trading days:")
print(forecast)
```

### Exponential Smoothing for Volatility Estimation
```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Calculate rolling volatility (20-day)
sp500['volatility'] = sp500['Close'].pct_change().rolling(window=20).std() * np.sqrt(252)

# Apply exponential smoothing to volatility
model = ExponentialSmoothing(sp500['volatility'].dropna(), trend='add', seasonal=None)
fit = model.fit()

# Forecast future volatility
volatility_forecast = fit.forecast(5)
print("Volatility forecast for next 5 trading days:")
print(volatility_forecast)
```

## 2. Statistical Arbitrage with Pairs Trading

### Cointegration Testing for S&P 500 Components
```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
import yfinance as yf

# Get data for two stocks (e.g., Microsoft and Apple)
msft = yf.download('MSFT', start='2022-01-01')['Close']
aapl = yf.download('AAPL', start='2022-01-01')['Close']

# Test for cointegration
score, pvalue, _ = coint(msft, aapl)
print(f"Cointegration p-value: {pvalue:.4f}")

if pvalue < 0.05:
    print("Stocks are cointegrated at 5% significance level")
    
    # Calculate spread
    spread = msft - 1.2 * aapl  # The 1.2 coefficient would be determined by regression
    spread_mean = spread.mean()
    spread_std = spread.std()
    
    # Define trading signals
    z_score = (spread - spread_mean) / spread_std
    buy_signal = z_score < -2.0
    sell_signal = z_score > 2.0
    
    print(f"Number of buy signals: {sum(buy_signal)}")
    print(f"Number of sell signals: {sum(sell_signal)}")
```

## 3. Risk-Return Optimization for S&P 500 Sector Allocation

### Markowitz Portfolio Optimization
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize

# Get data for S&P 500 sector ETFs
sectors = ['XLF', 'XLK', 'XLV', 'XLY', 'XLP', 'XLI', 'XLU', 'XLB', 'XLE', 'XLRE', 'XLC']
data = yf.download(sectors, start='2022-01-01')['Adj Close']
returns = data.pct_change().dropna()

# Calculate mean returns and covariance matrix
mean_returns = returns.mean() * 252  # Annualized
cov_matrix = returns.cov() * 252  # Annualized

# Function to calculate portfolio performance
def portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights)
    std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return std, returns

# Function to minimize (negative Sharpe Ratio)
def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.02):
    std, ret = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(ret - risk_free_rate) / std

# Constraints and bounds
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, 1) for i in range(len(sectors)))
initial_guess = [1/len(sectors)] * len(sectors)

# Optimize portfolio
optimal_weights = minimize(neg_sharpe_ratio, initial_guess, 
                          args=(mean_returns, cov_matrix),
                          method='SLSQP', bounds=bounds, constraints=constraints)

# Display optimal weights
optimal_allocation = pd.DataFrame(optimal_weights['x'], index=sectors, columns=['Weight'])
optimal_allocation['Weight'] = optimal_allocation['Weight'].apply(lambda x: f"{x*100:.2f}%")
print("Optimal Sector Allocation:")
print(optimal_allocation)
```

## 4. Options Pricing for S&P 500 Index Options (SPX)

### Black-Scholes Model Implementation
```python
import numpy as np
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate Black-Scholes price for a call option
    
    Parameters:
    S: Current stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free interest rate
    sigma: Volatility
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def black_scholes_put(S, K, T, r, sigma):
    """Calculate Black-Scholes price for a put option"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

# Example for S&P 500 index options
S = 4800  # Current S&P 500 level
K = 4850  # Strike price
T = 30/365  # 30 days to expiration 
r = 0.05  # 5% risk-free rate
sigma = 0.18  # 18% volatility

call_price = black_scholes_call(S, K, T, r, sigma)
put_price = black_scholes_put(S, K, T, r, sigma)

print(f"SPX Call Option Price: ${call_price:.2f}")
print(f"SPX Put Option Price: ${put_price:.2f}")

# Greeks calculation (for risk management)
def call_delta(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

def call_gamma(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))

print(f"Delta: {call_delta(S, K, T, r, sigma):.4f}")
print(f"Gamma: {call_gamma(S, K, T, r, sigma):.4f}")
```

## 5. Volatility Models for S&P 500 Risk Management

### GARCH Model for Volatility Forecasting
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch import arch_model
import yfinance as yf

# Get S&P 500 data
sp500 = yf.download('^GSPC', auto_adjust=False, start='2020-01-01')
returns = 100 * sp500['Close'].pct_change().dropna()

# Fit GARCH(1,1) model
model = arch_model(returns, vol='GARCH', p=1, q=1)
model_fit = model.fit(disp='off')

# Forecast volatility
forecasts = model_fit.forecast(horizon=10)
forecast_vol = np.sqrt(forecasts.variance.iloc[-1])

print("GARCH(1,1) parameters:")
print(model_fit.summary().tables[1])

print("\nForecasted volatility for next 10 days:")
print(forecast_vol)

# Plot volatility forecast
plt.figure(figsize=(12, 6))
plt.plot(forecast_vol)
plt.title('GARCH(1,1) Volatility Forecast for S&P 500')
plt.xlabel('Days ahead')
plt.ylabel('Volatility')
```

## 6. Mean Reversion Strategy for S&P 500 Trading

### RSI-Based Mean Reversion Algorithm
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Get S&P 500 data
sp500 = yf.download('^GSPC', auto_adjust=False, start='2020-01-01')

# Calculate RSI
def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100./(1. + rs)
    
    for i in range(period, len(prices)):
        delta = deltas[i-1]
        if delta > 0:
            upval = delta
            downval = 0
        else:
            upval = 0
            downval = -delta
            
        up = (up * (period-1) + upval) / period
        down = (down * (period-1) + downval) / period
        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)
    
    return rsi

sp500['RSI'] = calculate_rsi(sp500['Close'].values)

# Generate trading signals
sp500['Signal'] = 0
sp500.loc[sp500['RSI'] < 30, 'Signal'] = 1  # Oversold - Buy signal
sp500.loc[sp500['RSI'] > 70, 'Signal'] = -1 # Overbought - Sell signal

# Calculate strategy returns
sp500['Position'] = sp500['Signal'].shift(1)
sp500['Returns'] = sp500['Close'].pct_change()
sp500['Strategy'] = sp500['Position'] * sp500['Returns']

# Evaluate strategy
cumulative_returns = (1 + sp500['Returns']).cumprod()
cumulative_strategy = (1 + sp500['Strategy']).cumprod()

print(f"Total Buy Signals: {len(sp500[sp500['Signal'] == 1])}")
print(f"Total Sell Signals: {len(sp500[sp500['Signal'] == -1])}")
print(f"Buy & Hold Return: {(cumulative_returns.iloc[-1] - 1) * 100:.2f}%")
print(f"Strategy Return: {(cumulative_strategy.iloc[-1] - 1) * 100:.2f}%")
print(f"Sharpe Ratio: {(sp500['Strategy'].mean() / sp500['Strategy'].std()) * np.sqrt(252):.2f}")
```

## 7. Machine Learning for S&P 500 Prediction

### Random Forest Model for S&P 500 Direction Prediction
```python
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

# Get S&P 500 data
sp500 = yf.download('^GSPC', auto_adjust=False, start='2018-01-01')

# Feature engineering
sp500['Returns'] = sp500['Close'].pct_change()
sp500['Direction'] = np.where(sp500['Returns'] > 0, 1, 0)

# Create lagged features
for i in range(1, 6):
    sp500[f'Returns_lag_{i}'] = sp500['Returns'].shift(i)
    sp500[f'Volume_lag_{i}'] = sp500['Volume'].shift(i)

# Add technical indicators
sp500['MA_5'] = sp500['Close'].rolling(window=5).mean()
sp500['MA_20'] = sp500['Close'].rolling(window=20).mean()
sp500['MA_Ratio'] = sp500['MA_5'] / sp500['MA_20']
sp500['Volatility'] = sp500['Returns'].rolling(window=20).std()

# Prepare data for model
sp500 = sp500.dropna()
features = [col for col in sp500.columns if 'lag' in col or 'MA' in col or col == 'Volatility']
X = sp500[features]
y = sp500['Direction']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance.head(10))
```

## 8. Factor Analysis for S&P 500 Stock Selection

### Multi-factor Model for Stock Ranking
```python
import pandas as pd
import numpy as np
import yfinance as yf

# Get data for all S&P 500 stocks (using a smaller subset for example)
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'TSLA', 'NVDA', 'BRK-B', 'UNH', 'JNJ']
data = yf.download(tickers, start='2022-01-01')

# Calculate factors
results = pd.DataFrame(index=tickers)

# Momentum factor (3-month return)
results['Momentum'] = ((data['Adj Close'].iloc[-1] / data['Adj Close'].iloc[-63]) - 1).values

# Value factor (P/E ratio - lower is better)
pe_ratios = []
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        pe = stock.info.get('trailingPE', np.nan)
        pe_ratios.append(pe)
    except:
        pe_ratios.append(np.nan)
results['PE'] = pe_ratios

# Volatility factor (20-day annualized)
returns = data['Adj Close'].pct_change().dropna()
results['Volatility'] = returns.std() * np.sqrt(252)

# Quality factor (ROE - higher is better)
roe = []
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        return_on_equity = stock.info.get('returnOnEquity', np.nan)
        roe.append(return_on_equity)
    except:
        roe.append(np.nan)
results['ROE'] = roe

# Normalize factors
for factor in ['Momentum', 'PE', 'Volatility', 'ROE']:
    if factor in ['PE', 'Volatility']:  # Lower is better
        results[f'{factor}_Z'] = -(results[factor] - results[factor].mean()) / results[factor].std()
    else:  # Higher is better
        results[f'{factor}_Z'] = (results[factor] - results[factor].mean()) / results[factor].std()

# Create composite score
factor_cols = ['Momentum_Z', 'PE_Z', 'Volatility_Z', 'ROE_Z']
results['Composite'] = results[factor_cols].mean(axis=1)

# Rank stocks
final_ranking = results.sort_values('Composite', ascending=False)
print("Stock Ranking based on Multi-Factor Model:")
print(final_ranking[['Momentum', 'PE', 'Volatility', 'ROE', 'Composite']])
```

## 9. Trading Execution Model for S&P 500 ETF (SPY)

### Volume-Weighted Average Price (VWAP) Algorithm
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Get intraday data for SPY (will need to use actual intraday data in practice)
# This simulates intraday data with a day of minute bars
def simulate_intraday_data(symbol='SPY', periods=390):  # 390 minutes in a trading day
    data = yf.download(symbol, period='1d', interval='1m')
    if len(data) < periods:
        # Create synthetic data if not enough real data
        last_price = yf.Ticker(symbol).history(period='1d')['Close'].iloc[-1]
        price_series = last_price * (1 + np.random.normal(0, 0.0002, periods))
        volume_series = np.random.poisson(10000, periods)
        
        index = pd.date_range(start=pd.Timestamp.now().floor('D') + pd.Timedelta(hours=9, minutes=30),
                             periods=periods, freq='min')
        
        data = pd.DataFrame({
            'Open': price_series,
            'High': price_series * (1 + np.random.uniform(0, 0.001, periods)),
            'Low': price_series * (1 - np.random.uniform(0, 0.001, periods)),
            'Close': price_series,
            'Volume': volume_series
        }, index=index)
    
    return data

intraday_data = simulate_intraday_data('SPY')

# Calculate VWAP
intraday_data['Typical_Price'] = (intraday_data['High'] + intraday_data['Low'] + intraday_data['Close']) / 3
intraday_data['VP'] = intraday_data['Typical_Price'] * intraday_data['Volume']
intraday_data['Cumulative_VP'] = intraday_data['VP'].cumsum()
intraday_data['Cumulative_Volume'] = intraday_data['Volume'].cumsum()
intraday_data['VWAP'] = intraday_data['Cumulative_VP'] / intraday_data['Cumulative_Volume']

# VWAP Execution Algorithm
total_shares_to_buy = 10000
participation_rate = 0.15  # Percentage of volume to trade
executed_shares = 0
total_cost = 0

execution_log = []

for index, row in intraday_data.iterrows():
    if executed_shares >= total_shares_to_buy:
        break
        
    # Determine how many shares to buy in this period
    period_volume = row['Volume']
    shares_to_buy = min(int(period_volume * participation_rate), total_shares_to_buy - executed_shares)
    
    if shares_to_buy > 0:
        # Execute at the typical price for simplicity
        execution_price = row['Typical_Price']
        period_cost = shares_to_buy * execution_price
        
        # Update totals
        executed_shares += shares_to_buy
        total_cost += period_cost
        
        # Log execution
        execution_log.append({
            'Time': index,
            'Shares': shares_to_buy,
            'Price': execution_price,
            'Cost': period_cost,
            'VWAP': row['VWAP'],
            'Executed%': executed_shares / total_shares_to_buy * 100
        })

# Create execution DataFrame
execution_df = pd.DataFrame(execution_log)
average_execution_price = total_cost / executed_shares if executed_shares > 0 else 0
market_vwap = intraday_data['VWAP'].iloc[-1]

print(f"Total Shares Executed: {executed_shares} of {total_shares_to_buy}")
print(f"Average Execution Price: ${average_execution_price:.2f}")
print(f"Market VWAP: ${market_vwap:.2f}")
print(f"VWAP Performance: {(market_vwap - average_execution_price) / market_vwap * 10000:.2f} bps")
```

## 10. Systematic Trading Strategy for S&P 500 Sectors

### Momentum-Based Sector Rotation Strategy
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Get data for S&P 500 sector ETFs
sectors = {
    'XLF': 'Financials',
    'XLK': 'Technology',
    'XLV': 'Healthcare',
    'XLY': 'Consumer Discretionary',
    'XLP': 'Consumer Staples',
    'XLI': 'Industrials',
    'XLU': 'Utilities',
    'XLB': 'Materials',
    'XLE': 'Energy',
    'XLRE': 'Real Estate',
    'XLC': 'Communication Services'
}

# Download price data
data = yf.download(list(sectors.keys()), start='2020-01-01')['Adj Close']

# Calculate momentum (trailing 6-month returns)
momentum_periods = 126  # ~6 months of trading days
momentum = data.pct_change(momentum_periods)

# Strategy parameters
top_n_sectors = 3
rebalance_freq = 21  # Monthly rebalancing (approximately)

# Run the backtest
portfolio_value = 100  # Starting with $100
portfolio_hist = [portfolio_value]
current_date = momentum.index[momentum_periods]
positions = pd.Series(0, index=sectors.keys())

while current_date < momentum.index[-1]:
    # Get the momentum at the current date
    current_momentum = momentum.loc[current_date]
    
    # Select top N sectors by momentum
    top_sectors = current_momentum.nlargest(top_n_sectors).index
    
    # Rebalance portfolio - equal weight to top sectors
    new_positions = pd.Series(0, index=sectors.keys())
    for sector in top_sectors:
        new_positions[sector] = 1 / top_n_sectors
    
    # Calculate returns for the holding period
    next_date_idx = min(momentum.index.get_loc(current_date) + rebalance_freq, len(momentum.index) - 1)
    next_date = momentum.index[next_date_idx]
    
    sector_returns = data.loc[next_date] / data.loc[current_date] - 1
    period_return = (sector_returns * new_positions).sum()
    
    # Update portfolio value
    portfolio_value *= (1 + period_return)
    portfolio_hist.append(portfolio_value)
    
    # Move to next rebalance date
    positions = new_positions
    current_date = next_date

# Calculate benchmark return (equal-weight all sectors)
benchmark_weights = pd.Series(1/len(sectors), index=sectors.keys())
benchmark_returns = data.pct_change().dropna()
benchmark_return_series = (benchmark_returns * benchmark_weights.values).sum(axis=1)
benchmark_value = 100 * (1 + benchmark_return_series).cumprod()

# Calculate strategy statistics
strategy_returns = pd.Series(np.diff(portfolio_hist) / portfolio_hist[:-1],
                             index=momentum.index[momentum_periods:momentum_periods+len(portfolio_hist)-1])

print("Sector Rotation Strategy Performance:")
print(f"Total Return: {portfolio_value - 100:.2f}%")
print(f"Annualized Return: {((portfolio_value/100) ** (252 / len(strategy_returns)) - 1) * 100:.2f}%")
print(f"Sharpe Ratio: {strategy_returns.mean() / strategy_returns.std() * np.sqrt(252):.2f}")
print(f"Max Drawdown: {(1 - pd.Series(portfolio_hist).div(pd.Series(portfolio_hist).cummax())).max() * 100:.2f}%")
```
