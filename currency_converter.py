"""
Currency Converter with Live Exchange Rates
Uses exchangerate-api.com free API for real-time rates

Example output:
    100.00 USD = 92.45 EUR
    Exchange rate: 1 USD = 0.9245 EUR
"""

import requests
from typing import Optional


def get_exchange_rate(base: str, target: str) -> Optional[float]:
    """Fetch live exchange rate between two currencies."""
    url = f"https://api.exchangerate-api.com/v4/latest/{base.upper()}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        rates = response.json()['rates']
        return rates.get(target.upper())
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
    except KeyError:
        print("Invalid currency code or API response format changed")
        return None


def convert_currency(amount: float, base: str, target: str) -> Optional[float]:
    """Convert amount from base currency to target currency."""
    rate = get_exchange_rate(base, target)
    return amount * rate if rate else None


def main():
    print("=" * 50)
    print("Currency Converter (Live Rates)")
    print("=" * 50)

    amount = float(input("\nEnter amount: "))
    base = input("From currency (e.g., USD): ").strip()
    target = input("To currency (e.g., EUR): ").strip()

    result = convert_currency(amount, base, target)

    if result:
        print(f"\n{amount:.2f} {base.upper()} = {result:.2f} {target.upper()}")
        rate = get_exchange_rate(base, target)
        print(f"Exchange rate: 1 {base.upper()} = {rate:.4f} {target.upper()}")
    else:
        print("\nError: Could not fetch exchange rate. Check currency codes.")


if __name__ == "__main__":
    main()