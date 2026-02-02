from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import hashlib
import json

# Import our modules
from utils.embeddings import get_embedding
from utils.pinecone_client import upsert_vectors, query_vectors
from utils.chunker import chunk_text
from utils.openai_client import generate_rag_response

app = FastAPI(
    title="RAG SaaS API",
    description="Production-ready RAG API for agents",
    version="1.0.0"
)

# In-memory storage for demo (replace with DB in production)
document_store = {}

class QueryRequest(BaseModel):
    query: str
    document_id: Optional[str] = None
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list
    document_id: str

@app.get("/")
async def root():
    return {
        "service": "RAG SaaS API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "upload": "POST /upload",
            "query": "POST /query",
            "health": "GET /health"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "rag-saas-kit"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document and index it for RAG"""
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8', errors='ignore')
        
        # Generate document ID
        doc_id = hashlib.md5(file.filename.encode()).hexdigest()[:12]
        
        # Chunk the document
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        
        # Generate embeddings and upsert to Pinecone
        vectors = []
        for i, chunk in enumerate(chunks):
            embedding = get_embedding(chunk)
            vectors.append({
                "id": f"{doc_id}_{i}",
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "doc_id": doc_id,
                    "filename": file.filename,
                    "chunk_index": i
                }
            })
        
        # Upsert to Pinecone
        upsert_vectors(vectors)
        
        # Store metadata
        document_store[doc_id] = {
            "filename": file.filename,
            "chunks": len(chunks),
            "doc_id": doc_id
        }
        
        return {
            "success": True,
            "document_id": doc_id,
            "filename": file.filename,
            "chunks_indexed": len(chunks),
            "message": "Document uploaded and indexed successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the RAG system"""
    try:
        # Get query embedding
        query_embedding = get_embedding(request.query)
        
        # Query Pinecone
        results = query_vectors(query_embedding, top_k=request.top_k)
        
        if not results or len(results) == 0:
            return QueryResponse(
                answer="No relevant context found for this query.",
                sources=[],
                document_id="none"
            )
        
        # Extract context from results
        contexts = []
        sources = []
        doc_id = None
        
        for match in results:
            text = match.get('metadata', {}).get('text', '')
            filename = match.get('metadata', {}).get('filename', 'unknown')
            doc_id = match.get('metadata', {}).get('doc_id', 'unknown')
            score = match.get('score', 0)
            
            contexts.append(text)
            sources.append({
                "text": text[:200] + "..." if len(text) > 200 else text,
                "filename": filename,
                "score": round(score, 3)
            })
        
        # Generate response with OpenAI
        context_text = "\n\n".join(contexts)
        answer = generate_rag_response(request.query, context_text)
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            document_id=doc_id or "unknown"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    return {
        "documents": list(document_store.values()),
        "count": len(document_store)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
