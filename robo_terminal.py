import math
import csv
from io import StringIO

# Constants
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

DEATH_PROB = {
    "male": 0.1068,
    "female": 0.0463
}

LIFE_EVENTS = {
    "Married": [0.05, 0.03, 0.02, 0.01, 0.01],
    "Spouse Work": [0.03, 0.03, 0.02, 0.01, 0.01]
}


def estimate_le(age, gender):
    le = 75 if gender.lower() == 'male' else 80
    remaining_years = max(le - age, 0)
    return remaining_years


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


def calculate_retirement_savings(age, gender, income, retirement_age, married, spouse_work, target_amt):
    life_exp = estimate_le(age, gender)
    total_allocation = {asset: 0 for asset in ASSETS["Asset Class"]}

    for year in range(life_exp):
        current_age = age + year
        age_range = get_age_range(current_age)

        if married == "yes":
            if spouse_work == "yes":
                allocation_values = [a + b for a, b in zip(LIFE_EVENTS["Spouse Work"], AGE_ALLOCATIONS[age_range])]
            else:
                allocation_values = [a + b for a, b in zip(LIFE_EVENTS["Married"], AGE_ALLOCATIONS[age_range])]
        else:
            allocation_values = AGE_ALLOCATIONS[age_range]

        for asset, alloc in zip(ASSETS["Asset Class"], allocation_values):
            contribution = income * alloc
            growth_rate = GROWTH_RATES[asset]
            total_allocation[asset] += contribution * (growth_rate ** (life_exp - year))

        if current_age >= retirement_age:
            break

    total_savings = sum(total_allocation.values())
    years_to_target = next((i for i, v in enumerate(total_allocation.values()) if v >= target_amt), None)

    return total_allocation, years_to_target, life_exp


def generate_csv(results):
    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(['Category', 'Value'])
    for key, value in results.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                writer.writerow([f"{key} - {sub_key}", sub_value])
        else:
            writer.writerow([key, value])
    return csv_data.getvalue()


def main():
    print("Welcome to the Retirement Planning Calculator!")

    age = int(input("How old are you? "))
    gender = input("What is your gender? (male/female) ").lower()
    income = float(input("What is your annual income? "))
    retirement_age = int(input("At what age would you like to retire? "))
    target_amt = float(input("What is your retirement savings target? "))
    married = input("Are you married? (yes/no) ").lower()
    spouse_work = "no"
    if married == "yes":
        spouse_work = input("Does your spouse work? (yes/no) ").lower()

    total_allocation, years_to_target, life_expectancy = calculate_retirement_savings(
        age, gender, income, retirement_age, married, spouse_work, target_amt
    )

    total_savings = sum(total_allocation.values())
    years_to_retirement = retirement_age - age

    results = {
        'allocation': {asset: f"${value:,.2f}" for asset, value in total_allocation.items()},
        'total_savings': f"${total_savings:,.2f}",
        'years_to_target': str(years_to_target) if years_to_target is not None else "Not reached",
        'target_amount': f"${target_amt:,.2f}",
        'years_to_retirement': str(years_to_retirement),
        'excess_savings': f"${max(total_savings - target_amt, 0):,.2f}",
        'life_expectancy': life_expectancy + age,
        'remaining_years': life_expectancy
    }

    print("\nRetirement Planning Results:")
    print(f"Life Expectancy: {results['life_expectancy']} years")
    print(f"Remaining Years: {results['remaining_years']} years")
    print(f"Total Retirement Savings: {results['total_savings']}")
    print(f"Years to Reach Target: {results['years_to_target']}")
    print(f"Target Amount: {results['target_amount']}")
    print(f"Years until Retirement: {results['years_to_retirement']}")
    print(f"Excess Savings at Retirement: {results['excess_savings']}")

    print("\nAsset Allocation:")
    for asset, value in results['allocation'].items():
        print(f"{asset}: {value}")

    csv_output = generate_csv(results)
    with open('retirement_plan_results.csv', 'w', newline='') as csvfile:
        csvfile.write(csv_output)
    print("\nResults have been saved to 'retirement_plan_results.csv'")


if __name__ == "__main__":
    main()