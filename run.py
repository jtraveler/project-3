# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high





# Import and load structured country rate data from Google Sheets
from import_rates import load_import_data
from duty_calculator import calculate_landed_cost

#Load structured import rate data from Google Sheets
structured_data = load_import_data()

#Run the main duty/tax calculation flow based on user inputs
while True:
    calculate_landed_cost(structured_data)

    again = input("\nWould you like to calculate another shipment? (yes/no): ").strip()
    if again not in ['yes', 'y']:
        print("Thank for using the Import Duty Calculator. Goodbye!")
        break

