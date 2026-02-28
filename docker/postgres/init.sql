-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create stocks table
CREATE TABLE IF NOT EXISTS stocks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    market VARCHAR(10),
    industry VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create stock_daily table
CREATE TABLE IF NOT EXISTS stock_daily (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    open DECIMAL(10, 3),
    high DECIMAL(10, 3),
    low DECIMAL(10, 3),
    close DECIMAL(10, 3),
    volume BIGINT,
    amount DECIMAL(20, 3),
    change DECIMAL(10, 3),
    change_percent DECIMAL(10, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, date)
);

-- Create technical_indicators table
CREATE TABLE IF NOT EXISTS technical_indicators (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    ma5 DECIMAL(10, 3),
    ma10 DECIMAL(10, 3),
    ma20 DECIMAL(10, 3),
    ma30 DECIMAL(10, 3),
    ma60 DECIMAL(10, 3),
    rsi DECIMAL(10, 3),
    macd DECIMAL(10, 3),
    macd_signal DECIMAL(10, 3),
    macd_histogram DECIMAL(10, 3),
    kdj_k DECIMAL(10, 3),
    kdj_d DECIMAL(10, 3),
    kdj_j DECIMAL(10, 3),
    boll_upper DECIMAL(10, 3),
    boll_middle DECIMAL(10, 3),
    boll_lower DECIMAL(10, 3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, date)
);

-- Create ml_predictions table
CREATE TABLE IF NOT EXISTS ml_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    model_version VARCHAR(50) NOT NULL,
    prediction_date DATE NOT NULL,
    prediction_horizon INTEGER NOT NULL, -- days
    predicted_price DECIMAL(10, 3),
    confidence DECIMAL(5, 3),
    trend VARCHAR(20), -- 'up', 'down', 'neutral'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_id, model_version, prediction_date, prediction_horizon)
);

-- Create users table (for future authentication)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create user_portfolios table
CREATE TABLE IF NOT EXISTS user_portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stock_id UUID NOT NULL REFERENCES stocks(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    purchase_price DECIMAL(10, 3) NOT NULL,
    purchase_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_stock_daily_stock_id ON stock_daily(stock_id);
CREATE INDEX idx_stock_daily_date ON stock_daily(date);
CREATE INDEX idx_technical_indicators_stock_id ON technical_indicators(stock_id);
CREATE INDEX idx_technical_indicators_date ON technical_indicators(date);
CREATE INDEX idx_ml_predictions_stock_id ON ml_predictions(stock_id);
CREATE INDEX idx_ml_predictions_prediction_date ON ml_predictions(prediction_date);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_stocks_updated_at BEFORE UPDATE ON stocks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stock_daily_updated_at BEFORE UPDATE ON stock_daily
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_technical_indicators_updated_at BEFORE UPDATE ON technical_indicators
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ml_predictions_updated_at BEFORE UPDATE ON ml_predictions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_portfolios_updated_at BEFORE UPDATE ON user_portfolios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for testing
INSERT INTO stocks (code, name, market, industry) VALUES
    ('000001', '平安银行', 'SZ', '银行'),
    ('600036', '招商银行', 'SH', '银行'),
    ('000858', '五粮液', 'SZ', '食品饮料'),
    ('600519', '贵州茅台', 'SH', '食品饮料'),
    ('300750', '宁德时代', 'SZ', '电力设备')
ON CONFLICT (code) DO NOTHING;