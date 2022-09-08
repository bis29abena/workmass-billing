from app import app
import numpy as np
import numpy_financial as npf
import pandas as pd
from datetime import date, datetime
import os


def extract_data(filepath, file):
    data_path = os.path.join(filepath, file)
    data = pd.read_excel(io=data_path, sheet_name="Sheet1")

    data["Monthly Installment"] = None
    data["Projected Amount"] = None
    data["Number of Months"] = None

    index_balance = data.columns.get_loc("Balance")
    index_end_date = data.columns.get_loc("Repayment End Date")
    index_monthly_installment = data.columns.get_loc("Monthly Installment")
    index_projected_amount = data.columns.get_loc("Projected Amount")
    index_number_of_months = data.columns.get_loc("Number of Months")


    current_year = date.today().year

    interest_rate = 0.14/12


    for row in range(0, len(data)):
        year_difference = datetime.strptime(str(data.iat[row, index_end_date]), "%Y-%m-%d %H:%M:%S").year - current_year

        if year_difference >= 1:
            data.iat[row, index_number_of_months] = (year_difference * 12)
            data.iat[row, index_monthly_installment] = int(np.around(-npf.pmt(interest_rate, year_difference * 12, data.iat[row, index_balance])))
            data.iat[row, index_projected_amount] = ((year_difference * 12)) * int(np.around(-npf.pmt(interest_rate, year_difference * 12, data.iat[row, index_balance])))
        else:
            if year_difference == 0 or year_difference == -1:
                data.iat[row, index_monthly_installment] = 350
                data.iat[row, index_number_of_months] = 1 + int(np.around(npf.nper(interest_rate, -350, data.iat[row, index_balance])))
                data.iat[row, index_projected_amount] = int(350 * (1 + np.around(npf.nper(interest_rate, -350, data.iat[row, index_balance]))))
            elif year_difference == -2 or year_difference == -3:
                data.iat[row, index_monthly_installment] = 400
                data.iat[row, index_number_of_months] = 1 + int(np.around(npf.nper(interest_rate, -400, data.iat[row, index_balance])))
                data.iat[row, index_projected_amount] = int(400 * (1 + np.around(npf.nper(interest_rate, -400, data.iat[row, index_balance]))))
            else:
                data.iat[row, index_monthly_installment] = 500
                data.iat[row, index_number_of_months] = 1 + int(np.around(npf.nper(interest_rate, -500, data.iat[row, index_balance])))
                data.iat[row, index_projected_amount] = int(500 * (1 + np.around(npf.nper(interest_rate, -500, data.iat[row, index_balance]))))

    save_extract_path = os.path.join(app.config["EXTRACTION_FILE_PATH"], "Extraction.xlsx")

    data.to_excel(f"{save_extract_path}")
    extract_message = "Extraction Done"

    return extract_message
