import yfinance as yf
import pandas as pd


def nakit_akisi_getir(hisse_kodu: str) -> pd.DataFrame:
    # 1. Verilen hisse kodu (örneğin "AAPL") için bir borsa nesnesi oluşturur
    hisse = yf.Ticker(hisse_kodu)

    # 2. Yıllık nakit akışı tablosunu pandas DataFrame olarak çeker
    nakit_tablosu = hisse.cashflow

    # 3. Tablo boşsa uyarı verip boş bir tablo döndürür
    if nakit_tablosu is None or nakit_tablosu.empty:
        print(f"{hisse_kodu} için nakit akışı tablosu bulunamadı.")
        return pd.DataFrame()

    # 4. Bulunan tabloyu geri döndürür
    return nakit_tablosu


if __name__ == "__main__":
    # Dosyayı doğrudan çalıştırdığımızda AAPL verisini çekip satır isimlerini yazdırır
    df = nakit_akisi_getir("AAPL")

    if not df.empty:
        print("Nakit akışı tablosundaki satır isimleri:")
        for satir_adi in df.index:
            print("-", satir_adi)
