import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.getcwd())

from database.connection import get_db
from src.core.portfolio_manager import PortfolioManager

def test_add_transaction():
    print("Testing PortfolioManager...")
    
    # Get a session
    db = next(get_db())
    
    pm = PortfolioManager(db)
    
    # Test Adding a transaction
    try:
        print("Adding a test transaction for AAPL...")
        txn = pm.add_transaction(
            symbol="AAPL",
            date=datetime.now(),
            type="BUY",
            price=150.0,
            quantity=10,
            commission=1.5
        )
        print(f"Transaction added: ID={txn.id}, Asset={txn.asset.symbol}, Type={txn.type}")
    except Exception as e:
        print(f"Error adding transaction: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_add_transaction()
