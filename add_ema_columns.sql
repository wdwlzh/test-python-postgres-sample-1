-- Add missing columns to ema_backtests table
-- Run this SQL in your PostgreSQL database (pgAdmin, psql, etc.)

ALTER TABLE ema_backtests 
ADD COLUMN IF NOT EXISTS num_trades INTEGER,
ADD COLUMN IF NOT EXISTS cagr DECIMAL(10,6);

-- Verify the columns were added
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'ema_backtests' 
ORDER BY ordinal_position;
