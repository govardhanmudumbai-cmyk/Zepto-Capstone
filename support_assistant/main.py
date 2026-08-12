from fastapi import FastAPI

from pydantic import BaseModel

from rag import ask_zepto


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Zepto Support Assistant",
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class AskRequest(BaseModel):

    query: str


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {

        "status": "running",

        "service":
            "Zepto Support Assistant"
    }


# ============================================================
# ASK ENDPOINT
# ============================================================

@app.post("/ask")
def ask(
    request: AskRequest
):

    return ask_zepto(
        request.query
    )