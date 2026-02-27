import insightface
import chromadb
import numpy as np
import cv2
from insightface.app import FaceAnalysis

# --- InsightFace setup ---
app = FaceAnalysis(name='buffalo_l')  # buffalo_l = best accuracy
app.prepare(ctx_id=0, det_size=(640, 640))  
# ctx_id=0 for GPU, ctx_id=-1 for CPU

# --- ChromaDB setup ---
chroma_client = chromadb.PersistentClient(path="./attendance_db")

collection = chroma_client.get_or_create_collection(
    name="students",
    metadata={"hnsw:space": "cosine"}  # cosine similarity for face embeddings
)