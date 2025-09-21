def calculate_nigeria_tax(annual_salary, rent=0, pension_rate=8):
    # Step 1: Pension deduction
    pension = (pension_rate / 100) * annual_salary
    income_after_pension = annual_salary - pension
    
    # Step 2: Rent relief (max 500,000)
    rent_relief = min(rent, 500000)
    income_after_rent = income_after_pension - rent_relief
    
    # Step 3: Exemption threshold
    exempt_income = 800000
    taxable_income = income_after_rent - exempt_income
    if taxable_income <= 0:
        return 0, 0  # No tax if below exemption
    
    # Step 4: Apply tax bands
    tax = 0
    if taxable_income <= 2200000:  # 15% band up to 3,000,000 after exemption
        tax = taxable_income * 0.15
    else:
        tax = 2200000 * 0.15 + (taxable_income - 2200000) * 0.18
    
    # Step 5: Annual and Monthly Tax
    annual_tax = round(tax, 2)
    monthly_tax = round(tax / 12, 2)
    
    return annual_tax, monthly_tax


# Example usage:
annual_tax, monthly_tax = calculate_nigeria_tax(annual_salary=3600000, rent=500000, pension_rate=8)
print(f"Annual Tax: ₦{annual_tax}")
print(f"Monthly Tax: ₦{monthly_tax}")
