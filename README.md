# RAG SaaS API

Production-ready RAG API deployed on Render (free tier).

## Deploy to Render

1. Push this code to GitHub
2. Connect repo to Render
3. Add environment variables:
   - `OPENAI_API_KEY`
   - `PINECONE_API_KEY`
4. Deploy automatically

## API Endpoints

### Upload Document
```bash
curl -X POST "https://rag-saas-api.onrender.com/upload" \
  -F "file=@document.txt"
```

### Query
```bash
curl -X POST "https://rag-saas-api.onrender.com/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is this document about?"}'
```

## Environment Variables

- `OPENAI_API_KEY` - OpenAI API key
- `PINECONE_API_KEY` - Pinecone API key
- `PINECONE_INDEX` - Pinecone index name (default: rag-saas)
