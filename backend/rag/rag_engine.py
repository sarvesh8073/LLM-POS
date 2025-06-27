import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

class RAGEngine:
    def __init__(self, index_path="backend/rag/faiss_index"):
        if not os.path.exists(index_path):
            raise FileNotFoundError("FAISS index not found. Please run build_faiss.py first.")
        
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = FAISS.load_local(index_path, self.embedding_model, allow_dangerous_deserialization=True)

    def query(self, question: str, top_k=3) -> tuple[str, list[Document]]:
        docs = self.db.similarity_search(question, k=top_k)

        # Combine all docs into a single context string
        context = "\n\n".join([doc.page_content for doc in docs])
        return context, docs
