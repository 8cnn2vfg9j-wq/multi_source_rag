import os
import chromadb
from chromadb.utils import embedding_functions

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db")

def get_collection():
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_or_create_collection(name="student_qa", embedding_function=ef)

def query_knowledge_base(user_query: str, top_k: int = 1):
    """Queries ChromaDB and returns document texts, metadata, and distance metrics."""
    try:
        collection = get_collection()
        results = collection.query(
            query_texts=[user_query],
            n_results=top_k,
            include=["documents", "distances", "metadatas"]
        )
        return results
    except Exception as e:
        print(f"Vector Store Error: {e}")
        return {"documents": [[]], "distances": [[]], "metadatas": [[]]}