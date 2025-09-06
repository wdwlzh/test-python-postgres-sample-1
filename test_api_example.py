#!/usr/bin/env python3
"""
Example usage of the new Adjusted Prices API - matching the requirements exactly
"""

import requests

# Example that matches the requirement format
def test_adjusted_prices_api():
    """
    Test the new adjusted prices API endpoint
    This matches the format requested in the requirements
    """
    base_url = "http://localhost:8000"
    
    print("=== Testing Adjusted Prices API ===\n")
    
    # 1. Fetch and store adjusted prices (with start_date - matching the Tiingo example)
    print("1. Fetching and storing adjusted prices for AAPL with start_date...")
    
    headers = {'Content-Type': 'application/json'}
    
    # POST request to fetch and store data with start_date
    fetch_url = f"{base_url}/stocks/AAPL/fetch-adjusted-prices"
    params = {"start_date": "2019-01-02"}
    
    print(f"Request URL: {fetch_url}")
    print(f"Parameters: {params}")
    
    try:
        fetch_response = requests.post(fetch_url, params=params, headers=headers)
        print(f"Status Code: {fetch_response.status_code}")
        print(f"Response: {fetch_response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the backend is running.")
        print("Run: docker compose up -d")
        return
    
    print("\n" + "="*50 + "\n")
    
    # 1b. Test without start_date (optional parameter)
    print("1b. Testing without start_date (should fetch all available data)...")
    
    fetch_url_no_date = f"{base_url}/stocks/MSFT/fetch-adjusted-prices"
    
    print(f"Request URL: {fetch_url_no_date}")
    print("Parameters: None (start_date is optional)")
    
    try:
        fetch_response_no_date = requests.post(fetch_url_no_date, headers=headers)
        print(f"Status Code: {fetch_response_no_date.status_code}")
        print(f"Response: {fetch_response_no_date.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
    
    print("\n" + "="*50 + "\n")
    
    # 2. Retrieve stored data
    print("2. Retrieving stored adjusted prices...")
    
    get_url = f"{base_url}/stocks/AAPL/adjusted-prices"
    get_params = {"start_date": "2019-01-02", "limit": 5}
    
    print(f"Request URL: {get_url}")
    print(f"Parameters: {get_params}")
    
    try:
        get_response = requests.get(get_url, params=get_params, headers=headers)
        print(f"Status Code: {get_response.status_code}")
        print(f"Response (first 5 records):")
        
        data = get_response.json()
        if data:
            for i, record in enumerate(data[:3]):  # Show first 3 for brevity
                print(f"\nRecord {i+1}:")
                print(f"  Date: {record['date']}")
                print(f"  Close: {record['close']}")
                print(f"  Adj Close: {record['adj_close']}")
                print(f"  Volume: {record['volume']}")
                print(f"  Adj Volume: {record['adj_volume']}")
                print(f"  Div Cash: {record['div_cash']}")
                print(f"  Split Factor: {record['split_factor']}")
        else:
            print("No data found")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
    
    print("\n" + "="*50 + "\n")
    
    # 3. Show the exact format from requirements
    print("3. Expected Tiingo API format (for reference):")
    expected_format = [
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
    print(f"Tiingo format: {expected_format[0]}")

if __name__ == "__main__":
    test_adjusted_prices_api()
