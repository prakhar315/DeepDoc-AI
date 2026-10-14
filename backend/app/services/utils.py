import re
import time
from app.services.embedding import embed_text
from app.services.elastic import index_document
import fitz  # PyMuPDF
import docx
from typing import BinaryIO

def chunk_text(text:str, max_words:int = 350) -> list:
    # Basic sentence splitter (for clean boundaries)
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = []
    
    for sentence in sentences:
        current_chunk.append(sentence)
        chunk = ' '.join(current_chunk)
        if len(chunk.split()) >= max_words:
            chunks.append(chunk)
            current_chunk = []
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def extract_text_from_pdf(file: BinaryIO) -> str:
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file: BinaryIO) -> str:
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def process_and_index_text(
    text: str,
    base_metadata: dict,
    chunk_size: int = 350
) -> list:
    chunks = chunk_text(text, max_words=chunk_size)
    ids = []
    
    base_metadata["doc_id"] = f"{int(time.time())}"

    for idx, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        metadata = base_metadata.copy()
        metadata["chunk"] = idx + 1
        metadata["total_chunks"] = len(chunks)

        result = index_document(chunk, embedding, metadata)
        ids.append(result["id"])

    return ids