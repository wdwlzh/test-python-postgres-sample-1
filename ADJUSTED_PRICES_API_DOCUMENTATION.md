# Adjusted Prices API Documentation

## Overview

New API endpoints have been added to fetch and store adjusted historical price data from Tiingo API. This implementation includes all required fields from the Tiingo response and stores them in a new `adjusted_prices` table.

## Database Schema

### New Table: `adjusted_prices`

```sql
CREATE TABLE adjusted_prices (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER NOT NULL REFERENCES stocks(id),
    date DATE NOT NULL,
    close DECIMAL(10,4),
    high DECIMAL(10,4),
    low DECIMAL(10,4),
    open DECIMAL(10,4),
    volume BIGINT,
    adj_close DECIMAL(10,4),
    adj_high DECIMAL(10,4),
    adj_low DECIMAL(10,4),
    adj_open DECIMAL(10,4),
    adj_volume BIGINT,
    div_cash DECIMAL(10,4),
    split_factor DECIMAL(10,4)
);
```

## API Endpoints

### 1. Fetch and Store Adjusted Prices

**POST** `/stocks/{symbol}/fetch-adjusted-prices`

Fetches adjusted historical price data from Tiingo API and saves it to the database.

#### Query Parameters:
- `start_date` (optional): Start date for fetching historical data (YYYY-MM-DD format). If not provided, fetches all available data.

#### Request Examples:

**With start date:**
```bash
curl -X POST "http://localhost:8000/stocks/AAPL/fetch-adjusted-prices?start_date=2019-01-02" \
  -H "accept: application/json"
```

**Without start date (fetches all available data):**
```bash
curl -X POST "http://localhost:8000/stocks/AAPL/fetch-adjusted-prices" \
  -H "accept: application/json"
```

#### Python Request Examples:

**With start date:**
```python
import requests

response = requests.post(
    "http://localhost:8000/stocks/AAPL/fetch-adjusted-prices",
    params={"start_date": "2019-01-02"}
)
print(response.json())
```

**Without start date:**
```python
import requests

response = requests.post(
    "http://localhost:8000/stocks/AAPL/fetch-adjusted-prices"
)
print(response.json())
```

#### Response Examples:

**With start date:**
```json
{
    "message": "Fetched 1000 adjusted prices, inserted 500 new records for AAPL",
    "symbol": "AAPL",
    "start_date": "2019-01-02",
    "total_fetched": 1000,
    "total_inserted": 500
}
```

**Without start date:**
```json
{
    "message": "Fetched 2500 adjusted prices, inserted 1200 new records for AAPL",
    "symbol": "AAPL",
    "total_fetched": 2500,
    "total_inserted": 1200
}
```

### 2. Retrieve Adjusted Prices

**GET** `/stocks/{symbol}/adjusted-prices`

Retrieves stored adjusted price data with optional filtering.

#### Query Parameters:
- `start_date` (optional): Filter prices from this date onwards
- `end_date` (optional): Filter prices up to this date
- `skip` (optional, default: 0): Number of records to skip for pagination
- `limit` (optional, default: 100): Maximum number of records to return

#### Request Example:
```bash
curl -X GET "http://localhost:8000/stocks/AAPL/adjusted-prices?start_date=2019-01-02&limit=5" \
  -H "accept: application/json"
```

#### Response Example:
```json
[
    {
        "id": 1,
        "stock_id": 1,
        "date": "2019-01-02",
        "close": 157.92,
        "high": 158.85,
        "low": 154.23,
        "open": 154.89,
        "volume": 37039737,
        "adj_close": 157.92,
        "adj_high": 158.85,
        "adj_low": 154.23,
        "adj_open": 154.89,
        "adj_volume": 37039737,
        "div_cash": 0.0,
        "split_factor": 1.0
    }
]
```

## Configuration

### Environment Variable

Add the following environment variable to your `docker-compose.yml`:

```yaml
environment:
  TIINGO_API_KEY: ca8f2cf4df48422e3b650b5052792ac66379dbd0
```

## Tiingo API Integration

The implementation fetches data from:
```
https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate={date}&token={api_key}
```

### Tiingo Response Format

The API expects this exact response format from Tiingo:

```json
[
    {
        "date": "2019-01-02T00:00:00.000Z",
        "close": 157.92,
        "high": 158.85,
        "low": 154.23,
        "open": 154.89,
        "volume": 37039737,
        "adjClose": 157.92,
        "adjHigh": 158.85,
        "adjLow": 154.23,
        "adjOpen": 154.89,
        "adjVolume": 37039737,
        "divCash": 0.0,
        "splitFactor": 1.0
    }
]
```

## Error Handling

- **400 Bad Request**: Invalid symbol, missing API key, or Tiingo API errors
- **404 Not Found**: Stock symbol not found (for GET endpoint)
- **500 Internal Server Error**: Database or server errors

## Features

1. **Automatic Stock Creation**: If a stock symbol doesn't exist, it's automatically created
2. **Duplicate Prevention**: Existing price records are skipped during insertion
3. **Date Parsing**: Handles Tiingo's ISO datetime format and converts to date
4. **Comprehensive Data**: Stores all fields including adjusted values, dividends, and split factors
5. **Pagination**: GET endpoint supports pagination with skip/limit parameters
6. **Date Filtering**: GET endpoint supports date range filtering

## Testing

### Manual Testing with curl

1. Fetch and store data:
```bash
curl -X POST "http://localhost:8000/stocks/AAPL/fetch-adjusted-prices?start_date=2019-01-02"
```

2. Retrieve stored data:
```bash
curl -X GET "http://localhost:8000/stocks/AAPL/adjusted-prices?limit=5"
```

### Testing with Python

```python
import requests

# Fetch and store
response = requests.post(
    "http://localhost:8000/stocks/AAPL/fetch-adjusted-prices",
    params={"start_date": "2019-01-02"}
)
print("Fetch response:", response.json())

# Retrieve data
response = requests.get(
    "http://localhost:8000/stocks/AAPL/adjusted-prices",
    params={"limit": 5}
)
print("Retrieved data:", response.json())
```

## Implementation Files Modified

1. **`backend/app/models.py`**: Added `AdjustedPrice` model and updated `Stock` model
2. **`backend/app/main.py`**: Added API endpoints, Pydantic models, and Tiingo fetch function
3. **`docker-compose.yml`**: Added `TIINGO_API_KEY` environment variable
