# finance-py
Repository used in graduate level FinTech class using PyCharm IDE

# Retirement Planning Tools

This project includes two retirement planning tools: a Flask-based web application with a chatbot interface and a terminal-based application. Both tools help users calculate retirement savings projections based on their financial information.

## Features

- Interactive chatbot interface (web application)
- Terminal-based interface (command-line application)
- Retirement savings calculation based on user input
- Asset allocation recommendations
- Life expectancy estimation
- Consideration of life events (marriage and spouse's work status)
- Visualization of retirement savings growth
- CSV export of results

## Technologies Used

- Python
- Flask (for web application)
- JavaScript (for web application)
- HTML/CSS (for web application)

## Project Structure

```
Finance/
├── static/
│   ├── js/
│   │   └── main.js
│   └── styles/
│       └── styles.css
├── templates/
│   └── chatbot.html
├── robo.py
├── robo_terminal.py
├── requirements.txt
└── README.md
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/the-berryman/finance-py.git
   cd finance-py
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Web Application (robo.py)

1. Run the Flask application:
   ```
   python robo.py
   ```

2. Open a web browser and navigate to `http://localhost:5000` to use the chatbot.

3. Answer the chatbot's questions about your age, gender, income, retirement goals, etc.

4. The chatbot will calculate and display your projected retirement savings and asset allocation.

5. You can adjust your inputs and recalculate as needed.

### Terminal Application (robo_terminal.py)

1. Run the terminal application:
   ```
   python robo_terminal.py
   ```

2. Follow the prompts to enter your financial information and retirement goals.

3. The application will display your retirement planning results in the terminal and save them to a CSV file.

## New Features in robo_terminal.py

- Life expectancy calculation based on age and gender
- Detailed asset allocation based on age ranges
- Consideration of life events (marriage and spouse's work status) in calculations
- CSV export of results
- Terminal-based interface for easy command-line use

## Contributing

Contributions to improve the retirement planning tools or extend their features are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request


## Acknowledgments

- Flask documentation
- Python financial libraries
- Retirement planning resources