import chromadb
import ollama

client = chromadb.PersistentClient(path="./data/chroma_db")
collection = client.get_or_create_collection("student_memory")


def add_memory(student_id: int, text: str) -> None:
    embedding = ollama.embeddings(model="nomic-embed-text", prompt=text)["embedding"]

    collection.add(
        ids=[f"{student_id}_{hash(text)}"],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"student_id": student_id}],
    )


def search_memory(student_id: int, query: str):
    embedding = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5,
        where={"student_id": student_id},
    )

    return results.get("documents", [])
