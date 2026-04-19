# backend/main.py

import sys
import os
sys.path.append(os.path.dirname(__file__))

import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
from dotenv import load_dotenv
from prompt import build_prompt, SYSTEM_PROMPT

# Load the ANTHROPIC_API_KEY from your .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="SQL Query Generator API",
    description="Converts natural language to SQL using Claude",
    version="1.0.0"
)

# Allow your frontend (running on a different port) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Anthropic client (reads API key from .env automatically)
client = anthropic.Anthropic()


# --- Request & Response Models ---

class QueryRequest(BaseModel):
    schema: str      # The CREATE TABLE statements
    question: str    # The plain English question

class QueryResponse(BaseModel):
    sql: str         # The generated SQL query
    latency_ms: int  # How long it took in milliseconds
    question: str    # Echo back the original question


# --- Routes ---

@app.get("/")
def root():
    """Health check — confirms the server is running."""
    return {"status": "running", "message": "SQL Query Generator API is live"}


@app.post("/generate-sql", response_model=QueryResponse)
def generate_sql(req: QueryRequest):
    """
    Main endpoint. Takes a schema + question, returns SQL.
    This is the endpoint your frontend will call.
    """

    # Basic validation
    if not req.schema.strip():
        raise HTTPException(status_code=400, detail="Schema cannot be empty")
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        start_time = time.time()

        # Call Claude API
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Fast + cheap for testing
            max_tokens=500,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": build_prompt(req.schema, req.question)
                }
            ]
        )

        latency_ms = int((time.time() - start_time) * 1000)
        sql = message.content[0].text.strip()

        return QueryResponse(
            sql=sql,
            latency_ms=latency_ms,
            question=req.question
        )

    except anthropic.AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key. Check your .env file."
        )
    except anthropic.RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Rate limit hit. Wait a moment and try again."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    """Returns API key status without exposing the key itself."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    return {
        "status": "ok",
        "api_key_set": bool(api_key and api_key != "your_key_here")
    }