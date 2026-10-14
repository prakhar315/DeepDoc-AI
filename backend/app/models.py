
from typing import Dict, Optional

from pydantic import BaseModel

class DocumentUpload(BaseModel):
    id: Optional[str] = None
    text: str
    metadata: Optional[dict] = None

class SearchRequest(BaseModel):
    query: str
    department: Optional[str] = None,
    top_k: int = 5

class SearchResult(BaseModel):
    id: str
    score: float
    text: str
    metadata: Optional[Dict] = None