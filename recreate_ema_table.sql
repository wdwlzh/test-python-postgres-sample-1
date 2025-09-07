-- WARNING: This will delete all existing data in ema_backtests table
-- Only run this if you're okay with losing existing backtest results

DROP TABLE IF EXISTS ema_backtests;

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
    num_trades INTEGER,
    cagr DECIMAL(10,6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
