import os
from fasthtml.common import *
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from scraper import scrape_disease
import constants
# Set up the app
tlink = Script(src="https://cdn.tailwindcss.com")
dlink = Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css")

app = FastHTML(hdrs=(tlink, dlink))

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = constants.API_KEY

# Initialize global variables
current_disease = None
db = None
chain = None
messages = []

# Set up the LLM and embedding model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "chat_history", "input"],
    template='''
    System:
    Answer any user questions based solely on the context below:

    <context>
    {context}
    </context>

    Human:
    {input}
    '''
)

# Chat message component
def ChatMessage(msg_idx):
    msg = messages[msg_idx]
    text = msg['content']
    bubble_class = "chat-bubble-primary" if msg['role'] == 'user' else 'chat-bubble-secondary'
    chat_class = "chat-end" if msg['role'] == 'user' else 'chat-start'
    return Div(Div(msg['role'], cls="chat-header"),
               Div(text, cls=f"chat-bubble {bubble_class}"),
               cls=f"chat {chat_class}", id=f"chat-message-{msg_idx}")

# Disease input form
def DiseaseForm():
    return Form(
        Input(type="text", name='disease', placeholder="Enter disease name", cls="input input-bordered"),
        Button("Scrape Disease", cls="btn btn-primary"),
        hx_post="/scrape_disease", hx_target="#chat-container"
    )

# Chat input form
def ChatInput():
    return Form(
        Input(type="text", name='question', placeholder="Ask a question", cls="input input-bordered w-full"),
        Button("Send", cls="btn btn-primary"),
        hx_post="/ask_question", hx_target="#chat-container", hx_swap="beforeend"
    )

# Main page
@app.route("/")
def get():
    page = Body(
        H1('Disease Q&A Chatbot'),
        DiseaseForm(),
        Div(id="chat-container", cls="mt-4"),
        cls="p-4 max-w-lg mx-auto"
    )
    return Title('Disease Q&A Chatbot'), page

# Scrape disease route
@app.post("/scrape_disease")
def scrape_disease_route(disease: str):
    global current_disease, db, chain
    
    file_path = scrape_disease(disease)
    if file_path:
        current_disease = disease
        loader = TextLoader(file_path=file_path)
        data = loader.load()
        db = FAISS.from_documents(data, embeddings)
        retriever = db.as_retriever()
        combined_docs = create_stuff_documents_chain(llm=llm, prompt=prompt_template)
        chain = create_retrieval_chain(retriever, combined_docs)
        
        return Div(
            P(f"Information about {disease} has been scraped and loaded."),
            ChatInput(),
            id="chat-container"
        )
    else:
        return P(f"Could not find information about {disease}.")

# Ask question route
@app.post("/ask_question")
def ask_question(question: str):
    global chain, messages
    
    if not chain:
        return P("Please scrape a disease first.")
    
    messages.append({"role": "user", "content": question})
    result = chain.invoke({"input": question})
    answer = result["answer"]
    messages.append({"role": "assistant", "content": answer})
    
    return Div(*[ChatMessage(i) for i in range(len(messages)-2, len(messages))])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)