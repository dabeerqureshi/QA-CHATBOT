from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import retrieve_and_generate

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/chat")
async def chat(query: str):
    answer = retrieve_and_generate(query)
    return {"response": answer}
