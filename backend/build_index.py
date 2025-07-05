import os
import faiss
import pickle
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# === Config ===
CSV_PATH = os.path.join("", "data", "faq.csv")  # relative to /backend
INDEX_DIR = os.path.join("faiss_index")
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")
META_FILE = os.path.join(INDEX_DIR, "metadata.pkl")
EMBED_MODEL = 'all-MiniLM-L6-v2'

# === Ensure index folder exists ===
os.makedirs(INDEX_DIR, exist_ok=True)

# === Load CSV ===
try:
    df = pd.read_csv(CSV_PATH).dropna()
    questions = df["Question"].astype(str).tolist()
    answers = df["Answer"].astype(str).tolist()
except Exception as e:
    raise FileNotFoundError(f"❌ Error loading CSV: {e}")

# === Load model ===
print(f"🔄 Loading embedding model: {EMBED_MODEL}")
model = SentenceTransformer(EMBED_MODEL)

# === Embed questions ===
print(f"🔍 Embedding {len(questions)} questions...")
vectors = model.encode(questions, batch_size=32, show_progress_bar=True)

# === Build FAISS index ===
dim = vectors[0].shape[0]
print(f"🧠 Building FAISS index with dimension: {dim}")
index = faiss.IndexFlatL2(dim)
index.add(np.array(vectors).astype("float32"))

# === Save index and metadata ===
faiss.write_index(index, INDEX_FILE)
with open(META_FILE, "wb") as f:
    pickle.dump(answers, f)

print(f"✅ Index built and saved successfully to: {INDEX_DIR}")
