def calculate_landed_cost(structured_data, hs_codes):
    #Prompt user input
    print("\nAvailable countries:")
    for entry in structured_data:
        print(".", entry['country_code'])


    #Select valid country based on the available country codes
    valid_country_codes = [entry['country_code'] for entry in structured_data]

    selected_country = ""

    while selected_country not in valid_country_codes:
        selected_country = input("\nPlease enter a destination country code (e.g. US) ").upper()
        if selected_country.lower() == 'exit':
            print("\nExiting calculator. Goodbye!")
            return
        if selected_country not in valid_country_codes:
            print('\nSorry, that\'s an invalid country code. Please try again or type "exit" to end cycle')


    #Find matching country data
    country_info = next(entry for entry in structured_data if entry['country_code'] == selected_country)



    #Ask the user if they want to select an HS code
    use_hs = input("\nWould you like to use a sample HS code to override the duty rate? (yes/no): ").strip().lower()

    if use_hs in ['yes', 'y']:
        print("\nAvailable HS codes:")
        for index, hs in enumerate(hs_codes):
            print(f"{index+1}. {hs['hs_code']} - {hs['description']} ({hs['duty_rate']} rate)")

        #Let user select HS code
        try:
            select_index = int(input("\nEnter the number of the HS code to use (e.g 1): "))
            selected_hs = hs_codes[selected_index]
            country_info['duty_rate'] = float(selected_hs['duty_rate'])
            print(f"Using HS code: {selected_hs['hs_code']} with rate {selected_hs['duty_rate']}")
        except:
            print("Invalid HS code selection, Continuing with default duty rate.")


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
    print(f"\nCIF total: ${cif_total:.2f}")
    print(f"Import Duty: ${import_duty:.2f}")
    print(f"MPF (Processing Fee): ${mpf:.2f}")
    print(f"HMF (Harbor Fee): ${hmf:.2f}")

    #Calculate VAT (Value Added Tax)
    vat_rate = float(country_info['vat_rate'])
    vat = (cif_total + import_duty + mpf + hmf) * vat_rate

    #Calulating landed cost
    landed_cost = cif_total + import_duty + mpf + hmf + vat

    #Print VAT and Total
    print(f"VAT: ${vat:.2f}")
    print("\n--------------------------------------")
    print(f"\nTotal Landed Cost: ${landed_cost:.2f}\n")

    