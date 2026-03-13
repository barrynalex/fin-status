import requests
import os
import hmac
import hashlib
import time
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv

base_url = "https://api.pionex.com"
binance_price_url = "https://api.binance.com/api/v3/ticker/price"

class Pionex:
    def __init__(self):
        load_dotenv()
        self.name = self.__class__.__name__.lower()
        # Preferred env names
        self.api_key = os.getenv("PIONEX_API_KEY")
        self.api_secret = os.getenv("PIONEX_API_SECRET")

        # Backward-compatible fallback to legacy names
        if not self.api_key:
            self.api_key = os.getenv("pionex_userid")
        if not self.api_secret:
            self.api_secret = os.getenv("pionex_password")

        if not self.api_key or not self.api_secret:
            raise ValueError("PIONEX_API_KEY and PIONEX_API_SECRET are required")

    def _generate_signature(self, method: str, path: str, query_string: str = "") -> str:
        # IMPORTANT: path must start with '/', and include '?' before query if present
        method = method.upper()
        if not path.startswith("/"):
            path = "/" + path
        message = f"{method}{path}"
        if query_string:
            message += f"?{query_string}"
        return hmac.new(self.api_secret.encode("utf-8"),
                        message.encode("utf-8"),
                        hashlib.sha256).hexdigest()

    def _make_authenticated_request(self, method: str, endpoint: str, params: dict | None = None):
        if params is None:
            params = {}
        # fresh timestamp in ms
        params["timestamp"] = str(int(time.time() * 1000))
        # URL-encode in the exact order present in params (insertion order is preserved in Py3.7+)
        query_string = urlencode(params)

        signature = self._generate_signature(method, endpoint, query_string)

        headers = {
            "PIONEX-KEY": self.api_key,
            "PIONEX-SIGNATURE": signature,
            # Optional but harmless:
            "Content-Type": "application/json"
        }

        # Build full URL (do not include signature in the query)
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        url = f"{base_url}{endpoint}"
        if query_string:
            url = f"{url}?{query_string}"

        resp = requests.request(method.upper(), url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def _price_usdt(self, coin: str) -> float:
        coin = (coin or "").upper()
        if coin in {"USDT", "USD", "USDC", "BUSD"}:
            return 1.0

        symbol = f"{coin}USDT"
        r = requests.get(binance_price_url, params={"symbol": symbol}, timeout=10)
        if r.status_code != 200:
            return 0.0
        try:
            return float(r.json().get("price", 0))
        except Exception:
            return 0.0

    def get_number(self) -> float:
        data = self._make_authenticated_request("GET", "/api/v1/account/balances")
        ok = (data.get("result") is True) or (data.get("code") == 0)
        if not ok:
            raise Exception(f"API Error: {data.get('message') or data.get('msg') or data}")

        balances = (data.get("data") or {}).get("balances", [])
        total_usd = 0.0

        for b in balances:
            coin = b.get("coin") or b.get("asset") or ""
            free = float(b.get("free", 0))
            frozen = float(b.get("frozen", b.get("locked", 0)))
            qty = free + frozen
            if qty <= 0:
                continue

            px = self._price_usdt(coin)
            total_usd += qty * px

        logging.info(f"pionex total usd={total_usd:.2f}")
        return round(total_usd, 2)


if __name__ == "__main__":
    import logging
    logging.basicConfig( format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO )
    try:
        client = Pionex()
        total = client.get_number()
        print(f"Pionex Total USD: {total}")
        logging.info(f"Successfully retrieved total usd: {total}")
    except Exception as e:
        logging.error(f"Error retrieving balance: {e}")
        print(f"Error: {e}")