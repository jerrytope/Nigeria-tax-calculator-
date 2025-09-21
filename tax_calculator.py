import streamlit as st
import pandas as pd

# Nigeria progressive tax bands (2026 structure)
TAX_BANDS = [
    (300000, 0.07),
    (300000, 0.11),
    (500000, 0.15),
    (500000, 0.19),
    (1600000, 0.21),
    (float("inf"), 0.24)
]

def calculate_nigeria_tax(annual_salary, rent=0, pension_rate=8):
    reliefs = []

    # Step 1: Pension deduction
    pension = (pension_rate / 100) * annual_salary
    reliefs.append(["Pension Contribution", f"₦{pension:,.2f}"])

    # Step 2: Rent relief (max 500,000)
    rent_relief = min(rent, 500000)
    reliefs.append(["Rent Relief", f"₦{rent_relief:,.2f}"])

    # Step 3: Consolidated Relief Allowance (CRA)
    cra = max(200000, 0.01 * annual_salary + 0.20 * annual_salary)
    reliefs.append(["Consolidated Relief Allowance (CRA)", f"₦{cra:,.2f}"])

    # Step 4: Total Reliefs
    total_reliefs = pension + rent_relief + cra
    reliefs.append(["Total Reliefs", f"₦{total_reliefs:,.2f}"])

    # Step 5: Taxable Income
    taxable_income = max(annual_salary - total_reliefs, 0)

    # Step 6: Apply tax bands progressively
    tax = 0
    remaining = taxable_income
    tax_rows = []
    for band, rate in TAX_BANDS:
        if remaining <= 0:
            break
        taxable_at_this_band = min(remaining, band)
        band_tax = taxable_at_this_band * rate
        tax += band_tax
        tax_rows.append([
            f"₦{taxable_at_this_band:,.2f}",
            f"{rate*100:.0f}%",
            f"₦{band_tax:,.2f}"
        ])
        remaining -= taxable_at_this_band

    # Step 7: Annual & Monthly Tax
    annual_tax = round(tax, 2)
    monthly_tax = round(tax / 12, 2)

    # Convert to DataFrames
    reliefs_df = pd.DataFrame(reliefs, columns=["Description", "Amount"])
    tax_df = pd.DataFrame(tax_rows, columns=["Taxable Amount", "Rate", "Tax"])

    return annual_tax, monthly_tax, reliefs_df, taxable_income, tax_df


# ==================== STREAMLIT UI ====================

st.title("Nigeria Personal Income Tax Calculator (2026)")
st.write("Calculate annual and monthly tax with clear reliefs and tax bands")

# Inputs
annual_salary = st.number_input("Annual Salary (₦)", min_value=0, value=2400000, step=10000)
rent = st.number_input("Annual Rent (₦)", min_value=0, value=350000, step=10000)
pension_rate = st.number_input("Pension Rate (%)", min_value=0.0, max_value=20.0, value=8.0, step=0.5)

# Calculate Button
if st.button("Calculate Tax"):
    annual_tax, monthly_tax, reliefs_df, taxable_income, tax_df = calculate_nigeria_tax(
        annual_salary, rent, pension_rate
    )

    # Show Results
    st.subheader("Results")
    st.success(f"**Annual Tax:** ₦{annual_tax:,.2f}")
    st.success(f"**Monthly Tax:** ₦{monthly_tax:,.2f}")
    st.info(f"**Taxable Income after Reliefs:** ₦{taxable_income:,.2f}")

    # Show Reliefs
    st.subheader("Reliefs Summary")
    st.table(reliefs_df)

    # Show Tax Breakdown
    st.subheader("Tax Breakdown by Band")
    st.table(tax_df)

    st.markdown(
        "Note: The so-called *first ₦800k tax-free* comes from combining CRA, pension, and rent reliefs. "
        "It’s not a flat exemption but results from total reliefs allowed by law."
    )
