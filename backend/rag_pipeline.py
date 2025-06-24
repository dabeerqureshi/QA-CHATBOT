import faiss
import pickle
import numpy as np
from embedder import embed
from model import generate_answer

# Load FAISS index and metadata
index = faiss.read_index("backend/faiss_index/index.faiss")
with open("backend/faiss_index/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

def retrieve_and_generate(query):
    query_vec = embed([query])[0].reshape(1, -1)
    _, indices = index.search(query_vec, k=1)
    retrieved_text = metadata[indices[0][0]]
    prompt = f"Question: {query}\nContext: {retrieved_text}\nAnswer:"
    return generate_answer(prompt)
