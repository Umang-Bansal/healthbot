from flask import Flask, request, jsonify, session
from twilio.twiml.messaging_response import Message, MessagingResponse
import openai
import os
from twilio.rest import Client
from flask_ngrok import run_with_ngrok
from bs4 import BeautifulSoup
import requests
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
import constants
import sys

app = Flask(__name__)
app.secret_key = os.urandom(24)
run_with_ngrok(app)

os.environ["OPENAI_API_KEY"] = constants.APIKEY
os.environ['TWILIO_ACCOUNT_SID'] = constants.account_sid
os.environ['TWILIO_AUTH_TOKEN'] = constants.auth_token

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
openai.api_key = os.environ["OPENAI_API_KEY"]

def scrape_data(disease_name):
    disease = disease_name
    letter = disease[0]

    html_text = requests.get('https://www.mayoclinic.org/diseases-conditions/index?letter={}'.format(letter)).text

    soup = BeautifulSoup(html_text, 'lxml')
    data = soup.find('div', class_ = 'cmp-back-to-top-container__children')
    contents = data.find_all('div', class_='cmp-link', attrs={'data-testid': 'cmp-button'})

    disease_url = None
    for content in contents:
        if  content.text.lower() == disease.lower():
            disease_url = content.find('a')['href']
            break

    if disease_url:    
        html_text2 = requests.get(disease_url).text
        soup2 = BeautifulSoup(html_text2, 'lxml')

        try:
            data2 = soup2.find('div', class_ = 'content')
            content2 = data2.find('div', class_ = False)
            information = content2.find_all(['p', 'ul', 'h2', 'h3', 'h4'], class_ = False, id = False)
        except AttributeError:
            data2 = soup2.find('div', class_ = 'container-child container-child cmp-column-control__content-column')
            content2 = data2.find('article', attrs={'data-testid': 'cmp-article'})
            information = content2.find_all('section', attrs={'data-testid': 'cmp-section'})           
        scraped_data = "\n".join([element.text for element in information])
        file_path = os.path.join('data/', f"{disease}.txt")
        with open(file_path, 'a') as f:
            f.write(scraped_data)
        return None
        
    
loader = DirectoryLoader("data/")
index = VectorstoreIndexCreator().from_loaders([loader])
chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)


@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    try:
        incoming_message = request.values.get('Body', '').strip()

        if incoming_message.lower() in ['quit', 'q', 'exit']:
            session.clear()
            #for filename in os.listdir('data/'):
                #file_path = os.path.join('data/', filename)
                #if os.path.isfile(file_path):
                    #os.remove(file_path)
            return 'Chat ended', 200
        
        if incoming_message.lower() in ['help', 'h']:
            response = MessagingResponse()
            response.message("You can ask about a disease, and I will provide information. Type 'quit' to end the chat.")
            return str(response)
        
        
        disease_name = incoming_message
        scrape_data(disease_name)
            
        chat_history = []  
            
        # Pass the user's message to your chatbot function
        result = chain({"question": incoming_message, "chat_history": chat_history})
        chat_history.append((incoming_message, result['answer']))
        chatbot_response = result['answer']
        
        client.messages.create(
            body=chatbot_response,
            from_='whatsapp:+141******86',  # Use your Twilio WhatsApp number
            to='whatsapp:+917********5'  # The user's WhatsApp number
        )
        
        return '', 204  # Return a success response to Twilio

    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run()
