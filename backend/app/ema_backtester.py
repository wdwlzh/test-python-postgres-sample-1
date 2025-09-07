from sqlalchemy.orm import Session
from .models import EMABacktest
from .backtest import BacktestEngine
from .strategies.ema_crossover import EMACrossoverStrategy
from datetime import date
from typing import List, Tuple, Optional
import itertools

class EMABacktester:
    """
    Enhanced EMA Backtester class for testing EMA crossover strategies with multiple combinations.
    
    This class:
    1. Tests EMA crossover strategy for a given symbol with different short and long EMA combinations
    2. Short periods range from 3 to 20
    3. Long periods range from 10 to 60
    4. Records comprehensive backtest results in the database
    """
    
    def __init__(self, symbol: str, start_date: date, end_date: date, initial_cash: float = 10000):
        """
        Initialize the EMA Backtester.
        
        Args:
            symbol: Stock symbol to backtest (e.g., "QQQ")
            start_date: Start date for backtesting
            end_date: End date for backtesting
            initial_cash: Initial cash amount for backtesting
        """
        self.symbol = symbol.upper()
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self._validate_parameters()

    def _validate_parameters(self):
        """Validate initialization parameters."""
        if self.initial_cash <= 0:
            raise ValueError("Initial cash must be positive")
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")

    def generate_ema_combinations(self, 
                                short_periods: Optional[List[int]] = None, 
                                long_periods: Optional[List[int]] = None) -> List[Tuple[int, int]]:
        """
        Generate all valid EMA period combinations.
        
        Args:
            short_periods: List of short EMA periods (3 to 20)
            long_periods: List of long EMA periods (10 to 60)
            
        Returns:
            List of (short_period, long_period) tuples
        """
        if short_periods is None:
            short_periods = list(range(3, 21))  # 3, 4, 5, ..., 20
        if long_periods is None:
            long_periods = list(range(10, 61))  # 10, 11, 12, ..., 60

        # Validate and filter periods
        short_periods = self._validate_periods(short_periods, max_period=20, period_type="short")
        long_periods = self._validate_periods(long_periods, max_period=60, period_type="long")

        # Generate valid combinations (short < long)
        combinations = []
        for short, long in itertools.product(short_periods, long_periods):
            if short < long:
                combinations.append((short, long))
        
        return combinations

    def _validate_periods(self, periods: List[int], max_period: int, period_type: str) -> List[int]:
        """
        Validate that periods are positive integers within limits.
        
        Args:
            periods: List of periods to validate
            max_period: Maximum allowed period
            period_type: Type of period ("short" or "long") for error messages
            
        Returns:
            Validated list of periods
        """
        validated = []
        invalid_periods = []
        
        for period in periods:
            if not isinstance(period, int) or period <= 0:
                invalid_periods.append(f"{period} (must be positive integer)")
                continue
            if period > max_period:
                invalid_periods.append(f"{period} (exceeds max {max_period})")
                continue
            validated.append(period)
        
        if invalid_periods:
            print(f"Warning: Skipping invalid {period_type} periods: {', '.join(invalid_periods)}")
        
        if not validated:
            error_msg = f"No valid {period_type} periods provided. "
            error_msg += f"Valid periods must be positive integers ≤ {max_period}. "
            if period_type == "short":
                error_msg += f"Examples: 3, 4, 5, 6, 7, 8, etc. (up to {max_period})"
            else:
                error_msg += f"Examples: 10, 11, 12, 13, 14, 15, etc. (up to {max_period})"
            raise ValueError(error_msg)
        
        return sorted(validated)

    def run_single_combination(self, db: Session, short_period: int, long_period: int) -> Optional[dict]:
        """
        Run backtest for a single EMA combination.
        Stores num_trades and CAGR in the database.
        """
        try:
            strategy = EMACrossoverStrategy(short_period=short_period, long_period=long_period)
            engine = BacktestEngine(strategy, self.symbol, self.start_date, self.end_date, self.initial_cash)
            result = engine.run(db)

            if "error" in result:
                print(f"Error for EMA {short_period}/{long_period} on {self.symbol}: {result['error']}")
                return None

            # Calculate number of trades
            num_trades = result.get("num_trades")
            if num_trades is None and "trades" in result:
                num_trades = len(result["trades"])

            # Calculate CAGR
            years = (self.end_date - self.start_date).days / 365.25
            cagr = None
            if years > 0 and float(self.initial_cash) > 0 and float(result["final_cash"]) > 0:
                cagr = (float(result["final_cash"]) / float(self.initial_cash)) ** (1 / years) - 1

            # Create database record
            ema_backtest = EMABacktest(
                symbol=self.symbol,
                short_period=short_period,
                long_period=long_period,
                start_date=self.start_date,
                end_date=self.end_date,
                initial_cash=self.initial_cash,
                final_cash=result["final_cash"],
                total_return=result["total_return"],
                total_return_percent=result["total_return_percent"],
                num_trades=num_trades,
                cagr=cagr
            )
            db.add(ema_backtest)
            db.commit()
            db.refresh(ema_backtest)

            # Add combination info to result
            result.update({
                "symbol": self.symbol,
                "short_period": short_period,
                "long_period": long_period,
                "start_date": str(self.start_date),
                "end_date": str(self.end_date),
                "initial_cash": float(self.initial_cash),
                "final_cash": float(result["final_cash"]),
                "total_return": float(result["total_return"]),
                "total_return_percent": float(result["total_return_percent"]),
                "num_trades": num_trades,
                "cagr": cagr,
                "backtest_id": ema_backtest.id
            })

            return result

        except Exception as e:
            db.rollback()
            print(f"Exception during backtest for EMA {short_period}/{long_period}: {str(e)}")
            return None

    def run_combinations(self, db: Session, 
                        short_periods: Optional[List[int]] = None, 
                        long_periods: Optional[List[int]] = None) -> List[dict]:
        """
        Run backtests for multiple EMA combinations.
        
        Args:
            db: Database session
            short_periods: List of short EMA periods (multiples of 5, max 60)
            long_periods: List of long EMA periods (multiples of 5, max 120)
            
        Returns:
            List of backtest results
        """
        combinations = self.generate_ema_combinations(short_periods, long_periods)
        
        print(f"Running {len(combinations)} EMA combinations for {self.symbol} "
              f"from {self.start_date} to {self.end_date}")
        
        results = []
        successful_runs = 0
        
        for i, (short, long) in enumerate(combinations, 1):
            print(f"Processing combination {i}/{len(combinations)}: EMA {short}/{long}")
            
            result = self.run_single_combination(db, short, long)
            if result:
                results.append(result)
                successful_runs += 1
        
        print(f"Completed {successful_runs}/{len(combinations)} backtests successfully")
        return results

    def get_best_combination(self, db: Session, metric: str = "total_return_percent") -> Optional[EMABacktest]:
        """
        Get the best performing EMA combination for this symbol and date range.
        
        Args:
            db: Database session
            metric: Metric to optimize ("total_return_percent", "total_return", or "final_cash")
            
        Returns:
            Best performing EMABacktest record or None
        """
        valid_metrics = ["total_return_percent", "total_return", "final_cash"]
        if metric not in valid_metrics:
            raise ValueError(f"Metric must be one of {valid_metrics}")

        query = db.query(EMABacktest).filter(
            EMABacktest.symbol == self.symbol,
            EMABacktest.start_date == self.start_date,
            EMABacktest.end_date == self.end_date,
            EMABacktest.initial_cash == self.initial_cash
        )

        if metric == "total_return_percent":
            best = query.order_by(EMABacktest.total_return_percent.desc()).first()
        elif metric == "total_return":
            best = query.order_by(EMABacktest.total_return.desc()).first()
        else:  # final_cash
            best = query.order_by(EMABacktest.final_cash.desc()).first()

        return best

    def get_combination_summary(self, db: Session) -> dict:
        """
        Get summary statistics for all combinations tested.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with summary statistics
        """
        query = db.query(EMABacktest).filter(
            EMABacktest.symbol == self.symbol,
            EMABacktest.start_date == self.start_date,
            EMABacktest.end_date == self.end_date,
            EMABacktest.initial_cash == self.initial_cash
        )

        results = query.all()
        if not results:
            return {"message": "No backtest results found"}

        returns = [float(r.total_return_percent) for r in results]
        
        return {
            "symbol": self.symbol,
            "total_combinations": len(results),
            "best_return_percent": max(returns),
            "worst_return_percent": min(returns),
            "average_return_percent": sum(returns) / len(returns),
            "profitable_combinations": len([r for r in returns if r > 0]),
            "date_range": f"{self.start_date} to {self.end_date}"
        }
