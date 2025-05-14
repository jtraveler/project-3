# Numeric input helper
def get_positive_float(prompt):
    """
    Prompt for a non-negative numeric input.
    Repeats until the user provides valid float input ≥ 0.
    """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            print("\n👋  Exiting calculator. Goodbye!")
            return None
        try:
            value = float(user_input)
            if value < 0:
                print("\nPlease enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("\nInvalid input. Please enter a number.")


def calculate_landed_cost(structured_data, hs_codes):
    """
    Calculates total landed cost for an international shipment.

    Includes CIF, import duty, MPF, HMF, VAT, and supports FTA logic
    and optional HS code overrides.
    """
    print("\n👋  Welcome to the Import Duty Calculator!")
    print("📦  Please note that this tool is for U.S. imports only.")
    print('💡  Type "exit" at any prompt to leave the calculator.')

    # Prompt user input
    print("\n🌍  Available countries:")
    for entry in structured_data:
        print(".", entry['country_code'])

    valid_country_codes = [entry['country_code'] for entry in structured_data]

    # Get origin country
    origin_country = ""
    while origin_country not in valid_country_codes:
        origin_country = input("\n🏁 Origin country code (e.g. DE): ").upper()
        if origin_country.lower() == 'exit':
            print("\n👋 Exiting calculator. Goodbye!\n")
            return
        if origin_country not in valid_country_codes:
            print('\nInvalid code. Please try again or type "exit" to quit')

    # Get destination country
    destination_country = ""
    while destination_country not in valid_country_codes:
        destination_country = input(
            "\n🎯 Destination country code (e.g US): ").upper()
        if destination_country.lower() == 'exit':
            print("\n👋  Exiting calculator. Goodbye!")
            return
        if destination_country not in valid_country_codes:
            print('\nInvalid code. Please try again or type "exit" to quit.')

    # Warn and skip if origin is same as destination
    if origin_country == destination_country:
        print("\n⚠️  WARNING: Origin and destination country are the same.")
        print(
            "Sorry, this tool is for international imports only.")
        return

    # Load destination country info
    country_info = next(entry for entry in structured_data if entry[
        'country_code'] == destination_country)

    # Print trade route
    print(f"\nRoute: {origin_country} → {destination_country}")

    # Apply FTA (Free Trade Agreement) override if it applies
    is_mx_to_us = (
        origin_country == 'MX' and
        destination_country == 'US' and
        country_info.get('fta_eligible', False)
    )

    if is_mx_to_us:
        print("✅  FTA (Free Trade Agreement) applied: Import duty waived.")
        country_info['duty_rate'] = 0.0

    # Ask the user if they want to select an HS code
    hs_prompt = (
        "\n📦  Would you like to use a sample HS code to "
        "override the duty rate? (yes/no): "
    )
    use_hs = input(hs_prompt).strip().lower()
    if use_hs == 'exit':
        print("\n👋 Exiting calculator. Goodbye!")
        return
    elif use_hs in ['no', 'n']:
        print("\nℹ️ Continuing without HS code override.")

    elif use_hs in ['yes', 'y', 'ok', 'sure']:
        print("\nAvailable HS codes to use:")
        for index, hs in enumerate(hs_codes):
            desc = hs['description']
            code = hs['hs_code']
            rate = hs['duty_rate']
            print(f"{index+1}. {code} - {desc} ({rate} rate)")

        # Let user select HS code
        try:
            select_index = input(
                "\nHS code number (e.g. 1 or type 'exit'): "
                ).strip()
            if select_index.lower() == 'exit':
                print("\n👋 Exiting calculator. Goodbye!")
                return
            select_index = int(select_index)
            if 1 <= select_index <= len(hs_codes):
                selected_hs = hs_codes[select_index - 1]
                country_info['duty_rate'] = float(selected_hs['duty_rate'])
                code = selected_hs['hs_code']
                rate = selected_hs['duty_rate']
                print(f"Using HS code: {code} with rate {rate}")
            else:
                print("Number not in list. Default duty rate will be used.")
        except ValueError:
            print(
                "Invalid selection. Using default duty rate.")

    else:
        print("\nUnrecognized response. Proceeding without HS override.")

    # Ask for product cost inputs
    product_value = get_positive_float("\n💰 Enter product value (in USD): ")
    if product_value is None:
        return
    shipping_cost = get_positive_float("🚢 Enter shipping cost (in USD): ")
    if shipping_cost is None:
        return
    insurance_cost = get_positive_float("🛡️ Enter insurance cost (in USD): ")
    if insurance_cost is None:
        return

    # Calculating CIF (Cost of product + Insurance + Freight)
    cif_total = product_value + shipping_cost + insurance_cost

    import_duty = cif_total * float(country_info['duty_rate'])

    # Calculating MPF (Merchandise Processing Fee) with min/max limits
    mpf_percent = float(country_info['mpf_percent'])
    mpf_min = float(country_info['mpf_min'])
    mpf_max = float(country_info['mpf_max'])
    mpf = max(min(cif_total * mpf_percent, mpf_max), mpf_min)

    # Calculate HMF (Harbor Maintenance Fee) as a percentage of CIF
    harbor_fee_rate = float(country_info['harbor_fee'])
    hmf = cif_total * harbor_fee_rate
    print(f"\n📊  CIF total: ${cif_total:,.2f}")
    print(f"💵  Import Duty: ${import_duty:,.2f}")
    print(f"📦  MPF (Processing Fee): ${mpf:,.2f}")
    print(f"⚓ HMF (Harbor Fee): ${hmf:,.2f}")

    # Calculate VAT (Value Added Tax) as:
    # ((CIF + duty + fees) × vat_rate)
    vat_rate = float(country_info['vat_rate'])
    vat = (cif_total + import_duty + mpf + hmf) * vat_rate

    # Calculating landed cost as:
    # sum of all above (CIF + Duty + MPF + HMF + VAT)
    landed_cost = cif_total + import_duty + mpf + hmf + vat

    # Print VAT and Total
    print(f"🧾  VAT: ${vat:,.2f}")
    separator = "\n" + "-" * 38
    print(separator)
    print(f"\n✅  Total Landed Cost: ${landed_cost:,.2f}\n")
