from typing import List
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.utils import (
    extract_text_from_docx,
    extract_text_from_pdf,
    process_and_index_text,
)
from app.services.elastic import (
    delete_all_by_document_id,
    get_full_document_text_by_group,
    search_similar_documents,
)
from app.services.embedding import embed_text
from app.models import DocumentUpload, SearchRequest, SearchResult

# Metadata keys
DEPARTMENT = "department"
TITLE = "title"
SOURCE = "source"

router = APIRouter()


@router.get("/", tags=["Health"])
def health_check():
    return {"message": "DeepDoc AI backend running successfully!"}


@router.post("/upload", tags=["Document Upload"])
def upload_doc(doc: DocumentUpload):
    ids = process_and_index_text(
        text=doc.text,
        base_metadata=doc.metadata or {}
    )
    return {"message": f"{len(ids)} chunks uploaded", "ids": ids}


@router.post("/upload-file", tags=["Document Upload"])
def upload_file(
    file: UploadFile = File(...),
    department: str = Form(...),
    title: str = Form(...)
):
    filename = Path(file.filename).name.lower()

    try:
        if filename.endswith(".pdf"):
            text = extract_text_from_pdf(file.file)
        elif filename.endswith(".docx"):
            text = extract_text_from_docx(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    base_metadata = {
        DEPARTMENT: department,
        TITLE: title,
        SOURCE: filename,
    }

    ids = process_and_index_text(text, base_metadata)
    return {"message": f"{len(ids)} chunks uploaded", "ids": ids}


@router.post("/search", response_model=List[SearchResult], tags=["Search"])
def search_docs(payload: SearchRequest):
    if not 1 <= payload.top_k <= 50:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 50")

    query_embedding = embed_text(payload.query)
    results = search_similar_documents(
        query_embedding,
        department=payload.department,
        top_k=payload.top_k
    )
    return results


@router.get("/document/full/{key}/{value}", tags=["Document Retrieval"])
def get_full_document(key: str, value: str):
    doc = get_full_document_text_by_group(key, value)
    if doc["chunk_count"] == 0:
        raise HTTPException(status_code=404, detail="No chunks found for this document")
    return doc


@router.delete("/delete/doc_id/{doc_id}", tags=["Document Admin"])
def delete_document_by_document_id(doc_id: str):
    result = delete_all_by_document_id(doc_id)
    deleted = result.get("deleted", 0)
    return {"message": f"Deleted {deleted} chunks from document '{doc_id}'."}
