CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    balance DECIMAL(15,2) DEFAULT 100000.00,
    status ENUM('ACTIVE','BLOCKED') DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE trades (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side ENUM('BUY','SELL') NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    order_type ENUM('MARKET','LIMIT') DEFAULT 'MARKET',
    sl DECIMAL(12,2) NULL,
    target DECIMAL(12,2) NULL,
    status ENUM('OPEN','CLOSED') DEFAULT 'OPEN',
    trade_notes TEXT NULL,              -- ✅ REQUIRED BY YOU
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_user_symbol (user_id, symbol),
    INDEX idx_user_date (user_id, executed_at),

    CONSTRAINT fk_trades_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE positions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    net_quantity INT NOT NULL,
    avg_price DECIMAL(12,2) NOT NULL,
    unrealized_pnl DECIMAL(15,2) DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uq_user_symbol (user_id, symbol),

    CONSTRAINT fk_positions_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE orders_meta (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    trade_id BIGINT NOT NULL,
    sl_hit BOOLEAN DEFAULT FALSE,
    target_hit BOOLEAN DEFAULT FALSE,
    closed_reason VARCHAR(50) NULL,
    closed_at TIMESTAMP NULL,

    CONSTRAINT fk_orders_trade
        FOREIGN KEY (trade_id) REFERENCES trades(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE agent_chat_history (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    role ENUM('USER','AGENT') NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_user_chat (user_id, created_at),

    CONSTRAINT fk_chat_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE daily_pnl (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    trade_date DATE NOT NULL,
    realized_pnl DECIMAL(15,2) DEFAULT 0,
    unrealized_pnl DECIMAL(15,2) DEFAULT 0,

    UNIQUE KEY uq_user_date (user_id, trade_date),

    CONSTRAINT fk_pnl_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;
