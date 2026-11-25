import yfinance as yf


def get_aapl_cash_flow():
    """Fetch Apple's annual cash flow statement."""
    ticker = yf.Ticker("AAPL")
    cash_flow = ticker.cashflow
    return cash_flow


if __name__ == "__main__":
    print(get_aapl_cash_flow())
