#!/usr/bin/env python3
"""
Example script demonstrating how to use the Enhanced EMA Backtester class.

This script shows how to:
1. Initialize the EMABacktester
2. Run backtests for multiple EMA combinations
3. Find the best performing combination
4. Get summary statistics

Usage:
    python ema_backtest_example.py
"""

from datetime import date
from ema_backtester import EMABacktester
from database import SessionLocal

def main():
    """Demonstrate the EMA Backtester functionality."""
    
    # Database session
    db = SessionLocal()
    
    try:
        # Initialize the backtester
        symbol = "QQQ"
        start_date = date(2010, 1, 1)
        end_date = date(2025, 8, 15)
        initial_cash = 10000
        
        print(f"Initializing EMA Backtester for {symbol}")
        print(f"Period: {start_date} to {end_date}")
        print(f"Initial cash: ${initial_cash:,.2f}")
        print("-" * 50)
        
        backtester = EMABacktester(symbol, start_date, end_date, initial_cash)
        
        # Example 1: Run with default combinations (all multiples of 5)
        print("Example 1: Running with default EMA combinations...")
        
        # For demonstration, let's use a smaller subset to save time
        short_periods = [5, 10, 15, 20]  # Multiples of 5, max 60
        long_periods = [25, 30, 35, 40]  # Multiples of 5, max 120
        
        results = backtester.run_combinations(db, short_periods, long_periods)
        print(f"Completed {len(results)} backtests")
        
        if results:
            # Show first few results
            print("\nFirst few results:")
            for i, result in enumerate(results[:3]):
                print(f"  EMA {result['short_period']}/{result['long_period']}: "
                      f"Final Cash: ${result['final_cash']:,.2f}, "
                      f"Return: {result['total_return_percent']:.2f}%")
        
        print("-" * 50)
        
        # Example 2: Find the best combination
        print("Example 2: Finding the best performing combination...")
        
        best = backtester.get_best_combination(db, metric="total_return_percent")
        if best:
            print(f"Best combination: EMA {best.short_period}/{best.long_period}")
            print(f"  Initial Cash: ${best.initial_cash:,.2f}")
            print(f"  Final Cash: ${best.final_cash:,.2f}")
            print(f"  Total Return: {best.total_return:.4f}")
            print(f"  Return Percentage: {best.total_return_percent:.2f}%")
        else:
            print("No backtest results found")
        
        print("-" * 50)
        
        # Example 3: Get summary statistics
        print("Example 3: Getting summary statistics...")
        
        summary = backtester.get_combination_summary(db)
        if "message" not in summary:
            print(f"Total combinations tested: {summary['total_combinations']}")
            print(f"Best return: {summary['best_return_percent']:.2f}%")
            print(f"Worst return: {summary['worst_return_percent']:.2f}%")
            print(f"Average return: {summary['average_return_percent']:.2f}%")
            print(f"Profitable combinations: {summary['profitable_combinations']}")
        else:
            print(summary["message"])
        
        print("-" * 50)
        
        # Example 4: Validate parameter constraints
        print("Example 4: Testing parameter validation...")
        
        # Test invalid periods (not multiples of 5)
        invalid_short = [7, 13, 22]  # Not multiples of 5
        invalid_long = [33, 47, 65]   # Not multiples of 5
        
        try:
            combinations = backtester.generate_ema_combinations(invalid_short, invalid_long)
            print(f"Generated {len(combinations)} combinations after filtering invalid periods")
        except ValueError as e:
            print(f"Validation error: {e}")
        
        # Test periods exceeding limits
        print("\nTesting period limits...")
        over_limit_short = [65, 70]  # Exceeds max 60
        over_limit_long = [125, 130]  # Exceeds max 120
        
        try:
            combinations = backtester.generate_ema_combinations(over_limit_short, over_limit_long)
            print(f"Generated {len(combinations)} combinations after filtering over-limit periods")
        except ValueError as e:
            print(f"Validation error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    
    finally:
        db.close()
        print("\nExample completed!")

if __name__ == "__main__":
    main()
