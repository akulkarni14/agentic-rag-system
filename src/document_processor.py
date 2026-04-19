import os
import glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def load_documents(data_dir: str):
    """Loads all PDF and TXT files from the specified directory."""
    documents = []
    
    # Load PDFs
    for pdf_file in glob.glob(os.path.join(data_dir, "*.pdf")):
        try:
            loader = PyPDFLoader(pdf_file)
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading PDF {pdf_file}: {e}")
        
    # Load TXTs
    for txt_file in glob.glob(os.path.join(data_dir, "*.txt")):
        try:
            loader = TextLoader(txt_file, encoding="utf-8")
            documents.extend(loader.load())
        except Exception as e:
            print(f"Error loading TXT {txt_file}: {e}")
            
    return documents

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Splits documents into smaller chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)

def create_vector_db(chunks, persist_directory="./chroma_db"):
    """Creates a Chroma vector database from the document chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        print(f"Loading existing vector database at {persist_directory}...")
        vector_db = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
    else:
        print(f"Creating new vector database at {persist_directory}...")
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        # .persist() is deprecated and automatic in newer Chroma
        
    return vector_db

def setup_retriever(data_dir="./data", persist_directory="./chroma_db"):
    """Main function to setup the retriever."""
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    # Set GOOGLE_API_KEY if GEMINI_API_KEY is present
    if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
        
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable not found. Please set it in your .env file.")

    # basic check if already constructed
    if os.path.exists(persist_directory) and os.listdir(persist_directory):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        vector_db = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
        return vector_db.as_retriever(search_kwargs={"k": 3})

    print("Initializing Document Processor...")
    documents = load_documents(data_dir)
    
    if not documents:
        print(f"No documents found in {data_dir}. System will only have general knowledge.")
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        vector_db = Chroma(
            persist_directory=persist_directory, 
            embedding_function=embeddings
        )
        return vector_db.as_retriever(search_kwargs={"k": 3})
        
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks from {len(documents)} documents.")
    
    vector_db = create_vector_db(chunks, persist_directory)
    print("Vector database created successfully.")
    
    return vector_db.as_retriever(search_kwargs={"k": 3})
