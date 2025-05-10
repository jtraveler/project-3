# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

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

print(data)

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
            value = float(value) if value not in ['TRUE', 'FALSE'] else value
        except ValueError:
            pass
        country_dict[key] = value
    structured_data.append(country_dict)

#Prompt user input
print("Available countries:")
for entry in structured_data:
    print(".", entry['country_code'])

selected_country = input("Please enter destination country code (e.g. US): ").upper()

#Find matching country
country_info = None
for entry in structured_data:
    if entry['country_code'] == selected_country:
        country_info = entry
        break
if not country_info:
    print("Sorry, country not found in the sheet.")
    exit()

#Ask for product cost inputs
product_value = float(input("Enter product value (in USD): "))
shipping_cost = float(input("Enter shipping cost (in USD): "))
insurance_cost = float(input("Enter insurance cost (in USD): "))

#Calculating CIF (Cost, Insurance, and Freight)
cif_total = product_value + shipping_cost + insurance_cost

import_duty = cif_total * country_info['duty']

print(f"\n CIF Total: ${cif_total:.2f}")
print(f"\n Import Duty: ${cif_duty:.2f}")
          
