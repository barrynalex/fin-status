import requests
import os
import hmac
import hashlib
import time
from urllib.parse import urlencode
from bank import Bank

base_url = "https://api.pionex.com"

class Pionex(Bank):
    def __init__(self):
        self.name = self.__class__.__name__.lower()
        self.api_key = os.getenv("pionex_userid")
        self.api_secret = os.getenv("pionex_password")
        if not self.api_key or not self.api_secret:
            raise ValueError("PI_API_KEY and PI_API_SECRET environment variables are required")

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

    def get_balance(self):
        data = self._make_authenticated_request("GET", "/api/v1/account/balances")
        # Success shape per docs: {"result": true, "data": {"balances": [...]}}
        # Some deployments use {"code":0}. Handle both.
        ok = (data.get("result") is True) or (data.get("code") == 0)
        if not ok:
            raise Exception(f"API Error: {data.get('message') or data.get('msg') or data}")
        balances = (data.get("data") or {}).get("balances", [])
        parts = []
        for b in balances:
            # fields seen in docs: coin/free/frozen; sometimes asset/locked
            coin = b.get("coin") or b.get("asset") or ""
            free = float(b.get("free", 0))
            frozen = float(b.get("frozen", b.get("locked", 0)))
            total = free + frozen
            if total > 0:
                parts.append(f"{coin}: {total}")
        return " | ".join(parts) if parts else "No balance found"


if __name__ == "__main__":
    import logging
    logging.basicConfig( format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO )
    try:
        client = Pionex()
        balance = client.get_balance()
        print(f"Pionex Balance: {balance}")
        logging.info(f"Successfully retrieved balance: {balance}")
    except Exception as e:
        logging.error(f"Error retrieving balance: {e}")
        print(f"Error: {e}")