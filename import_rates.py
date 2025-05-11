
import gspread
from google.oauth2.service_account import Credentials


def load_import_data():
    """
    Connecting to Google Sheets and returning structured import data.
    """
    
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]

    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SHEET = GSPREAD_CLIENT.open('code-institute-project3-import_rates')

    country_rates = SHEET.worksheet('imported_rates')

    data = country_rates.get_all_values()


    # Convert sheet data to list dictionaries
    headers = data [0]
    rows = data[1:]

    structured_data = []
    for row in rows:
        country_dict = {}
        for set in range(len(headers)):
            key = headers[set]
            value = row[set]
            #Try converting numbers if possible
            try:
                if value == '':
                    value = 0.0
                elif value not in ['TRUE', 'FALSE']:
                      value = float(value)
            except ValueError:
                pass
            country_dict[key] = value
        structured_data.append(country_dict)
    return structured_data

def load_hs_codes():
    """
    Loads HS code data from the 'hs_codes' tab in the same Google Sheet.
    Returns a list of dictionaries with hs_code, description, and duty_rate.

    """

    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
        ]

    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

    hs_sheet = GSPREAD_CLIENT.open('code-institute-project3-import_rates').worksheet('hs_codes')
    hs_data = hs_sheet.get_all_records()

    return hs_data