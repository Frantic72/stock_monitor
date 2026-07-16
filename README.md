# Stock Alert Monitor CLI

#### Video URL: https://youtu.be/SZk0JEuKkDY

#### Description:
An automated Command-Line Interface (CLI) application built in Python that tracks real-time asset prices via the Yahoo Finance API and dispatches custom trigger notifications directly to Discord channels. 

This application was designed and engineered as a final project for CS50’s Introduction to Programming with Python, focusing on modular structure, rigorous testing, and Clean Code principles.

### Key Components

1. **`project.py`**: The primary executable module containing the application lifecycle:
   - `parse_arguments`: Validates and sanitizes CLI arguments.
   - `fetch_stock_price`: Queries the `yfinance` backend securely.
   - `send_discord_notification`: Connects to external servers using HTTP POST.
   - `main`: Orchestrates user input verification, business evaluation logic, and exception recovery.

2. **`test_project.py`**: Automated test suite powered by `pytest` ensuring 100% test isolation via execution mocks.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com
   cd stock_monitor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Execute the program directly from your shell environment:

```bash
python project.py <TICKER> <TARGET_PRICE> <DISCORD_WEBHOOK_URL>
```

### Example
```bash
python project.py AAPL 190.00 https://discord.com
```

## Quality Control

Run automated validations to confirm script integrity:
```bash
ruff check
pytest
```
