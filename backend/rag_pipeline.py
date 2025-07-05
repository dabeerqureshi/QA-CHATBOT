import os
import faiss
import pickle
import numpy as np
from embedder import embed
from model import generate_answer

# === Safe Path Handling ===
BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "faiss_index", "index.faiss")
META_PATH = os.path.join(BASE_DIR, "faiss_index", "metadata.pkl")

# === Load FAISS Index and Metadata ===
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, "rb") as f:
    metadata = pickle.load(f)

# === Threshold for deciding if context is relevant ===
DISTANCE_THRESHOLD = 1.0  # loosened threshold, tune as needed

# Simple greetings & farewells map
GREETINGS = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! What can I do for you?",
    "hey": "Hey! How may I assist you?",
    "good morning": "Good morning! How can I assist you?",
    "good afternoon": "Good afternoon! How can I help?",
    "good evening": "Good evening! How can I assist you?",
    "bye": "Goodbye! Have a great day!",
    "goodbye": "Bye! Feel free to ask if you need anything else.",
    "see you": "See you later! Take care.",
    "thanks": "You're welcome! Let me know if you have more questions.",
    "thank you": "Glad to help! Ask anytime."
}

def retrieve_and_generate(query: str) -> str:
    # Normalize query for matching
    q_norm = query.strip().lower()

    # Check for simple greetings and farewells
    for key_phrase, response in GREETINGS.items():
        if key_phrase in q_norm:
            return response

    # Otherwise proceed with FAISS retrieval + generation
    query_vec = embed([query])[0].reshape(1, -1)
    distances, indices = index.search(query_vec, k=3)

    if distances[0][0] > DISTANCE_THRESHOLD:
        return "Sorry, I don't have enough information to answer that question."

    retrieved_contexts = [metadata[i] for i in indices[0]]
    combined_context = " ".join(retrieved_contexts)

    prompt = f"""You are a helpful customer support agent.
Answer the following question briefly and accurately using the given context.

Context: {combined_context}
Question: {query}
Answer (brief and to the point):"""

    return generate_answer(prompt)
