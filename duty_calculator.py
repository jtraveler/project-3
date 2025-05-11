def calculate_landed_cost(structured_data):
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
    print(f"Total Landed Cost: ${landed_cost:.2f}")

    