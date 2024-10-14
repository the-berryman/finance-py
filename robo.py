import math
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')


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
    "0-29": [0.4, 0.1, 0.1, 0.3, 0.1],
    "30-39": [0.4, 0.1, 0.1, 0.2, 0.2],
    "40-49": [0.3, 0.2, 0.2, 0.1, 0.2],
    "50-59": [0.1, 0.3, 0.3, 0.1, 0.2],
    "60-69": [0, 0.6, 0.2, 0, 0.2],
    "70+": [0, 0.7, 0, 0, 0.3]
}

LIFE_EVENTS = {
    "Married": [0.05, 0.03, 0.02, 0.01, 0.01],
    "Spouse Income": [0.03, 0.03, 0.02, 0.01, 0.01]
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


@app.route('/')
def index():
    return render_template('chatbot.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        app.logger.debug(f"Received data: {data}")  # Log received data

        age = int(data['age'])
        income = int(data['income'])
        retirement_age = int(data['retirement_age'])
        target_amt = int(data['target_amt'])
        married = data.get('married', False)

        spouse_income = 0
        if married:
            spouse_work = data.get('spouse_work', False)
            if spouse_work:
                spouse_income = int(data.get('spouse_income', 0))

        app.logger.debug(f"Processed inputs: age={age}, income={income}, retirement_age={retirement_age}, "
                         f"target_amt={target_amt}, married={married}, spouse_income={spouse_income}")

        compound_allocation, years_to_target = calculate_retirement_savings(age, income, retirement_age, married,
                                                                            spouse_income, target_amt)

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

        app.logger.debug(f"Calculation results: {results}")  # Log results

        return jsonify(results)
    except Exception as e:
        app.logger.error(f"Error in calculate: {str(e)}", exc_info=True)  # Log the full exception
        return jsonify({'error': f'An error occurred: {str(e)}. Please try again.'}), 400

if __name__ == "__main__":
    app.run(debug=True)