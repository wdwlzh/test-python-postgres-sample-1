-- Init script for Postgres
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

INSERT INTO items (name, description) VALUES ('Sample Item', 'This is a sample item');

-- Tables for stock price data and backtesting
CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS prices (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    open_price DECIMAL(10, 4),
    high DECIMAL(10, 4),
    low DECIMAL(10, 4),
    close DECIMAL(10, 4),
    volume BIGINT,
    UNIQUE(stock_id, date)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_prices_stock_id ON prices(stock_id);
CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(date);
CREATE INDEX IF NOT EXISTS idx_prices_stock_date ON prices(stock_id, date);

-- Optional: Table for backtest results
CREATE TABLE IF NOT EXISTS backtests (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    strategy TEXT,
    start_date DATE,
    end_date DATE,
    initial_capital DECIMAL(15, 2),
    final_capital DECIMAL(15, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
