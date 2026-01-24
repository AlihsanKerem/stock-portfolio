# Stock Portfolio & Decision Support System

A comprehensive Python-based system for tracking stock portfolios, analyzing performance, and providing AI-powered decision support.

## Project Structure
```
stock-portfolio-system/
├── config/             # Configuration
├── database/           # Database models & connection
├── src/                # source code
│   ├── core/           # Core logic (PortfolioManager)
│   ├── analysis/       # Technical analysis
│   └── data/           # Data fetching
├── scripts/            # Utility scripts (init_db, etc)
└── tests/              # Tests
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   This script creates the tables in SQLite.
   ```bash
   python scripts/init_db.py
   ```
   *Note: On this environment, the database is stored at `C:/Users/Aliihsan/stock_portfolio_mcp.db` to avoid WSL file locking issues.*

3. **Run Tests**
   ```bash
   python tests/test_setup.py
   ```

## Tech Stack
* **Language:** Python 3.10+
* **Data:** yfinance
* **Database:** SQLite (SQLAlchemy)
* **Analysis:** pandas, pandas-ta
* **Dashboard:** Streamlit (Planned)
