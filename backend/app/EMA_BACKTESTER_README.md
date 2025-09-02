# Enhanced EMA Backtester

This document explains the enhanced EMA Backtester class that can backtest EMA crossover strategies for a given symbol with different short and long EMA combinations.

## Features

1. **Automated EMA Combination Testing**: Tests multiple EMA crossover combinations automatically
2. **Strict Parameter Validation**: Ensures EMAs are multiples of 5 with proper limits
3. **Comprehensive Database Storage**: Stores all results with detailed metrics
4. **Performance Analysis**: Provides best combination finding and summary statistics
5. **Error Handling**: Robust error handling and validation

## Requirements

- Short EMA periods: Multiples of 5, maximum 60
- Long EMA periods: Multiples of 5, maximum 120  
- Short period must be less than long period

## Database Schema

The results are stored in the `ema_backtests` table with the following fields:

```sql
CREATE TABLE ema_backtests (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    short_period INTEGER NOT NULL,
    long_period INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    initial_cash DECIMAL(15,2) NOT NULL,
    final_cash DECIMAL(15,2) NOT NULL,
    total_return DECIMAL(15,4) NOT NULL,
    total_return_percent DECIMAL(15,4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Example record:
```json
{
  "symbol": "QQQ",
  "short_period": 20,
  "long_period": 50,
  "start_date": "2010-01-01",
  "end_date": "2025-08-15",
  "initial_cash": 10000.00,
  "final_cash": 43356.38,
  "total_return": 3.3356,
  "total_return_percent": 333.56
}
```

## Usage

### 1. Basic Usage

```python
from datetime import date
from app.ema_backtester import EMABacktester
from app.database import SessionLocal

# Initialize
backtester = EMABacktester(
    symbol="QQQ",
    start_date=date(2010, 1, 1),
    end_date=date(2025, 8, 15),
    initial_cash=10000
)

# Run all default combinations
db = SessionLocal()
results = backtester.run_combinations(db)
print(f"Completed {len(results)} backtests")
```

### 2. Custom EMA Periods

```python
# Define custom periods (must be multiples of 5)
short_periods = [5, 10, 15, 20, 25]  # Max 60
long_periods = [30, 35, 40, 45, 50]  # Max 120

results = backtester.run_combinations(db, short_periods, long_periods)
```

### 3. Find Best Combination

```python
# Find best by different metrics
best_return = backtester.get_best_combination(db, metric="total_return_percent")
best_cash = backtester.get_best_combination(db, metric="final_cash")

print(f"Best return: EMA {best_return.short_period}/{best_return.long_period}")
print(f"Return: {best_return.total_return_percent:.2f}%")
```

### 4. Get Summary Statistics

```python
summary = backtester.get_combination_summary(db)
print(f"Total combinations: {summary['total_combinations']}")
print(f"Average return: {summary['average_return_percent']:.2f}%")
print(f"Profitable combinations: {summary['profitable_combinations']}")
```

## API Endpoints

### Run EMA Backtests
```http
POST /ema-backtests/run
Content-Type: application/json

{
  "symbol": "QQQ",
  "start_date": "2010-01-01",
  "end_date": "2025-08-15",
  "initial_cash": 10000,
  "short_periods": [5, 10, 15, 20],
  "long_periods": [25, 30, 35, 40]
}
```

### Get Best Combination
```http
GET /ema-backtests/best?symbol=QQQ&start_date=2010-01-01&end_date=2025-08-15&metric=total_return_percent
```

### Get Summary Statistics
```http
GET /ema-backtests/summary?symbol=QQQ&start_date=2010-01-01&end_date=2025-08-15
```

## Class Methods

### `__init__(symbol, start_date, end_date, initial_cash=10000)`
Initialize the backtester with symbol and date range.

### `generate_ema_combinations(short_periods=None, long_periods=None)`
Generate all valid EMA period combinations with validation.

### `run_single_combination(db, short_period, long_period)`
Run backtest for a single EMA combination.

### `run_combinations(db, short_periods=None, long_periods=None)`
Run backtests for multiple EMA combinations.

### `get_best_combination(db, metric="total_return_percent")`
Get the best performing combination by specified metric.

### `get_combination_summary(db)`
Get summary statistics for all tested combinations.

## Validation Rules

1. **Period Multiples**: All periods must be multiples of 5
2. **Period Limits**: Short ≤ 60, Long ≤ 120
3. **Period Relationship**: Short < Long
4. **Positive Values**: Initial cash and periods must be positive
5. **Date Range**: Start date must be before end date

## Error Handling

The class includes comprehensive error handling:
- Invalid periods are filtered out with warnings
- Database errors are rolled back
- Missing data is handled gracefully
- Detailed error messages for debugging

## Example Output

```
Running 12 EMA combinations for QQQ from 2010-01-01 to 2025-08-15
Processing combination 1/12: EMA 5/25
Processing combination 2/12: EMA 5/30
...
Completed 12/12 backtests successfully

Best combination: EMA 15/40
  Initial Cash: $10,000.00
  Final Cash: $43,356.38
  Total Return: 3.3356
  Return Percentage: 333.56%

Summary Statistics:
  Total combinations: 12
  Best return: 345.67%
  Worst return: 156.23%
  Average return: 267.45%
  Profitable combinations: 11
```

## Integration with Existing System

The enhanced EMA backtester integrates seamlessly with your existing:
- FastAPI application
- SQLAlchemy database models
- BacktestEngine framework
- EMACrossoverStrategy implementation

No breaking changes to existing functionality.
