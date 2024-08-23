import os
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate


prompt_template = PromptTemplate(
    input_variables=["context", "chat_history", "input"],
    template='''
    System:
    Answer any use questions based solely on the context below:

    <context>
    {context}
    </context>


    Human:
    {input}
    '''
)

# Set your Google API key
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
db_file_path='FAISS_Index'
data = "data/asthma.txt"

loader = TextLoader(file_path=data)

# Create a Gemini chat model
llm  = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
data = loader.load()
#db.save_local(db_file_path)
index = None
current_disease = None
db=FAISS.from_documents(data, embeddings)
retriever = db.as_retriever()
combined_docs = create_stuff_documents_chain(llm = llm, prompt=prompt_template)
chain = create_retrieval_chain(retriever, combined_docs)
result = chain.invoke({"input": "symptoms of asthma?"})
a = result["answer"]
