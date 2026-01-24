"""
SQLAlchemy ORM Models for Stock Portfolio System

"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, 
    Enum, ForeignKey, Index, CheckConstraint, Numeric, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import enum

Base = declarative_base()


class TransactionType(enum.Enum):
    """Transaction types for the ledger"""
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"
    SPLIT = "SPLIT"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"


class Currency(enum.Enum):
    """Supported currencies"""
    USD = "USD"
    TRY = "TRY"
    EUR = "EUR"


class AssetType(enum.Enum):
    """Asset categories"""
    STOCK = "STOCK"
    ETF = "ETF"
    CRYPTO = "CRYPTO"
    COMMODITY = "COMMODITY"


# =====================================================================
# CORE TABLES
# =====================================================================

class Asset(Base):
    """
    Master table for all tradeable assets (stocks, ETFs, etc.)
    """
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False, default=AssetType.STOCK)
    currency = Column(Enum(Currency), nullable=False, default=Currency.USD)
    exchange = Column(String(50))  # e.g., "NASDAQ", "BIST"
    sector = Column(String(100))
    industry = Column(String(100))
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="asset", cascade="all, delete-orphan")
    price_history = relationship("PriceHistory", back_populates="asset", cascade="all, delete-orphan")
    watchlist_items = relationship("WatchlistItem", back_populates="asset", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Asset(symbol='{self.symbol}', name='{self.name}')>"


class Transaction(Base):
    """
    Complete transaction ledger - the source of truth for all portfolio calculations
    """
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    
    # Transaction details
    transaction_type = Column(Enum(TransactionType), nullable=False)
    transaction_date = Column(DateTime, nullable=False, index=True)
    quantity = Column(Numeric(precision=18, scale=8), nullable=False)  # High precision for fractional shares
    price = Column(Numeric(precision=18, scale=4), nullable=False)  # Price per unit
    
    # Costs
    commission = Column(Numeric(precision=10, scale=2), default=0.0)
    tax = Column(Numeric(precision=10, scale=2), default=0.0)
    other_fees = Column(Numeric(precision=10, scale=2), default=0.0)
    
    # Calculated fields
    total_amount = Column(Numeric(precision=18, scale=2))  # quantity * price + fees
    
    # Metadata
    notes = Column(String(500))
    broker = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    asset = relationship("Asset", back_populates="transactions")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity != 0', name='check_quantity_not_zero'),
        Index('idx_asset_date', 'asset_id', 'transaction_date'),
    )
    
    def __repr__(self):
        return f"<Transaction({self.transaction_type.value} {self.quantity} @ {self.price})>"


class PriceHistory(Base):
    """
    Historical price data for assets (fetched from yfinance)
    """
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    
    date = Column(DateTime, nullable=False, index=True)
    open = Column(Numeric(precision=18, scale=4))
    high = Column(Numeric(precision=18, scale=4))
    low = Column(Numeric(precision=18, scale=4))
    close = Column(Numeric(precision=18, scale=4), nullable=False)
    volume = Column(Integer)
    adjusted_close = Column(Numeric(precision=18, scale=4))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    asset = relationship("Asset", back_populates="price_history")
    
    __table_args__ = (
        Index('idx_asset_price_date', 'asset_id', 'date', unique=True),
    )
    
    def __repr__(self):
        return f"<PriceHistory({self.asset.symbol} @ {self.date}: {self.close})>"


class DailyPortfolioSnapshot(Base):
    """
    Daily snapshot of total portfolio value for historical tracking and charting
    """
    __tablename__ = 'daily_portfolio_snapshots'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_date = Column(DateTime, nullable=False, unique=True, index=True)
    
    # Portfolio metrics
    total_value = Column(Numeric(precision=18, scale=2), nullable=False)  # Total equity
    cash_balance_usd = Column(Numeric(precision=18, scale=2), default=0.0)
    cash_balance_try = Column(Numeric(precision=18, scale=2), default=0.0)
    
    total_invested = Column(Numeric(precision=18, scale=2))  # Total capital invested
    total_realized_pnl = Column(Numeric(precision=18, scale=2))  # Realized gains/losses
    total_unrealized_pnl = Column(Numeric(precision=18, scale=2))  # Paper gains/losses
    
    # Daily change
    daily_change = Column(Numeric(precision=18, scale=2))
    daily_change_percent = Column(Numeric(precision=8, scale=4))
    
    # Number of positions
    num_positions = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Snapshot({self.snapshot_date}: ${self.total_value})>"


class CashAccount(Base):
    """
    Cash balances in different currencies
    """
    __tablename__ = 'cash_accounts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(Enum(Currency), nullable=False, unique=True)
    balance = Column(Numeric(precision=18, scale=2), nullable=False, default=0.0)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_non_negative_balance'),
    )
    
    def __repr__(self):
        return f"<CashAccount({self.currency.value}: {self.balance})>"


# =====================================================================
# ANALYSIS & WATCHLIST TABLES
# =====================================================================

class Watchlist(Base):
    """
    Watchlist groups (e.g., "Tech Stocks", "Dividend Plays")
    """
    __tablename__ = 'watchlists'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Watchlist('{self.name}')>"


class WatchlistItem(Base):
    """
    Individual stocks in a watchlist
    """
    __tablename__ = 'watchlist_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    watchlist_id = Column(Integer, ForeignKey('watchlists.id'), nullable=False)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    
    target_price = Column(Numeric(precision=18, scale=4))
    notes = Column(String(500))
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    watchlist = relationship("Watchlist", back_populates="items")
    asset = relationship("Asset", back_populates="watchlist_items")
    
    __table_args__ = (
        Index('idx_watchlist_asset', 'watchlist_id', 'asset_id', unique=True),
    )
    
    def __repr__(self):
        return f"<WatchlistItem({self.asset.symbol} in {self.watchlist.name})>"


class TechnicalSignal(Base):
    """
    Technical analysis signals (RSI, MACD, etc.) - calculated daily
    """
    __tablename__ = 'technical_signals'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    asset_id = Column(Integer, ForeignKey('assets.id'), nullable=False)
    
    signal_date = Column(DateTime, nullable=False, index=True)
    
    # Indicators
    rsi_14 = Column(Numeric(precision=8, scale=4))
    macd = Column(Numeric(precision=18, scale=8))
    macd_signal = Column(Numeric(precision=18, scale=8))
    macd_histogram = Column(Numeric(precision=18, scale=8))
    sma_50 = Column(Numeric(precision=18, scale=4))
    sma_200 = Column(Numeric(precision=18, scale=4))
    
    # Signal interpretation
    signal = Column(String(10))  # "BUY", "SELL", "HOLD"
    signal_strength = Column(Numeric(precision=5, scale=2))  # -1.0 to 1.0
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_asset_signal_date', 'asset_id', 'signal_date', unique=True),
    )
    
    def __repr__(self):
        return f"<TechnicalSignal({self.asset.symbol} @ {self.signal_date}: {self.signal})>"


# =====================================================================
# DATABASE INITIALIZATION
# =====================================================================

def init_database(db_url: str = "sqlite:///database/portfolio.db"):
    """
    Initialize the database and create all tables
    
    Args:
        db_url: Database connection string
    """
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine):
    """
    Get a database session
    """
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Example: Create the database
    engine = init_database()
    print("✅ Database schema created successfully!")