# Backtest Logic Updates - Using Adjusted Prices

## Overview

All backtest logic has been updated to use the `adjusted_prices` table instead of the regular `prices` table. This provides more accurate backtesting results by accounting for stock splits, dividend distributions, and other corporate actions.

## Changes Made

### 1. **BacktestEngine Class** (`backend/app/backtest.py`)
- **Import**: Changed from `Price` to `AdjustedPrice` model
- **Query**: Now queries `adjusted_prices` table instead of `prices` table
- **Pricing**: 
  - Buy orders use `adj_open` instead of `open_price`
  - Sell orders use `adj_close` instead of `close`
- **Return Type**: `_get_prices()` now returns `List[AdjustedPrice]`

### 2. **Strategy Base Class** (`backend/app/strategies/__init__.py`)
- **Import**: Changed from `Price` to `AdjustedPrice` model
- **Method Signatures**: Both `should_buy()` and `should_sell()` now expect `List[AdjustedPrice]`

### 3. **EMACrossoverStrategy** (`backend/app/strategies/ema_crossover.py`)
- **Import**: Changed from `Price` to `AdjustedPrice` model
- **EMA Calculation**: Now uses `adj_close` instead of `close` for calculating EMAs
- **Method Signatures**: Updated to use `List[AdjustedPrice]`

### 4. **BuyAndHoldStrategy** (`backend/app/strategies/buy_and_hold.py`)
- **Import**: Changed from `Price` to `AdjustedPrice` model
- **Method Signatures**: Updated to use `List[AdjustedPrice]`

## Benefits of Using Adjusted Prices

### 1. **Accurate Returns**
- Eliminates artificial price jumps caused by stock splits
- Accounts for dividend distributions in return calculations
- Provides realistic backtesting results

### 2. **Corporate Action Handling**
- **Stock Splits**: Prices are adjusted to maintain continuity
- **Dividends**: Return calculations include dividend distributions
- **Spin-offs**: Price adjustments account for value distribution

### 3. **Example Impact**
```
Regular Price Data:
- Day 1: $100 (before 2:1 split)
- Day 2: $50 (after split) - appears as 50% loss

Adjusted Price Data:
- Day 1: $50 (adjusted for split)
- Day 2: $50 (actual price) - shows true 0% change
```

## API Endpoints (No Changes Required)

All existing backtest API endpoints continue to work without any changes:

### Run Standard Backtest
```bash
POST /backtests/run
{
  "symbol": "AAPL",
  "strategy_name": "ema_crossover",
  "start_date": "2019-01-02",
  "end_date": "2023-01-01",
  "initial_cash": 10000
}
```

### Run EMA Backtests
```bash
POST /ema-backtests/run
{
  "symbol": "AAPL",
  "start_date": "2019-01-02",
  "end_date": "2023-01-01",
  "initial_cash": 10000
}
```

## Data Requirements

### Before Running Backtests
Ensure adjusted price data is available by fetching it first:

```bash
POST /stocks/AAPL/fetch-adjusted-prices?start_date=2019-01-02
```

### Data Validation
- Backtests will return an error if no adjusted price data is found
- Make sure the date range for adjusted prices covers your backtest period
- Use the same or earlier start date when fetching adjusted prices

## Backward Compatibility

### Regular Price Endpoints
The original price endpoints remain unchanged for backward compatibility:
- `POST /prices/` - Create price records
- `GET /prices/` - Retrieve price records
- `POST /stocks/{symbol}/fetch-prices` - Fetch from Alpha Vantage

### Migration Path
1. **Immediate**: All new backtests automatically use adjusted prices
2. **Gradual**: Existing price data remains available for other use cases
3. **Future**: Consider migrating other analysis tools to use adjusted prices

## Database Schema

### New Table Usage
```sql
-- Backtests now query this table
SELECT * FROM adjusted_prices 
WHERE stock_id = ? 
  AND date >= ? 
  AND date <= ? 
ORDER BY date;
```

### Key Fields Used
- `adj_open`: For buy order pricing
- `adj_close`: For sell order pricing and EMA calculations
- `date`: For time series ordering
- `adj_volume`: Available for volume-based strategies (future use)

## Testing

### Verification Steps
1. Fetch adjusted price data for a symbol
2. Run a backtest with the same symbol and date range
3. Verify the backtest uses adjusted prices (no "No price data found" errors)
4. Compare results with previous backtests using regular prices

### Expected Differences
- **More Realistic Returns**: Especially for stocks with splits/dividends
- **Smoother Price Series**: No artificial jumps from corporate actions
- **Different Trade Timing**: EMA crossovers may occur at different points

## Migration Complete ✅

- ✅ BacktestEngine uses adjusted_prices table
- ✅ All strategies use AdjustedPrice model
- ✅ EMA calculations use adj_close prices
- ✅ Buy/sell orders use adj_open/adj_close
- ✅ Backward compatibility maintained
- ✅ API endpoints unchanged
