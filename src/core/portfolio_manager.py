from sqlalchemy.orm import Session
from src.data.models import Transaction, Asset, TransactionType
from datetime import datetime
import pandas as pd

class PortfolioManager:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add_transaction(self, symbol: str, date: datetime, type: str, price: float, quantity: float, commission: float = 0.0, currency: str = "USD"):
        """
        Adds a new transaction to the ledger.
        If the asset does not exist, it creates it.
        """
        # 1. Get or Create Asset
        asset = self.db.query(Asset).filter(Asset.symbol == symbol).first()
        if not asset:
            asset = Asset(symbol=symbol, name=symbol) # Valid ticker check should happen before this
            self.db.add(asset)
            self.db.commit()
            self.db.refresh(asset)
        
        # 2. Create Transaction
        new_txn = Transaction(
            asset_id=asset.id,
            date=date,
            type=TransactionType(type),
            price=price,
            quantity=quantity,
            commission=commission,
            currency=currency
        )
        self.db.add(new_txn)
        self.db.commit()
        return new_txn

    def get_current_holdings(self):
        """
        Calculates current holdings based on the transaction ledger.
        Returns a DataFrame.
        """
        # This is a skeleton logic - needs robust implementation of FIFO/Weighted Avg later
        pass

    def get_portfolio_value(self):
        """
        Fetches live prices for current holdings and returns total portfolio value.
        """
        pass
    
    def get_cash_balance(self):
        """
        Returns the calculated cash balance from deposits/withdrawals/buys/sells.
        """
        pass

    def get_recent_transactions(self, limit: int = 20):
        """
        Returns the most recent transactions with asset relationship.
        """
        return self.db.query(Transaction).order_by(Transaction.date.desc()).limit(limit).all()