# 📦 Import Duty Calculator

[Live Site on Heroku](https://project-3-0d23a0350b7d.herokuapp.com/)  
This project was built with Python3 as the **"Python's Essentials" Project (Portfolio Project 3)** for [Code Institute](https://codeinstitute.net/).

![Responsive Preview](insert-your-screenshot-url-here)

---

## 📖 Table of Contents
- [Overview](#overview)
- [User Story](#user-story)
- [Planning](#planning)
- [User Flow](#user-flow)
- [Features](#features)
- [Calculator Math](#calculator-math)
- [Disclaimer](#disclaimer)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

---

## 🧭 Overview

Calculating import duty, tax, and tariff fees is often more frustrating than it should be. Rates change based on trade policies, political events, and new legislation. Data may be outdated, hard to find, or the existing calculators overly complex.

That’s why I built the **Import Duty Calculator** — a user-friendly terminal app that pulls dynamic values from **Google Sheets** so rates can be updated easily without modifying code. It’s designed to be:

- **Helpful**: Explains results clearly
- **Accessible**: No need for users to understand complex formulas
- **Up-to-date**: Powered by live spreadsheet data

---

## 👤 User Story

 *Picture this: You're running a U.S.-based business that imports LED displays from China. While watching the news, you hear the President announce new tariffs on electronics from several countries. You panic — how much more will your next shipment cost? How do you plan, budget, or quote customers confidently?*  
 
 **This calculator steps in to provide clarity**. With just a few prompts, it calculates your total landed cost, including CIF, Duty, MPF, HMF, and VAT — and even flags whether a Free Trade Agreement might reduce your fees.

---

## 📋 Planning and Research

To push this idea forward, I had to dive into the planning and research phase to gain a better understanding on the calculation formulas and duty fee terminolog. Luckily I was able to get help with using the Perpexity tool, which made my job much easier with gathering the information I needed. Therfore, with my research I was able to get the information for gathering the calculator math from the following references:

[U.S. Customs and Border Protection](https://www.cbp.gov/trade/basic-import-export/importer-exporter-tips)

[HTS.USITC.gov](https://hts.usitc.gov/)

---

## 🧮 Calculator Math

The calculator uses the following key formulas:

| Calculation       | Formula |
|------------------|---------|
| **CIF (Cost, Insurance, Freight)** | `CIF = product value + shipping cost + insurance` |
| **Import Duty**   | `Import Duty = CIF × duty_rate` |
| **MPF (Merchandise Processing Fee)** | `MPF = max(min(CIF × mpf_rate, mpf_max), mpf_min)` |
| **HMF (Harbor Maintenance Fee)** | `HMF = CIF × harbor_fee` |
| **VAT**           | `VAT = (CIF + Import Duty + MPF + HMF) × vat_rate` |
| **Total Landed Cost** | `Landed Cost = CIF + Import Duty + MPF + HMF + VAT` |


## ⚠️ Disclaimer

This calculator is a **demo/prototype** and is intended for **testing purposes only**. Therfore the rates may not be current.  
- Duty rates, VAT, MPF, and HMF values are not guaranteed to be up-to-date.
- Data is manually managed via Google Sheets and may not reflect current U.S. Customs or international rates.
- Links to official sources: [U.S. Customs and Border Protection](https://www.cbp.gov/trade/basic-import-export/importer-exporter-tips) and [HTS.USITC.gov](https://hts.usitc.gov) for authoritative import fees and regulations.


### ℹ️ Assumptions

- This calculator uses **flat percentage rates** for import duty, VAT, MPF, and HMF.
- It assumes **CIF valuation method** (Cost + Insurance + Freight).
- HS code overrides and FTA eligibility logic are simplified and only apply to specific hard-coded conditions.
- The Merchandise Processing Fee (MPF) uses a capped min/max formula.


### ⚙️ How Rates Are Applied

| Component | Trigger Logic |
|----------|----------------|
| **FTA (Free Trade Agreement)** | If origin is `MX` and destination is `US`, and `fta_eligible` is `TRUE`, then duty rate is set to `0.0`. |
| **HS Code Override** | If user opts to select an HS code, its duty rate overrides the default country rate. |
| **VAT** | Applied to the total value `(CIF + Duty + MPF + HMF) × VAT Rate`, if a non-zero VAT rate exists. |
| **MPF** | Applies to all U.S. imports using `min(max(CIF × rate, min), max)` formula. |
| **HMF** | Only applied if destination country includes a non-zero `harbor_fee` in the data sheet. |


## ❗ Demo Limitations

This calculator is currently a **simplified proof-of-concept** and includes the following known limitations:

- ✅ Only **3 countries** supported: United States (US), Germany (DE), and Mexico (MX).
- ✅ Only **3 sample HS codes** are available for duty overrides.
- ❌ Does not support tiered or compound duty logic (e.g. per-item fees).
- ❌ No currency conversion — all values are assumed to be in USD.
- ❌ Does not distinguish between product categories (e.g. apparel vs. electronics) beyond the provided samples.
- ❌ Does not check whether HMF or VAT applies based on product type or transport mode.
- ⚠️ FTA logic is hardcoded only for **MX → US** scenario.


---

## 📊 Sample Data

This calculator pulls its rates dynamically from an external [Google Sheet](https://docs.google.com/spreadsheets/d/1fKBxT4pJ79_vV1g2D00qnVRt39NgiDhrEzw0EjH4uoM/edit?usp=sharing) to allow easy updating of duty, tax, and fee values without modifying the source code.

The demo version uses a simplified dataset containing three countries and three HS (Harmonized System) product codes.

---

### 🌎 Sample Country Codes

Each country entry includes fields for value-added tax (VAT), merchandise processing fee (MPF), harbor maintenance fee (HMF), currency, and whether the country qualifies for free trade agreement (FTA) exemptions.

| Country Code | VAT Rate | MPF %    | MPF Min | MPF Max | Harbor Fee | Currency | Duty Rate | FTA Eligible |
|--------------|----------|----------|---------|---------|------------|----------|-----------|--------------|
| US           | 0        | 0.00346  | 31.67   | 614.35  | 0.00125     | USD      | 0.08      | TRUE         |
| DE           | 0.19     | 0        | 0       | 0       | 0           | EUR      | 0.04      | TRUE         |
| MX           | 0.16     | 0        | 0       | 0       | 0           | MXN      | 0.08      | TRUE         |





### 📦 Sample Products (HS Codes)

This table contains mock Harmonized System codes (HS codes) used to simulate how duty rates change by product category.

| HS Code      | Description         | Duty Rate |
|--------------|---------------------|------------|
| 4202.31.6000 | Leather Wallets     | 0.08       |
| 6109.10.0012 | Cotton T-Shirts     | 0.165      |
| 8528.72.6400 | LED Displays        | 0.026      |



---

## 🔀 Flowchart

The logic of this program is summarized in the following diagram:

![Flowchart of Program](insert-your-flowchart-url-here)

---

## 🧩 Features

### ✅ Core Functionality
- User selects **origin and destination country codes**
- Prompts for product value, shipping, insurance
- Calculates:
  - CIF
  - Import Duty
  - MPF (with min/max bounds)
  - HMF
  - VAT
  - Total Landed Cost
- Optionally overrides the duty rate using an **HS code**
- Checks for **FTA exemptions** (e.g., Mexico → US)

### 📊 Google Sheets Integration
- Imports `duty_rate`, `mpf_min`, `vat_rate`, etc. from a live Google Sheet
- Easily updated by non-technical users

---

## 📦 Example Output

```bash
Welcome to the Import Duty Calculator!
This calculator assumes you're importing into the U.S. from abroad.

Available countries:
. US
. DE
. MX

Origin country code (e.g. DE): MX
DESTINATION country code (e.g US): US

Route: MX → US
FTA (Free Trade Agreement) applied: Import duty waived.
