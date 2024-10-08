import math
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


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

LIFE_EVENTS = {
    "Married": [0.05, 0.03, 0.02, 0.01, 0.01],
    "Spouse Income": [0.03, 0.03, 0.02, 0.01, 0.01]
}

def get_user_inputs():
    age = int(input("How old are you? "))
    income = int(input("What is your income? "))
    retirement_age = int(input("At what age would you like to retire? "))
    married = input("Are you married? ").lower() == "yes"
    spouse_income = 0
    if married:
        spouse_work = input("Does your spouse work? ").lower() == "yes"
        if spouse_work:
            spouse_income = int(input("What is your spouse's income? "))
    target_amt = int(input("What is your retirement savings target? "))

    return age, income, retirement_age, married, spouse_income, target_amt


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


def calculate_allocation(age, income, married, spouse_income):
    age_range = get_age_range(age)
    base_allocation = AGE_ALLOCATIONS[age_range]

    if married:
        if spouse_income > 0:
            adjustment = LIFE_EVENTS["Spouse Income"]
        else:
            adjustment = LIFE_EVENTS["Married"]
        allocation = [a + b for a, b in zip(base_allocation, adjustment)]
    else:
        allocation = base_allocation

    return [(asset, alloc * income) for asset, alloc in zip(ASSETS["Asset Class"], allocation)]


def calculate_retirement_savings(age, income, retirement_age, married, spouse_income):
    total_allocation = {asset: 0 for asset in ASSETS["Asset Class"]}
    years = retirement_age - age

    for year in range(years):
        current_age = age + year
        allocation = calculate_allocation(current_age, income, married, spouse_income)

        for asset, amount in allocation:
            total_allocation[asset] += amount

        if year == 0 or (year + 1) % 10 == 0:
            print(f"\nAllocation at age {current_age}:")
            for asset, amount in allocation:
                print(f"{asset}: ${amount:,.2f} per year")

    compound_allocation = {
        asset: round(amount * (GROWTH_RATES[asset] ** years), 2)
        for asset, amount in total_allocation.items()
    }

    return compound_allocation

def calculate_years_to_target(current_savings, annual_contribution, target_amount, average_growth_rate):
    return math.ceil(math.log(target_amount / (current_savings * average_growth_rate + annual_contribution) + 1) /
                     math.log(average_growth_rate))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        age = int(request.form['age'])
        income = int(request.form['income'])
        retirement_age = int(request.form['retirement_age'])
        married = request.form['married'] == 'yes'

        # Handle spouse income more carefully
        spouse_income = 0
        if married:
            spouse_work = request.form.get('spouse_work') == 'yes'
            if spouse_work:
                spouse_income_str = request.form.get('spouse_income', '')
                spouse_income = int(spouse_income_str) if spouse_income_str else 0

        target_amt = int(request.form['target_amt'])

        compound_allocation = calculate_retirement_savings(age, income, retirement_age, married, spouse_income)

        total_savings = sum(compound_allocation.values())
        years_to_retirement = retirement_age - age
        average_annual_contribution = total_savings / years_to_retirement
        average_growth_rate = sum(GROWTH_RATES.values()) / len(GROWTH_RATES)

        years_to_target = calculate_years_to_target(total_savings, average_annual_contribution, target_amt,
                                                    average_growth_rate)

        results = {
            'allocation': {asset: f"${value:,.2f}" for asset, value in compound_allocation.items()},
            'total_savings': f"${total_savings:,.2f}",
            'years_to_target': years_to_target,
            'target_amount': f"${target_amt:,.2f}"
        }

        return jsonify(results)
    except ValueError as e:
        return jsonify(
            {'error': f'Invalid input. Please ensure all fields are filled with valid numbers. Details: {str(e)}'}), 400


if __name__ == "__main__":
    app.run(debug=True)