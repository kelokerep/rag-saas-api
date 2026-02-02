def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split text into overlapping chunks"""
    chunks = []
    start = 0
    
    while start < len(text):
        # Get chunk
        end = start + chunk_size
        chunk = text[start:end]
        
        # Don't add empty chunks
        if chunk.strip():
            chunks.append(chunk.strip())
        
        # Move start position with overlap
        start += chunk_size - overlap
    
    return chunks
