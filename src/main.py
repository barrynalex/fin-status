import gspread
from datetime import datetime
import logging
from cathey import Cathey
from esun import Esun
from ctbc import Ctbc
from ipost import Ipost
from pionex import Pionex
from binance import Binance

bank_list = [Esun, Ctbc, Ipost, Cathey, Pionex, Binance]

def main():
    data = {}
    for bank in bank_list:
        print(bank)
        try:
            client = bank()
            data[client.name] = client.get_number()
        except Exception as e:
            logging.exception(f"{bank.__name__} failed: {e}")
            data[bank.__name__.lower()] = 0

    # write to google sheet
    client = gspread.service_account(filename="token.json")
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1dF1XOF0PEs27cII03F6QRnuqf78umW8eGdUs7eD2X_g/edit?usp=sharing")
    worksheet = sheet.get_worksheet(0)
    new_data = [
        datetime.now().year,
        datetime.now().month,
        data.get("esun", 0),
        10000,
        data.get('ipost', 0),
        data.get('ctbc', 0),
        data.get('cathey', 0),
        data.get('pionex', 0),
        data.get('binance', 0),
    ]
    worksheet.append_row(new_data, value_input_option='USER_ENTERED')

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    main()
