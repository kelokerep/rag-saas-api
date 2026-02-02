# RAG API Deployment Guide
**Status:** Code Complete - Ready for Render Deploy
**ETA:** 5 minutes after config

---

## Deployment Steps

### 1. Environment Variables Needed
Create these in Render dashboard:
- `OPENAI_API_KEY` - Your OpenAI API key
- `PINECONE_API_KEY` - Your Pinecone API key
- `PINECONE_INDEX` = `rag-saas`

### 2. Deploy
Render will auto-deploy from `render.yaml`

### 3. Update x402 Endpoint URL
Once deployed, update the endpoint:
```bash
cd /Users/ofiz/clawd/x402-layer
source .env
X_API_KEY="x402_847b9c1189dd4fa09d2fcb983bee7629" \
  python3 scripts/manage_endpoint.py update rag-saas-kit \
  --origin https://rag-saas-api.onrender.com
```

---

## API Testing

### Upload Document
```bash
curl -X POST "https://rag-saas-api.onrender.com/upload" \
  -F "file=@document.txt"
```

### Query (through x402 - paid)
```bash
curl -X POST "https://api.x402layer.cc/e/rag-saas-kit/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: x402_847b9c1189dd4fa09d2fcb983bee7629" \
  -d '{"query": "What is this document about?"}'
```

---

## Revenue Model Active
- $0.01 per API call
- Payments auto-collected to your wallet
- 20,000 credits available

**Next:** Deploy to Render, then start promoting to Moltbook agents
