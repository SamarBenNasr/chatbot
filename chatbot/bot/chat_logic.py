# chatbot/chat_logic.py

import os
import re
from dotenv import load_dotenv
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

def select_llm():
    return HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation",
        temperature=0.7,
        token=HF_TOKEN,
        max_new_tokens=500,
    )

def init_rag():
    file_path = "C:/Users/MSI/chatbot/bot/faq.txt"
    loader = TextLoader(file_path)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore.as_retriever()


retriever = init_rag()

def is_greeting(msg): return re.search(r"\b(hi|hello|salut|bonjour)\b", msg.lower())
def is_farewell(msg): return re.search(r"\b(bye|goodbye|à bientôt)\b", msg.lower())
def is_agreement(msg): return re.search(r"\b(yes|ok|oui|d'accord)\b", msg.lower())
def is_disagreement(msg): return re.search(r"\b(no|non)\b", msg.lower())
def is_thank_you(msg): return re.search(r"\b(thanks|merci)\b", msg.lower())

def get_answer(llm, message):
    if is_greeting(message):
        return "Hello! 👋 How can I help you today?"
    elif is_farewell(message):
        return "Goodbye! Take care! 👋"
    elif is_agreement(message):
        return "Perfect! Let's continue. 👍"
    elif is_disagreement(message):
        return "Alright, let me know what you'd prefer. 🤔"
    elif is_thank_you(message):
        return "You're welcome! 😊"
    
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return rag_chain.run(message)
