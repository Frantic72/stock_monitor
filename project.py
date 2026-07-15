"""CS50P Final Project: Stock Alert Monitor CLI."""

import sys
import yfinance as yf


def parse_arguments(args: list[str]) -> tuple[str, float, str]:
    """Parse and validate command line arguments.

    Expects format: project.py <TICKER> <TARGET_PRICE> <DISCORD_WEBHOOK>
    """
    if len(args) != 4:
        print("Usage: python project.py <TICKER> <TARGET_PRICE> <WEBHOOK_URL>")
        sys.exit(1)

    ticker = args[1].strip().upper()
    try:
        target_price = float(args[2])
    except ValueError:
        print("Error: Target price must be a valid number.")
        sys.exit(1)

    webhook_url = args[3].strip()
    return ticker, target_price, webhook_url


def fetch_stock_price(ticker: str) -> float:
    """Fetch the latest closing price for a given stock ticker via yfinance."""
    if not ticker:
        raise ValueError("Ticker symbol cannot be empty.")
    
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    if hist.empty:
        raise ValueError(f"No stock data found for ticker: {ticker}")
    
    print(f"Latest price: {hist['Close'].iloc[-1]}")


def main() -> None:
    """Execute the core application workflow."""
    ticker, target_price, webhook_url = parse_arguments(sys.argv)
    print(f"ticker: {ticker}")
    print(f"target_price: {target_price}")
    print(f"webhook_url: {webhook_url}")

    print(f"Fetching latest data for {ticker}...")
    try:
        current_price = fetch_stock_price(ticker)
    except Exception as e:
        print(f"Execution Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
