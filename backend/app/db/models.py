from sqlalchemy import (
    Column, Integer, BigInteger, String, Text, DateTime,
    Enum, ForeignKey, DECIMAL, Date, Boolean
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


# --------------------
# USERS
# --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    balance = Column(DECIMAL(15, 2), default=100000.00)
    status = Column(Enum("ACTIVE", "BLOCKED"), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)


# --------------------
# TRADES
# --------------------
class Trade(Base):
    __tablename__ = "trades"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    symbol = Column(String(20), nullable=False)
    side = Column(Enum("BUY", "SELL"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(12, 2), nullable=False)
    order_type = Column(Enum("MARKET", "LIMIT"), default="MARKET")
    sl = Column(DECIMAL(12, 2))
    target = Column(DECIMAL(12, 2))
    status = Column(Enum("OPEN", "CLOSED"), default="OPEN")
    trade_notes = Column(Text)
    executed_at = Column(DateTime, default=datetime.utcnow)


# --------------------
# POSITIONS
# --------------------
class Position(Base):
    __tablename__ = "positions"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    symbol = Column(String(20), nullable=False)
    net_quantity = Column(Integer, nullable=False)
    avg_price = Column(DECIMAL(12, 2), nullable=False)
    unrealized_pnl = Column(DECIMAL(15, 2), default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)


# --------------------
# ORDER META
# --------------------
class OrderMeta(Base):
    __tablename__ = "orders_meta"

    id = Column(BigInteger, primary_key=True)
    trade_id = Column(BigInteger, ForeignKey("trades.id", ondelete="CASCADE"))
    sl_hit = Column(Boolean, default=False)
    target_hit = Column(Boolean, default=False)
    closed_reason = Column(String(50))
    closed_at = Column(DateTime)


# --------------------
# AI CHAT HISTORY
# --------------------
class AgentChatHistory(Base):
    __tablename__ = "agent_chat_history"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    role = Column(Enum("USER", "AGENT"))
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# --------------------
# DAILY PNL
# --------------------
class DailyPNL(Base):
    __tablename__ = "daily_pnl"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    trade_date = Column(Date)
    realized_pnl = Column(DECIMAL(15, 2), default=0)
    unrealized_pnl = Column(DECIMAL(15, 2), default=0)
