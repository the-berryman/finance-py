# finance-py
Repository used in graduate level FinTech class using PyCharm IDE

# Retirement Planning Chatbot

This project is a Flask-based web application that provides a chatbot interface for retirement planning. Users can input their financial information, and the chatbot will calculate and display retirement savings projections.

## Features

- Interactive chatbot interface
- Retirement savings calculation based on user input
- Asset allocation recommendations
- Visualization of retirement savings growth

## Technologies Used

- Python
- Flask
- JavaScript
- HTML/CSS

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
└── README.md
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/finance-py.git
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

4. Run the Flask application:
   ```
   python robo.py
   ```

5. Open a web browser and navigate to `http://localhost:5000` to use the chatbot.

## Usage

1. Open the chatbot interface in your web browser.
2. Answer the chatbot's questions about your age, income, retirement goals, etc.
3. The chatbot will calculate and display your projected retirement savings and asset allocation.
4. You can adjust your inputs and recalculate as needed.

## Contributing

Contributions to improve the chatbot or extend its features are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Flask documentation
- Python financial libraries
- Retirement planning resources