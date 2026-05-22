from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n","\n","."," "]
    )
    chunks = splitter.split_documents(pages)
    print(f"Loaded {len(pages)} pages -> split into {len(chunks)} chunks")
    return chunks