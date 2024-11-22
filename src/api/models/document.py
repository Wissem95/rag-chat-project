from pydantic import BaseModel
from typing import Dict, List

class DocumentRequest(BaseModel):
    content: str
    filename: str

class DocumentResponse(BaseModel):
    id: str
    filename: str
    metadata: Dict
    tags: List[str]
