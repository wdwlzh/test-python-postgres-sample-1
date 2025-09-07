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
    "short_periods": [3, 5, 8],
    "long_periods": [15, 20, 25]
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
    "short_periods": [3, 5, 8, 12, 15, 18, 20],
    "long_periods": [25, 30, 35, 40, 45, 50, 55, 60]
  }'
```

## Valid Period Requirements:
- Must be positive integers
- Short periods: 3 to 20
- Long periods: 10 to 60
- Short period must be less than long period

## Invalid Examples (Will Cause Errors):
```json
{
  "short_periods": [0],        // ❌ 0 is not valid
  "long_periods": [0]          // ❌ 0 is not valid
}

{
  "short_periods": [1, 2],     // ❌ Below minimum (3)
  "long_periods": [8, 9]       // ❌ Below minimum (10)
}

{
  "short_periods": [25],       // ❌ Exceeds maximum (20)
  "long_periods": [65]         // ❌ Exceeds maximum (60)
}

{
  "short_periods": [15],       // ❌ Short >= Long (invalid)
  "long_periods": [12]         // ❌ Short >= Long (invalid)
}
```

## For the Swagger UI:
Replace the request body with:
```json
{
  "short_periods": [3, 5, 8],
  "long_periods": [15, 20, 25]
}
```
