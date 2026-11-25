import yfinance as yf


def get_cash_flow(ticker_symbol):
    # Create a Ticker object for the given stock symbol
    company = yf.Ticker(ticker_symbol)

    # Fetch the annual cash flow statement (returns a pandas DataFrame)
    cash_flow_df = company.cashflow

    # Get the reporting currency automatically (USD for AAPL, EUR for SAP.DE)
    currency = company.info.get("financialCurrency", "Unknown")

    return cash_flow_df, currency


# --- FETCH DATA FOR BOTH APPLE AND SAP ---
tickers = ["AAPL", "SAP.DE"]  # List of target companies
cash_flow_tables = {}         # Dictionary to store each company's DataFrame

for symbol in tickers:
    # Unpack the DataFrame and currency returned by the function
    cf_df, currency = get_cash_flow(symbol)
    
    # Save the table in our dictionary for later use (e.g., cash_flow_tables["AAPL"])
    cash_flow_tables[symbol] = cf_df

    print(f"\n==================== {symbol} ({currency}) ====================")
    
    # Print the full cash flow table
    print(cf_df)

    # Get the newest fiscal year date (first 10 characters: YYYY-MM-DD)
    latest_date = str(cf_df.columns[0])[:10]

    # Extract the 3 most important rows for DCF from the newest column (.iloc[0])
    operating_cf = cf_df.loc["Operating Cash Flow"].iloc[0]
    capex = cf_df.loc["Capital Expenditure"].iloc[0]
    fcf = cf_df.loc["Free Cash Flow"].iloc[0]

    print(f"\n--- Key DCF Metrics ({latest_date}) ---")
    print(f"Operating Cash Flow : {operating_cf:,.0f} {currency}")
    print(f"Capital Expenditure : {capex:,.0f} {currency}")
    print(f"Free Cash Flow (FCF): {fcf:,.0f} {currency}")

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
