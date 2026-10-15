def chunk_text(text: str, size: int = 500, overlap: int = 50):
    step = size - overlap
    chunks = [text[i : i + size] for i in range(0, len(text), step)]
    return chunks
