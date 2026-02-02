import os
import openai

# Set API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    """Generate embedding for text using OpenAI"""
    try:
        response = openai.embeddings.create(
            model=model,
            input=text[:8000]  # Limit text length
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding error: {e}")
        # Return zero vector as fallback
        return [0.0] * 1536
