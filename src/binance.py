import os
import time
import hmac
import hashlib
import logging
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

BASE_URL = "https://api.binance.com"


class Binance:
    def __init__(self):
        load_dotenv()
        self.name = self.__class__.__name__.lower()
        # Preferred env names
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        # Backward-compatible fallback to legacy names
        if not self.api_key:
            self.api_key = os.getenv("binance_userid")
        if not self.api_secret:
            self.api_secret = os.getenv("binance_password")

        if not self.api_key or not self.api_secret:
            raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET are required in .env")

    def _signed_get(self, path: str, params: dict | None = None):
        params = params or {}
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        url = f"{BASE_URL}{path}?{query}&signature={signature}"
        headers = {"X-MBX-APIKEY": self.api_key}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()

    def _price_usdt(self, asset: str) -> float:
        asset = asset.upper()
        if asset in {"USDT", "USD", "USDC", "BUSD"}:
            return 1.0

        symbol = f"{asset}USDT"
        url = f"{BASE_URL}/api/v3/ticker/price?symbol={symbol}"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return 0.0
        data = r.json()
        try:
            return float(data.get("price", 0))
        except Exception:
            return 0.0

    def get_number(self) -> float:
        account = self._signed_get("/api/v3/account")
        balances = account.get("balances", [])

        total_usd = 0.0
        for b in balances:
            free = float(b.get("free", 0))
            locked = float(b.get("locked", 0))
            qty = free + locked
            if qty <= 0:
                continue

            asset = b.get("asset", "")
            px = self._price_usdt(asset)
            total_usd += qty * px

        logging.info(f"binance total usd={total_usd:.2f}")
        return round(total_usd, 2)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
    c = Binance()
    print(c.get_number())
