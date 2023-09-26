# HealthBot - Your Health Information Chatbot


## Overview

HealthBot is a Python-based chatbot that provides health-related information to users. It utilizes the Twilio API for messaging and OpenAI's GPT-3.5 model for natural language understanding.

## Features

- **Disease Information:** Users can ask for information about various diseases.
- **Interactive Chat:** Engage in interactive conversations with the chatbot.
- **Persistent Sessions:** Store chat history for each user session.
- **Data Scraping:** Retrieve disease information from Mayo Clinic's website.
 - Web scraper that scrapes the diseases and conditions of [Mayo Clinic]http://www.mayoclinic.org).





## Setup and Usage

### Installation
- Install dependencies:
    ```pip install -r requirements.txt```

- Set up environment variables for Twilio and OpenAI API keys.

- Start the Flask application:
    ```python app.py```

- Use Ngrok for local development (if necessary):
    ```ngrok http 5000```


### Usage
- Send a WhatsApp message to your Twilio phone number to initiate a chat session.

- You can ask for disease information, get help, and end the chat using commands like "help," "quit," or "exit."

- The chatbot will respond with relevant health information.


