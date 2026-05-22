from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
import os

def get_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text:v1.5")  

def build_vectorstore(chunks, path="vectorstore"):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(path)
    print(f"Vector store saved to '{path}'")
    return vectorstore

def load_vectorstore(path="vectorstore"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No vectorstore at '{path}'")
    embeddings = get_embeddings()
    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )