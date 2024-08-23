# Disease Q&A Healthbot

This repository contains a web-based Q&A chatbot that provides information on various diseases. The chatbot uses Google's Gemini language model for natural language understanding and FAISS for vector-based document retrieval. The chatbot scrapes disease-related data and allows users to ask questions, which are answered based on the context of the scraped data.

![alt text](<Screenshot 2024-08-23 200058.png>)

## Features

- **Disease Information Scraper:** Scrapes information about a disease from online sources.[Mayo Clinic]http://www.mayoclinic.org
- **Q&A Chatbot:** Answers user questions based on the scraped information using a conversational interface.
- **Natural Language Processing:** Utilizes Google's Gemini language model (`gemini-1.5-flash`) for generating responses.
- **Vector-Based Search:** Uses FAISS for efficient document retrieval.
- **User-Friendly Interface:** Built with FastHTML, TailwindCSS, and DaisyUI for a responsive and interactive user experience.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Umang- Bansal/healthbot.git
   cd healthbot

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the required dependencies:**
   ```bash
    pip install -r requirements.txt

4. **Set up environment variables:**
    make a file - constants.py and save
   ```bash
    GOOGLE_API_KEY=your-google-api-key

5. **Run the application:**
   ```bash
    python app.py

6. **Access the application:**
    Open your browser and navigate to http://127.0.0.1:8000.


## Usage

1. Scrape Disease Information:

Enter the name of a disease in the input field and click "Scrape Disease."
The application will fetch information related to the disease and prepare it for Q&A.

2. Ask Questions:

After scraping, you can ask any questions related to the disease.
The chatbot will provide answers based on the context of the scraped data.    

## License
  This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
1. LangChain for providing the core components of the chatbot.
2. Google for the Gemini language model.
3. FAISS for the vector store.
