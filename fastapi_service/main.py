from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import os
import json
import fitz  # PyMuPDF for parsing PDF files
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from uuid import uuid4
from config.otel_config import configure_instrumentation

app = FastAPI()

qdrant_client = QdrantClient(":memory:")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
COLLECTION_NAME = "document_embeddings"

qdrant_client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={"size": 384, "distance": "Cosine"}
)

configure_instrumentation(app)

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {e}")

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    os.makedirs("uploads", exist_ok=True)
    for file in files:
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
    return {"message": "Files uploaded successfully"}

@app.post("/index")
async def index_documents():
    documents = []
    for file_name in os.listdir("uploads"):
        file_path = os.path.join("uploads", file_name)
        if file_name.endswith(".pdf"):
            documents.append(extract_text_from_pdf(file_path))
    vectors = [
        {"id": str(uuid4()), "vector": embedding_model.encode(doc), "payload": {"text": doc}}
        for doc in documents
    ]
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=vectors)
    for file_name in os.listdir("uploads"):
        os.remove(os.path.join("uploads", file_name))
    return {"message": f"Indexed {len(vectors)} documents"}

@app.post("/search")
async def search_documents(query: str, top_k: int = 3):
    query_vector = embedding_model.encode(query)
    results = qdrant_client.search(collection_name=COLLECTION_NAME, query_vector=query_vector, limit=top_k)
    return {"results": [{"text": r.payload["text"], "score": r.score} for r in results]}
