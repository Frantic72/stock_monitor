"""CS50P Final Project: Stock Alert Monitor CLI."""

import sys

import requests
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
    
    return float(hist["Close"].iloc[-1])


def send_discord_notification(webhook_url: str, message: str) -> bool:
    """Send an alert message to a Discord channel via Webhook."""
    if not webhook_url.startswith("https://discord.com"):
        raise ValueError("Invalid Discord Webhook URL structure.")
    if not message.strip():
        raise ValueError("Notification message cannot be empty.")
    
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload, timeout=10)
    return response.status_code == 204


def main() -> None:
    """Execute the core application workflow."""
    ticker, target_price, webhook_url = parse_arguments(sys.argv)
    print(f"Fetching latest data for {ticker}...")
    try:
        current_price = fetch_stock_price(ticker)
        print(f"Current Price: ${current_price:.2f} | Target: ${target_price:.2f}")

        if current_price >= target_price:
            msg = (f"🚨 ALERT: {ticker} hit ${current_price:.2f} "
                   f"(Target: ${target_price:.2f})!")
            if send_discord_notification(webhook_url, msg):
                print("Notification sent successfully to Discord!")
        else:
            print("Target price not reached. No alert triggered.")
    except Exception as e:
        print(f"Execution Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
