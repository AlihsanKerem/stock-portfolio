import sqlite3

def get_db_connection():
    """Veritabanına bağlanır ve bağlantı nesnesini döndürür."""
    con = sqlite3.connect('portfolio.db') # Dosya adını proje ile uyumlu yaptım
    con.row_factory = sqlite3.Row # Verilere sözlük gibi erişmek için (row['symbol'] diyebilmek için)
    return con

def create_tables():
    """Gerekli tabloları oluşturur."""
    con = get_db_connection()
    cur = con.cursor()

    # 1. Tablo: İşlemler (Senin yapını biraz sadeleştirdim, direkt symbol tutuyoruz)
    # Neden? Python tarafında "ID bulma" karmaşasıyla uğraşmaman için.
    transactions_query = """
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        action TEXT NOT NULL, 
        quantity REAL NOT NULL,
        price REAL NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """
    cur.execute(transactions_query)

    # 2. Tablo: Günlük Portföy Özeti (Grafikler için)
    summary_query = """
    CREATE TABLE IF NOT EXISTS daily_summary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        total_equity REAL,
        profit_loss REAL
    )
    """
    cur.execute(summary_query)

    con.commit() # Değişiklikleri onayla
    con.close()  # Bağlantıyı kapat
    print("Veritabanı ve tablolar başarıyla oluşturuldu/kontrol edildi.")

if __name__ == "__main__":
    # Bu dosya doğrudan çalıştırılırsa tabloları oluştur
    create_tables()