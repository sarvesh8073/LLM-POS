import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings

PDF_PATH = "backend/referance/comprehensive-clinical-nephrology.pdf"
FAISS_PATH = "backend/rag/faiss_index"

def build_faiss_index():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found at: {PDF_PATH}")

    print("📄 Loading PDF...")
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()

    print(f"🧱 Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
    docs = splitter.split_documents(pages)

    print(f"🧠 Embedding with SentenceTransformer...")
    embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"📦 Building FAISS index...")
    faiss_index = FAISS.from_documents(docs, embed_model)

    print(f"💾 Saving index to: {FAISS_PATH}")
    faiss_index.save_local(FAISS_PATH)

    print("✅ FAISS index built and saved!")

if __name__ == "__main__":
    build_faiss_index()
