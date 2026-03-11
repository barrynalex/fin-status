import os
import time
import hmac
import hashlib
import logging
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

SPOT_BASE_URL = "https://api.binance.com"
FUTURES_BASE_URL = "https://fapi.binance.com"


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

    def _signed_get(self, path: str, params: dict | None = None, base_url: str = SPOT_BASE_URL):
        params = params or {}
        params["timestamp"] = int(time.time() * 1000)
        query = urlencode(params)
        signature = hmac.new(self.api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
        url = f"{base_url}{path}?{query}&signature={signature}"
        headers = {"X-MBX-APIKEY": self.api_key}
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()

    def _price_usdt(self, asset: str) -> float:
        asset = asset.upper()
        if asset in {"USDT", "USD", "USDC", "BUSD", "FDUSD", "TUSD", "USDP"}:
            return 1.0

        symbol = f"{asset}USDT"
        url = f"{SPOT_BASE_URL}/api/v3/ticker/price?symbol={symbol}"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return 0.0
        data = r.json()
        try:
            return float(data.get("price", 0))
        except Exception:
            return 0.0

    def _spot_balances(self):
        account = self._signed_get("/api/v3/account")
        return account.get("balances", [])

    def _simple_earn_flexible_positions(self):
        rows = []
        page = 1
        size = 100

        while True:
            data = self._signed_get(
                "/sapi/v1/simple-earn/flexible/position",
                {"current": page, "size": size},
                base_url=SPOT_BASE_URL,
            )
            current_rows = data.get("rows", []) or []
            rows.extend(current_rows)

            total = int(data.get("total", len(rows)))
            if len(rows) >= total or not current_rows:
                break
            page += 1

        return rows

    def _futures_balances(self):
        # USDⓈ-M futures wallet balances
        data = self._signed_get("/fapi/v3/balance", base_url=FUTURES_BASE_URL)
        return data if isinstance(data, list) else []

    def get_number(self) -> float:
        spot_assets: dict[str, float] = {}
        simple_earn_assets: dict[str, float] = {}
        futures_assets: dict[str, float] = {}

        # 1) Spot balances
        for b in self._spot_balances():
            free = float(b.get("free", 0))
            locked = float(b.get("locked", 0))
            qty = free + locked
            if qty <= 0:
                continue

            asset = (b.get("asset") or "").upper()
            spot_assets[asset] = spot_assets.get(asset, 0.0) + qty

        # 2) Simple Earn flexible positions
        try:
            positions = self._simple_earn_flexible_positions()
            for p in positions:
                asset = (p.get("asset") or "").upper()
                amount = float(p.get("totalAmount", p.get("total", 0)) or 0)
                if amount <= 0 or not asset:
                    continue
                simple_earn_assets[asset] = simple_earn_assets.get(asset, 0.0) + amount
        except Exception as e:
            logging.warning(f"simple earn fetch failed, continue with spot/futures only: {e}")

        # 3) USDⓈ-M futures wallet balances
        try:
            for b in self._futures_balances():
                asset = (b.get("asset") or "").upper()
                qty = float(b.get("balance", 0) or 0)
                if qty <= 0 or not asset:
                    continue
                futures_assets[asset] = futures_assets.get(asset, 0.0) + qty
        except Exception as e:
            logging.warning(f"futures balance fetch failed, continue with spot/simple earn only: {e}")

        def subtotal_usd(asset_map: dict[str, float]) -> float:
            s = 0.0
            for asset, qty in asset_map.items():
                if qty <= 0:
                    continue
                px = self._price_usdt(asset.replace("LD", ""))
                s += qty * px
            return s

        spot_usd = subtotal_usd(spot_assets)
        simple_earn_usd = subtotal_usd(simple_earn_assets)
        futures_usd = subtotal_usd(futures_assets)
        total_usd = spot_usd + simple_earn_usd + futures_usd

        logging.info(
            "binance breakdown usd | spot=%.2f simple_earn=%.2f futures=%.2f total=%.2f",
            spot_usd,
            simple_earn_usd,
            futures_usd,
            total_usd,
        )

        return round(total_usd, 2)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO)
    c = Binance()
    print(c.get_number())
