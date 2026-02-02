import os
from pinecone import Pinecone, ServerlessSpec

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "rag-saas")

pc = Pinecone(api_key=PINECONE_API_KEY)

# Get or create index
try:
    index = pc.Index(PINECONE_INDEX)
except Exception as e:
    # Create index if doesn't exist
    pc.create_index(
        name=PINECONE_INDEX,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    index = pc.Index(PINECONE_INDEX)

def upsert_vectors(vectors: list, namespace: str = "default"):
    """Upsert vectors to Pinecone"""
    try:
        index.upsert(vectors=vectors, namespace=namespace)
        return True
    except Exception as e:
        print(f"Upsert error: {e}")
        return False

def query_vectors(vector: list, top_k: int = 5, namespace: str = "default"):
    """Query vectors from Pinecone"""
    try:
        results = index.query(
            vector=vector,
            top_k=top_k,
            namespace=namespace,
            include_metadata=True
        )
        return results.matches
    except Exception as e:
        print(f"Query error: {e}")
        return []
