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

def calculate_dcf(last_fcf, growth_rate, wacc, terminal_growth_rate, cash, total_debt, shares_outstanding, years=5):
    # WACC must be greater than the terminal growth rate for the formula to hold
    if wacc <= terminal_growth_rate:
        raise ValueError("WACC must be greater than terminal growth rate!")

    projected_fcfs = []  # List to store projected Free Cash Flows for future years
    total_pv_fcf = 0     # Accumulator for the sum of present values of future cash flows

    # STEP 1 & 2: Project future cash flows and discount them to present value
    for year in range(1, years + 1):  # Loop through each year from 1 to 5
        future_fcf = last_fcf * ((1 + growth_rate) ** year)  # Calculate projected FCF for the given year
        projected_fcfs.append(future_fcf)  # Save FCF to access the final year later

        present_value = future_fcf / ((1 + wacc) ** year)  # Discount future FCF back to today using WACC
        total_pv_fcf += present_value  # Add present value to the running total

    # STEP 3: Calculate Terminal Value (Gordon Growth Model)
    final_year_fcf = projected_fcfs[-1]  # Get the final projected year's FCF (Year 5)
    terminal_value = (final_year_fcf * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)  # Estimate value beyond the projection period
    pv_terminal_value = terminal_value / ((1 + wacc) ** years)  # Discount Terminal Value back to present day

    # STEP 4: Bridge from Enterprise Value to Intrinsic Value per Share
    enterprise_value = total_pv_fcf + pv_terminal_value  # Calculate total Enterprise Value (EV)
    equity_value = enterprise_value + cash - total_debt  # Add cash and subtract debt to get Equity Value
    intrinsic_value_per_share = equity_value / shares_outstanding  # Divide by total shares to get per-share price

    return round(intrinsic_value_per_share, 2)  # Round result to 2 decimal places and return


# --- EXAMPLE TEST ---
estimated_price = calculate_dcf(
    last_fcf=100_000_000,           # Last annual Free Cash Flow (FCF)
    growth_rate=0.10,               # Expected annual growth rate (10%) for the next 5 years
    wacc=0.12,                      # Discount rate / Cost of Capital (12%)
    terminal_growth_rate=0.03,      # Perpetual growth rate (3%) after Year 5
    cash=50_000_000,                # Cash and cash equivalents
    total_debt=80_000_000,          # Total debt
    shares_outstanding=20_000_000   # Total diluted shares outstanding
)

print(f"Estimated Intrinsic Value per Share: {estimated_price}")
