const chatBody = document.getElementById('chat-body');
const userInput = document.getElementById('user-input-field');
const sendButton = document.getElementById('send-button');

const questions = [
    "Welcome to the Retirement Planning Bot! Let's start by gathering some information. How old are you?",
    "What is your gender? (male/female)",
    "What is your annual income?",
    "At what age would you like to retire?",
    "What is your retirement savings target?",
    "Are you married? (yes/no)",
    "Does your spouse work? (yes/no)",
    "What is your spouse's annual income?"
];

let currentQuestion = 0;
let userResponses = {};

function addMessage(message, isUser = false) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageElement.textContent = message;
    chatBody.appendChild(messageElement);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function askQuestion() {
    addMessage(questions[currentQuestion]);
}

function processUserInput(input) {
    addMessage(input, true);
    console.log(`User input for question ${currentQuestion}: ${input}`);

    switch (currentQuestion) {
        case 0: userResponses.age = parseInt(input); break;
        case 1: userResponses.gender = input.toLowerCase(); break;
        case 2: userResponses.income = parseFloat(input); break;
        case 3: userResponses.retirement_age = parseInt(input); break;
        case 4: userResponses.target_amt = parseFloat(input); break;
        case 5:
            userResponses.married = input.toLowerCase() === 'yes';
            if (!userResponses.married) {
                calculateRetirement();
                return;
            }
            break;
        case 6:
            userResponses.spouse_work = input.toLowerCase() === 'yes';
            if (!userResponses.spouse_work) {
                calculateRetirement();
                return;
            }
            break;
        case 7:
            userResponses.spouse_income = parseFloat(input);
            calculateRetirement();
            return;
    }

    currentQuestion++;

    if (currentQuestion < questions.length) {
        setTimeout(askQuestion, 1000);
    }
}

function calculateRetirement() {
    addMessage("Thank you for providing all the information. I'm now calculating your retirement plan...");

    console.log("Sending data to server:", userResponses);

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userResponses)
    })
    .then(response => response.json())
    .then(results => {
        console.log("Received results from server:", results);
        if (results.error) {
            throw new Error(results.error);
        }
        displayResults(results);
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage(`I'm sorry, there was an error calculating your retirement plan. Error details: ${error.message}`);
    });
}

function displayResults(results) {
    const messages = [
        `Based on your inputs, here are your retirement planning results:`,
        `Your estimated life expectancy: ${results.life_expectancy} years`,
        `Remaining years (based on life expectancy): ${results.remaining_years} years`,
        `Your total retirement savings: ${results.total_savings}`,
        `Years to reach your target: ${results.years_to_target}`,
        `Your target amount: ${results.target_amount}`,
        `Your current annual contribution: ${results.annual_contribution}`,
        `Years until retirement: ${results.years_to_retirement}`,
        `Excess savings at retirement: ${results.excess_savings}`,
        `Here's how your savings are allocated:`,
        ...Object.entries(results.allocation).map(([asset, value]) => `${asset}: ${value}`)
    ];

    function typeWriter(index = 0) {
        if (index < messages.length) {
            addMessage(messages[index]);
            setTimeout(() => typeWriter(index + 1), 1000);
        } else {
            const downloadButton = document.createElement('button');
            downloadButton.textContent = 'Download Results as CSV';
            downloadButton.onclick = () => window.location.href = '/download-csv';
            downloadButton.className = 'download-button';
            chatBody.appendChild(downloadButton);
        }
    }

    typeWriter();
}

sendButton.addEventListener('click', () => {
    const input = userInput.value.trim();
    if (input) {
        processUserInput(input);
        userInput.value = '';
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});

// Start the conversation
askQuestion();