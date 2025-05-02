import gspread
from datetime import datetime
import logging
from cathey import Cathey
from esun import Esun
from ctbc import Ctbc
from ipost import Ipost



bank_list = [Esun, Ctbc, Ipost]

def main():
    data = {}
    for bank in bank_list:
        print(bank)
        client = bank()
        data[client.name] = client.get_number()

    # write to google sheet
    client = gspread.service_account(filename="token.json")
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1dF1XOF0PEs27cII03F6QRnuqf78umW8eGdUs7eD2X_g/edit?usp=sharing")
    worksheet = sheet.get_worksheet(0)
    new_data = [datetime.now().year, datetime.now().month, data["esun"], 10000, data['ipost'], data['ctbc']]
    worksheet.append_row(new_data, value_input_option='USER_ENTERED')

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    main()
