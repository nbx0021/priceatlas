import requests
from datetime import datetime

class ForexEngine:
    _instance = None
    _rates = {}
    _last_updated = None

    def __new__(cls):
        """
        Singleton pattern to ensure we only fetch rates once per session
        to save API bandwidth and improve speed.
        """
        if cls._instance is None:
            cls._instance = super(ForexEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only update if rates are empty or older than 24 hours
        if not self._rates or self._is_cache_stale():
            self.update_rates()

    def _is_cache_stale(self):
        if not self._last_updated:
            return True
        delta = datetime.now() - self._last_updated
        return delta.total_seconds() > 86400  # 24 hours

    def update_rates(self):
        """
        Fetches real-time exchange rates.
        Fulfills 'forex_rates' table requirement in Supabase Schema.
        """
        print("🌍 Syncing Global Forex Rates...")
        try:
            # Using a reliable free API for currency data
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self._rates = data.get('rates', {})
                self._last_updated = datetime.now()
                print(f"✅ Forex Sync Complete: 1 USD = {self._rates.get('INR')} INR")
            else:
                # Fallback rates if API is down
                self._rates = {"INR": 83.5, "USD": 1.0, "EUR": 0.92}
        except Exception as e:
            print(f"⚠️ Forex API Error: {e}. Using static fallback.")
            self._rates = {"INR": 83.5, "USD": 1.0}

    def convert_to_inr(self, amount, from_currency):
        """
        Converts any currency to INR for local market comparison (UC3).
        """
        try:
            if from_currency == "INR":
                return amount
            
            # Logic: Convert from 'source' to USD, then USD to INR
            # (Standard practice for multi-currency engines)
            rate_to_usd = self._rates.get(from_currency, 1.0)
            inr_rate = self._rates.get("INR", 83.5)
            
            usd_value = amount / rate_to_usd
            return round(usd_value * inr_rate, 2)
        except Exception:
            # Emergency fallback: multiply by 83.5 if everything fails
            return round(amount * 83.5, 2) if from_currency == "USD" else amount

    def get_current_rate(self, currency="USD"):
        """Returns the specific rate for the Supabase 'analysis' column"""
        return self._rates.get(currency, 1.0)