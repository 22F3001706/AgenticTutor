from rag.loader import load_and_split
from rag.embeddings import build_vectorstore, load_vectorstore
from rag.chain import build_chain
from rag.voice import speak
import os

PDF_PATH = "BOOKS/C9S/CH1.pdf"

if not os.path.exists("vectorstore"):
    print("Building vectorstore for the first time...")
    chunks = load_and_split(PDF_PATH)
    vectorstore = build_vectorstore(chunks)
else:
    print("Loading existing vectorstore...")
    vectorstore = load_vectorstore()

chain = build_chain(vectorstore)

print("\nChapter 1 RAG ready! Ask anything. Type 'quit' to exit.\n")

while True:
    question = input("You: ").strip()
    if not question:
        continue
    if question.lower() == "quit":
        break

    answer = chain.invoke(question)
    print(f"\nAssistant: {answer}\n")

    # Voice is optional — won't crash if it fails
    try:
        speak(answer)
    except Exception as e:
        pass  # silently skip if voice fails