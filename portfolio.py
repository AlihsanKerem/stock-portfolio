from database import get_db_connection # con yerine fonksiyonu import ettik
import datetime

def add_transaction(symbol, action, quantity, price, date=None):
    """Veritabanına işlem ekler."""
    if date is None:
        # Eğer tarih verilmezse bugünün tarihini al
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    symbol = symbol.upper()
    
    # 1. Bağlantıyı aç
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 2. İşlemi yap
    try:
        cur.execute(
            "INSERT INTO transactions (symbol, action, quantity, price, date) VALUES (?, ?, ?, ?, ?)",
            (symbol, action, quantity, price, date)
        )
        conn.commit()
        print(f"✅ {symbol} için {action} işlemi kaydedildi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
    finally:
        # 3. Bağlantıyı her durumda kapat (Hata olsa bile)
        conn.close()

def get_portfolio_status():
    """
    Tüm işlemleri tarar ve eldeki GÜNCEL hisse adetlerini hesaplar.
    Geriye şöyle bir sözlük döndürür: {'THYAO': 100, 'ASELS': 50}
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Verileri sözlük gibi çekmek için ayar (database.py'de row_factory varsa gerekmez ama garanti olsun)
    conn.row_factory = None 
    
    cur.execute("SELECT symbol, action, quantity FROM transactions")
    transactions = cur.fetchall()
    conn.close()

    portfolio = {}

    for row in transactions:
        sym = row[0]       # symbol
        action = row[1]    # action
        qty = row[2]       # quantity

        if sym not in portfolio:
            portfolio[sym] = 0

        if action == 'BUY':
            portfolio[sym] += qty
        elif action == 'SELL':
            portfolio[sym] -= qty
    
    # Adedi 0 olanları listeden temizleyelim
    return {k: v for k, v in portfolio.items() if v > 0}

def buy_stock(symbol, quantity, price, date=None):
    add_transaction(symbol, 'BUY', quantity, price, date)

def sell_stock(symbol, quantity, price, date=None):
    symbol = symbol.upper()
    current_portfolio = get_portfolio_status() # Sözlük döner: {'THYAO': 100}
    
    # 1. Hisse hiç var mı?
    current_qty = current_portfolio.get(symbol, 0)
    
    # 2. Yeterli miktarda var mı?
    if current_qty < quantity:
        print(f"⚠️ HATA: Yetersiz bakiye! Eldeki {symbol}: {current_qty}, Satılmak istenen: {quantity}")
        return # İşlemi durdur

    # Sorun yoksa sat
    add_transaction(symbol, 'SELL', quantity, price, date)