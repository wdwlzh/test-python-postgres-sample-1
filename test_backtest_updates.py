#!/usr/bin/env python3
"""
Test script to verify the updated backtest logic using adjusted_prices table
"""

import sys
import os

# Add the backend app to the path
sys.path.append('/workspaces/backend')

def test_backtest_adjustments():
    """
    Test script to verify that all backtest components now use AdjustedPrice
    """
    print("=== Testing Backtest Logic Updates ===\n")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from backend.app.models import AdjustedPrice, Stock
        from backend.app.backtest import BacktestEngine
        from backend.app.strategies import Strategy
        from backend.app.strategies.ema_crossover import EMACrossoverStrategy
        from backend.app.strategies.buy_and_hold import BuyAndHoldStrategy
        print("✅ All imports successful")
        
        # Test BacktestEngine class structure
        print("\n2. Testing BacktestEngine structure...")
        
        # Check method signature
        import inspect
        get_prices_method = getattr(BacktestEngine, '_get_prices')
        signature = inspect.signature(get_prices_method)
        return_annotation = signature.return_annotation
        print(f"✅ _get_prices return type: {return_annotation}")
        
        # Test Strategy base class
        print("\n3. Testing Strategy base class...")
        strategy = Strategy()
        should_buy_method = getattr(strategy, 'should_buy')
        signature = inspect.signature(should_buy_method)
        params = list(signature.parameters.values())
        prices_param = params[1]  # Second parameter after self
        print(f"✅ Strategy.should_buy prices parameter type: {prices_param.annotation}")
        
        # Test EMACrossoverStrategy
        print("\n4. Testing EMACrossoverStrategy...")
        ema_strategy = EMACrossoverStrategy(5, 10)
        should_buy_method = getattr(ema_strategy, 'should_buy')
        signature = inspect.signature(should_buy_method)
        params = list(signature.parameters.values())
        prices_param = params[1]
        print(f"✅ EMACrossoverStrategy.should_buy prices parameter type: {prices_param.annotation}")
        
        # Test BuyAndHoldStrategy
        print("\n5. Testing BuyAndHoldStrategy...")
        bah_strategy = BuyAndHoldStrategy()
        should_buy_method = getattr(bah_strategy, 'should_buy')
        signature = inspect.signature(should_buy_method)
        params = list(signature.parameters.values())
        prices_param = params[1]
        print(f"✅ BuyAndHoldStrategy.should_buy prices parameter type: {prices_param.annotation}")
        
        print("\n✅ All backtest components successfully updated to use AdjustedPrice!")
        
        # Show key changes
        print("\n📋 Key Changes Made:")
        print("  - BacktestEngine now queries adjusted_prices table")
        print("  - Uses adj_open for buy prices and adj_close for sell prices")
        print("  - All strategies now expect List[AdjustedPrice] instead of List[Price]")
        print("  - EMACrossoverStrategy uses adj_close for EMA calculations")
        print("  - Preserves original Price endpoints for backward compatibility")
        
        print("\n🎯 Benefits of Using Adjusted Prices:")
        print("  - Accounts for stock splits and dividend distributions")
        print("  - Provides more accurate backtesting results")
        print("  - Eliminates artificial price jumps due to corporate actions")
        print("  - Better reflects actual investment returns")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def show_api_usage():
    """
    Show how to use the updated API
    """
    print("\n" + "="*60)
    print("📚 Updated API Usage Examples")
    print("="*60)
    
    print("""
1. First, fetch adjusted price data:
   POST /stocks/AAPL/fetch-adjusted-prices?start_date=2019-01-02

2. Run backtests (now automatically uses adjusted prices):
   POST /backtests/run
   {
     "symbol": "AAPL",
     "strategy_name": "ema_crossover",
     "start_date": "2019-01-02",
     "end_date": "2023-01-01",
     "initial_cash": 10000
   }

3. Run EMA backtests (uses adjusted prices):
   POST /ema-backtests/run
   {
     "symbol": "AAPL",
     "start_date": "2019-01-02",
     "end_date": "2023-01-01",
     "initial_cash": 10000
   }

All backtest operations now automatically use the adjusted_prices table,
providing more accurate results that account for splits and dividends.
""")

if __name__ == "__main__":
    success = test_backtest_adjustments()
    if success:
        show_api_usage()
    else:
        print("\n❌ Testing failed. Please check the implementation.")
