# API Request Examples for EMA Backtester

## 1. Using Default Periods (Recommended for first test)
```bash
curl -X POST "http://localhost:8000/ema-backtests/run" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "QQQ",
    "start_date": "2020-01-01",
    "end_date": "2023-01-01",
    "initial_cash": 10000
  }'
```

## 2. Using Custom Small Set of Periods (For Testing)
```bash
curl -X POST "http://localhost:8000/ema-backtests/run" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "QQQ",
    "start_date": "2020-01-01",
    "end_date": "2023-01-01",
    "initial_cash": 10000,
    "short_periods": [5, 10, 15],
    "long_periods": [20, 25, 30]
  }'
```

## 3. Using Larger Set of Valid Periods
```bash
curl -X POST "http://localhost:8000/ema-backtests/run" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "QQQ",
    "start_date": "2020-01-01",
    "end_date": "2023-01-01",
    "initial_cash": 10000,
    "short_periods": [5, 10, 15, 20, 25, 30],
    "long_periods": [35, 40, 45, 50, 55, 60]
  }'
```

## Valid Period Requirements:
- Must be positive integers
- Must be multiples of 5 (5, 10, 15, 20, 25, 30, etc.)
- Short periods: maximum 60
- Long periods: maximum 120
- Short period must be less than long period

## Invalid Examples (Will Cause Errors):
```json
{
  "short_periods": [0],        // ❌ 0 is not valid
  "long_periods": [0]          // ❌ 0 is not valid
}

{
  "short_periods": [7, 13],    // ❌ Not multiples of 5
  "long_periods": [22, 33]     // ❌ Not multiples of 5
}

{
  "short_periods": [65],       // ❌ Exceeds maximum 60
  "long_periods": [125]        // ❌ Exceeds maximum 120
}

{
  "short_periods": [25],       // ❌ Short >= Long (invalid)
  "long_periods": [20]         // ❌ Short >= Long (invalid)
}
```

## For the Swagger UI:
Replace the request body with:
```json
{
  "short_periods": [5, 10, 15],
  "long_periods": [20, 25, 30]
}
```
