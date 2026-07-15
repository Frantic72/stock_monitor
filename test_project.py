"""Unit tests for project.py using pytest."""

from unittest.mock import MagicMock, patch
import pytest
import pandas as pd
from project import fetch_stock_price, parse_arguments, send_discord_notification


def test_parse_arguments():
    """Test argument parsing for both successful and error execution paths."""
    # Test valid command line argument parsing
    success_args = [
        "project.py",
        "AAPL",
        "150.50",
        "https://discord.com",
    ]
    ticker, price, url = parse_arguments(success_args)
    assert ticker == "AAPL"
    assert price == 150.50
    assert url == "https://discord.com"

    # Test that an invalid price string causes a system exit
    invalid_args = [
        "project.py",
        "AAPL",
        "not-a-number",
        "https://discord.com",
    ]
    with pytest.raises(SystemExit):
        parse_arguments(invalid_args)


@patch("yfinance.Ticker")
def test_fetch_stock_price(mock_ticker):
    """Test stock price retrieval for successful data and empty inputs."""
    # Test successful yfinance price retrieval using mock data
    mock_instance = MagicMock()
    mock_instance.history.return_value = pd.DataFrame({"Close": [185.00]})
    mock_ticker.return_value = mock_instance
    assert fetch_stock_price("AAPL") == 185.00

    # Test that an empty ticker raises a ValueError
    with pytest.raises(ValueError):
        fetch_stock_price("")


@patch("requests.post")
def test_send_discord_notification(mock_post):
    """Test discord communication layer for valid and unapproved URL formats."""
    # Test successful notification post to Discord webhook
    mock_post.return_value.status_code = 204
    url = "https://discord.com/abc"
    assert send_discord_notification(url, "Test Message") is True

    # Test protection against unapproved webhook URLs
    with pytest.raises(ValueError):
        send_discord_notification("https://invalid-url.com", "Hello")
