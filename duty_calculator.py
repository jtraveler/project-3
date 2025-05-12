


def calculate_landed_cost(structured_data, hs_codes):
    #Intro and setting explaining how it works
    print("\nWelcome to the Import Duty Calculator!")
    print("This calculator assumes you are importing goods INTO the U.S. from another country.")

    #Prompt user input
    print("\nAvailable countries:")
    for entry in structured_data:
        print(".", entry['country_code'])

    valid_country_codes = [entry['country_code'] for entry in structured_data]
    
    #Get origin country
    origin_country = ""
    while origin_country not in valid_country_codes:
        origin_country = input("Enter the ORIGIN country code (e.g DE): ").upper()
        if origin_country.lower() == 'exit':
            print("\nExiting calculator. Goodbye!")
            return
        if origin_country not in valid_country_codes:
            print('\nInvalid code. Please try again or type "exit" to quit')


    #Get destination country
    destination_country = ""
    while destination_country not in valid_country_codes:
        destination_country = input("\nEnter the DESTINATION country code (e.g US): ").upper()
        if destination_country.lower() == 'exit':
            print("\nExiting calculator. Goodbye!")
            return
        if destination_country not in valid_country_codes:
            print('\nInvalid code. Please try again or type "exit" to quit.')

    #Warn and skip if orgin is same as destination
    if origin_country == destination_country:
        print("\nWARNING: Origin and destination country are the same.")
        print("Sorry, this calculator is intended for international imports only.")
        return

    #Load destination country info
    country_info = next(entry for entry in structured_data if entry['country_code'] == destination_country)

    #Print trade route
    print(f"\nRoute: {origin_country} → {destination_country}")

    #Apply FTA (Free Trade Agreement) override if it applies
    if origin_country =='MX' and destination_country == 'US' and country_info.get('fta_eligible', False):
        print("FTA (Free Trade Agreement) applied: Import duty waived.")
        country_info['duty_rate'] = 0.0


    #Ask the user if they want to select an HS code
    use_hs = input("\nWould you like to use a sample HS code to override the duty rate? (yes/no): ").strip().lower()

    if use_hs in ['yes', 'y']:
        print("\nAvailable HS codes:")
        for index, hs in enumerate(hs_codes):
            print(f"{index+1}. {hs['hs_code']} - {hs['description']} ({hs['duty_rate']} rate)")

        #Let user select HS code
        try:
            select_index = int(input("\nEnter the number of the HS code to use (e.g 1): "))
            if 1 <= select_index <= len(hs_codes):
                selected_hs = hs_codes[select_index - 1]  
                country_info['duty_rate'] = float(selected_hs['duty_rate'])
                print(f"Using HS code: {selected_hs['hs_code']} with rate {selected_hs['duty_rate']}")
            else:
                print("That number is not in the list. Continuing with default duty rate.")
        except ValueError:
            print("Invalid HS code selection. Continuing with default duty rate.")  
            
            

    #Numeric input helper
    def get_positive_float(prompt):
        while True:
            try:
                value = float(input(prompt))
                if value < 0:
                    print("\nPlease enter a non-negative number.")
                else:
                    return value
            except ValueError:
                print("\nSorry, you entered invalid input. Please enter a number")


    #Ask for product cost inputs
    product_value = get_positive_float("\nEnter product value (in USD): ")
    shipping_cost = get_positive_float("Enter shipping cost (in USD): ")
    insurance_cost = get_positive_float("Enter insurance cost (in USD): ")


    #Calculating CIF (Cost, Insurance, and Freight)
    cif_total = product_value + shipping_cost + insurance_cost

    import_duty = cif_total * float(country_info['duty_rate'])


    #Calculating MPF (Merchandise Processing Fee )
    mpf_percent = float(country_info['mpf_percent'])
    mpf_min = float(country_info['mpf_min'])
    mpf_max = float(country_info['mpf_max'])
    mpf = max(min(cif_total * mpf_percent, mpf_max), mpf_min)


    #Calculate HMF (Harbor Maintenance Fee)
    harbor_fee_rate = float(country_info['harbor_fee'])
    hmf = cif_total * harbor_fee_rate
    print(f"\nCIF total: ${cif_total:,.2f}")
    print(f"Import Duty: ${import_duty:,.2f}")
    print(f"MPF (Processing Fee): ${mpf:,.2f}")
    print(f"HMF (Harbor Fee): ${hmf:,.2f}")

    #Calculate VAT (Value Added Tax)
    vat_rate = float(country_info['vat_rate'])
    vat = (cif_total + import_duty + mpf + hmf) * vat_rate

    #Calculating landed cost
    landed_cost = cif_total + import_duty + mpf + hmf + vat

    #Print VAT and Total
    print(f"VAT: ${vat:,.2f}")
    print("\n--------------------------------------")
    print(f"\nTotal Landed Cost: ${landed_cost:,.2f}\n")

    