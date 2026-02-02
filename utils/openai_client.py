import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_rag_response(query: str, context: str, model: str = "gpt-3.5-turbo") -> str:
    """Generate RAG response using context"""
    try:
        system_prompt = """You are a helpful assistant. Answer the user's question based on the provided context. 
If the context doesn't contain relevant information, say so clearly.
Be concise and accurate."""
        
        user_prompt = f"""Context:
{context}

Question: {query}

Answer:"""
        
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Generation error: {e}")
        return f"Error generating response: {str(e)}"
