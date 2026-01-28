import database
import portfolio
import time

def menu():
    print("\n--- Hisse Senedi Portföy Yönetim Sistemi ---")
    print("1. Hisse Al")
    print("2. Hisse Sat")
    print("3. Portföy Durumunu Görüntüle")
    print("4. Çıkış")

def main():
    database.create_tables() 
    time.sleep(1)

    while True:
        menu()
        choice = input("Seçiminiz (1-4): ")

        if choice == '1':
            symbol = input("Hisse sembolü: ")
            quantity = float(input("Adet: "))
            price = float(input("Fiyat: "))
            portfolio.buy_stock(symbol, quantity, price)
        elif choice == '2':
            symbol = input("Hisse sembolü: ")
            quantity = float(input("Adet: "))
            price = float(input("Fiyat: "))
            portfolio.sell_stock(symbol, quantity, price)
        elif choice == '3':
            status = portfolio.get_portfolio_status()
            print("\n--- Portföy Durumu ---")
            for sym, qty in status.items():
                print(f"{sym}: {qty} adet")
        elif choice == '4':
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")
    print("Program sonlandı.")

if __name__ == "__main__":
    main()