import os
from pathlib import Path
from typing import TypedDict, List

import chromadb

from sentence_transformers import SentenceTransformer

from pydantic import BaseModel, Field

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(
    __file__
).resolve().parent

CHROMA_DIR = BASE_DIR / "chroma_db"


# ============================================================
# RESPONSE MODEL
# ============================================================

class AskResponse(BaseModel):

    answer: str

    sources: List[str]

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )


# ============================================================
# LANGGRAPH STATE
# ============================================================

class GraphState(TypedDict, total=False):

    query: str

    intent: str

    answer: str

    sources: List[str]

    confidence: float


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ============================================================
# CHROMADB
# ============================================================

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_collection(
    "zepto_policy"
)


# ============================================================
# RETRIEVAL
# ============================================================

def retrieve(
    query: str,
    top_k: int = 3
):

    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    )[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# ============================================================
# NODE 1
# CLASSIFY INTENT
# ============================================================

def classify_intent(state):

    query = state["query"].lower()

    policy_words = [

        "delivery",
        "deliver",
        "return",
        "refund",
        "membership",
        "pass",
        "tracking",
        "track",
        "cancel",
        "cancellation",
        "gift",
        "gift card",
        "support",
        "replacement",
        "replace",
        "damaged",
        "damage",
        "missing",
        "spoiled",
        "fee",
        "order",
        "packed",
        "priority"

    ]

    if any(
        word in query
        for word in policy_words
    ):

        return {
            "intent": "policy_question"
        }

    return {
        "intent": "general_question"
    }


# ============================================================
# NODE 2
# RETRIEVE + ANSWER
# ============================================================

def retrieve_and_answer(state):

    results = retrieve(
        state["query"],
        top_k=3
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    sources = results.get(
        "ids",
        [[]]
    )[0]

    if documents:

        answer = (
            "Based on the retrieved Zepto policy: "
            + documents[0]
        )

        confidence = 1.0

    else:

        answer = (
            "No relevant Zepto policy was found."
        )

        confidence = 0.0

    return {

        "answer": answer,

        "sources": sources,

        "confidence": confidence
    }


# ============================================================
# NODE 3
# DIRECT ANSWER
# ============================================================

def direct_answer(state):

    return {

        "answer": (
            "I can only answer questions "
            "about Zepto policies."
        ),

        "sources": [],

        "confidence": 1.0
    }


# ============================================================
# CONDITIONAL ROUTER
# ============================================================

def route(state):

    if state["intent"] == "policy_question":

        return "retrieve_and_answer"

    return "direct_answer"


# ============================================================
# LANGGRAPH
# ============================================================

builder = StateGraph(
    GraphState
)


# Three required nodes

builder.add_node(
    "classify_intent",
    classify_intent
)

builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

builder.add_node(
    "direct_answer",
    direct_answer
)


# Start

builder.add_edge(
    START,
    "classify_intent"
)


# Conditional routing

builder.add_conditional_edges(

    "classify_intent",

    route,

    {
        "retrieve_and_answer":
            "retrieve_and_answer",

        "direct_answer":
            "direct_answer"
    }
)


# End

builder.add_edge(
    "retrieve_and_answer",
    END
)

builder.add_edge(
    "direct_answer",
    END
)


graph = builder.compile()


# ============================================================
# PUBLIC FUNCTION
# ============================================================

def ask_zepto(
    query: str
):

    result = graph.invoke(
        {
            "query": query
        }
    )

    return AskResponse(

        answer=result.get(
            "answer",
            ""
        ),

        sources=result.get(
            "sources",
            []
        ),

        confidence=result.get(
            "confidence",
            0.0
        )
    )

# Deterministic mock mode for offline grading
MOCK_LLM = os.getenv("MOCK_LLM", "true").lower() == "true"
