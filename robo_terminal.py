import math
# Can be run in the terminal without flask back end

ASSETS = {
    "Asset Class": ["Stocks", "Bonds", "Commodities", "Real Estate", "Cash"],
    "Age Range": ["0-29", "30-39", "40-49", "50-59", "60-69", "70+"]
}

GROWTH_RATES = {
    "Stocks": 1.065,
    "Bonds": 1.03,
    "Commodities": 1.015,
    "Real Estate": 1.025,
    "Cash": 1
}

AGE_ALLOCATIONS = {
    "0-29": [0.2, 0.4, 0.1, 0.1, 0.1],
    "30-39": [0.3, 0.3, 0.2, 0.1, 0.1],
    "40-49": [0.4, 0.2, 0.3, 0.1, 0.1],
    "50-59": [0.5, 0.1, 0.4, 0.1, 0.1],
    "60-69": [0.6, 0.1, 0.3, 0.1, 0.1],
    "70+": [0.7, 0.1, 0.2, 0.1, 0.1]
}

CONTRIBUTION_RATES = {
    "0-29": 0.10,  # 10% of income
    "30-39": 0.15,  # 15% of income
    "40-49": 0.20,  # 20% of income
    "50-59": 0.25,  # 25% of income
    "60-69": 0.30,  # 30% of income
    "70+": 0.30  # 30% of income
}

def get_age_range(age):
    if age < 30:
        return "0-29"
    elif age < 40:
        return "30-39"
    elif age < 50:
        return "40-49"
    elif age < 60:
        return "50-59"
    elif age < 70:
        return "60-69"
    else:
        return "70+"


def calculate_annual_contribution(income, spouse_income, age):
    total_income = income + spouse_income
    age_range = get_age_range(age)
    contribution_rate = CONTRIBUTION_RATES[age_range]
    return total_income * contribution_rate


def calculate_retirement_savings(age, income, retirement_age, married, spouse_income, target_amt):
    total_allocation = {asset: 0 for asset in ASSETS["Asset Class"]}
    years = retirement_age - age
    years_to_target = None
    total_savings = 0

    for year in range(years):
        current_age = age + year
        annual_contribution = calculate_annual_contribution(income, spouse_income, current_age)

        for asset, alloc in zip(ASSETS["Asset Class"], AGE_ALLOCATIONS[get_age_range(current_age)]):
            contribution = annual_contribution * alloc
            growth_rate = GROWTH_RATES[asset]
            total_allocation[asset] += contribution * (growth_rate ** (years - year))

        total_savings = sum(total_allocation.values())
        if total_savings >= target_amt and years_to_target is None:
            years_to_target = year + 1

    return total_allocation, years_to_target


def calculate_years_to_target(current_savings, annual_contribution, target_amount, average_growth_rate):
    if current_savings >= target_amount:
        return 0

    years = 0
    while current_savings < target_amount and years < 100:  # Cap at 100 years to prevent infinite loop
        current_savings = (current_savings + annual_contribution) * average_growth_rate
        years += 1

    return years if years < 100 else "100+"


def get_user_input():
    print("Welcome to the Retirement Planning Calculator!")
    age = int(input("How old are you? "))
    income = int(input("What is your annual income? "))
    retirement_age = int(input("At what age would you like to retire? "))
    target_amt = int(input("What is your retirement savings target? "))
    married = input("Are you married? (yes/no) ").lower() == 'yes'

    spouse_income = 0
    if married:
        spouse_work = input("Does your spouse work? (yes/no) ").lower() == 'yes'
        if spouse_work:
            spouse_income = int(input("What is your spouse's annual income? "))

    return age, income, retirement_age, target_amt, married, spouse_income

def display_results(results):
    print("\nRetirement Planning Results:")
    print(f"Total retirement savings: {results['total_savings']}")
    print(f"Years to reach target: {results['years_to_target']}")
    print(f"Target amount: {results['target_amount']}")
    print(f"Current annual contribution: {results['annual_contribution']}")
    print(f"Years until retirement: {results['years_to_retirement']}")
    print(f"Excess savings at retirement: {results['excess_savings']}")
    print("\nAllocation:")
    for asset, value in results['allocation'].items():
        print(f"  {asset}: {value}")

def main():
    age, income, retirement_age, target_amt, married, spouse_income = get_user_input()

    compound_allocation, years_to_target = calculate_retirement_savings(
        age, income, retirement_age, married, spouse_income, target_amt
    )

    total_savings = sum(compound_allocation.values())
    years_to_retirement = retirement_age - age
    current_annual_contribution = calculate_annual_contribution(income, spouse_income, age)

    results = {
        'allocation': {asset: f"${value:,.2f}" for asset, value in compound_allocation.items()},
        'total_savings': f"${total_savings:,.2f}",
        'years_to_target': years_to_target if years_to_target is not None else "Not reached",
        'target_amount': f"${target_amt:,.2f}",
        'annual_contribution': f"${current_annual_contribution:,.2f}",
        'years_to_retirement': years_to_retirement,
        'excess_savings': f"${max(total_savings - target_amt, 0):,.2f}"
    }

    display_results(results)

if __name__ == "__main__":
    main()