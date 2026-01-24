import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Add project root to path
# We need to go up one level from 'dashboard'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import get_db
from src.core.portfolio_manager import PortfolioManager

st.set_page_config(page_title="Stock Portfolio System", layout="wide")

st.title("Stock Portfolio & Decision Support System")

# Initialize DB and Manager
db = next(get_db())
pm = PortfolioManager(db)

# Sidebar - Add Transaction
st.sidebar.header("Add Transaction")
with st.sidebar.form("add_txn_form"):
    symbol = st.text_input("Symbol (e.g. AAPL)").upper()
    txn_type = st.selectbox("Type", ["BUY", "SELL", "DEPOSIT", "WITHDRAWAL", "DIVIDEND"])
    date = st.date_input("Date", datetime.now())
    price = st.number_input("Price", min_value=0, step=0)
    quantity = st.number_input("Quantity", min_value=0, step=0)
    commission = st.number_input("Commission", min_value=0, step=0)
    
    submitted = st.form_submit_button("Submit Transaction")
    if submitted and symbol:
        try:
            # We treat the date input as a datetime for the DB
            txn_dt = datetime.combine(date, datetime.min.time())
            
            pm.add_transaction(
                symbol=symbol,
                date=txn_dt,
                type=txn_type,
                price=price,
                quantity=quantity,
                commission=commission
            )
            st.success(f"Transaction for {symbol} added successfully!")
        except Exception as e:
            st.error(f"Error adding transaction: {e}")

# Main Content - Recent Transactions
st.subheader("Recent Transactions")

txns = pm.get_recent_transactions(50)

if txns:
    data = []
    for t in txns:
        asset_name = t.asset.symbol if t.asset else "CASH"
        data.append({
            "ID": t.id,
            "Date": t.date,
            "Symbol": asset_name,
            "Type": t.type.value,
            "Price": t.price,
            "Quantity": t.quantity,
            "Commission": t.commission,
            "Total": (t.price * t.quantity) + t.commission if t.type.value == 'BUY' else (t.price * t.quantity) - t.commission
        })
    st.dataframe(pd.DataFrame(data))
else:
    st.info("No transactions found. Add one from the sidebar.")

db.close()
