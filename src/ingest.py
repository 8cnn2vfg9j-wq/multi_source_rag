import os
import json
import chromadb
from chromadb.utils import embedding_functions

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "data", "chroma_db")
JSON_PATH = os.path.join(BASE_DIR, "data", "raw", "sample_telegram_data.json")

DOMAIN_ALIASES = {
    "wifi": ["internet", "connection", "network", "univ-secure", "university wifi", "campus wifi", "login", "library wifi"],
    "override": ["course registration", "add drop", "class permit", "cs department"],
    "tech support": ["it help desk", "student union", "computer support", "help desk"]
}

def enrich_text_with_aliases(text: str) -> str:
    enriched = text
    lower_text = text.lower()
    for key, aliases in DOMAIN_ALIASES.items():
        if key in lower_text:
            enriched += f" (Keywords: {', '.join(aliases)})"
    return enriched

def ingest_data():
    if not os.path.exists(JSON_PATH):
        print(f"Error: Could not find dataset at {JSON_PATH}")
        return

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Force clear old index
    try:
        client.delete_collection(name="student_qa")
        print("Cleared stale collection database.")
    except Exception:
        pass

    collection = client.create_collection(
        name="student_qa",
        embedding_function=ef
    )

    documents = []
    ids = []
    metadatas = []

    threads = data.get("threads", [])
    if threads:
        for thread in threads:
            raw_text = " ".join(thread["context"].split())
            enriched_text = enrich_text_with_aliases(raw_text)
            documents.append(enriched_text)
            ids.append(str(thread["thread_id"]))
            metadatas.append({
                "topic": thread.get("topic", "General"),
                "char_count": len(enriched_text)
            })

    collection.add(documents=documents, ids=ids, metadatas=metadatas)
    print(f"Successfully ingested {len(documents)} items into ChromaDB.")

if __name__ == "__main__":
    ingest_data()