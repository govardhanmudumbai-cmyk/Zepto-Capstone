# Module 3 — Zepto Support Assistant

## Overview

This module implements a document-grounded support assistant.

Architecture:

Documents
→ Embeddings
→ ChromaDB
→ LangGraph
→ FastAPI

## Policy Documents

Eight Zepto policy documents are stored in:

`docs/`

The documents cover:

- Delivery
- Returns and refunds
- Membership
- Order tracking
- Order cancellation
- Damaged or missing items
- Gift cards
- Customer support

## Embeddings

The `all-MiniLM-L6-v2` sentence-transformer model is used
to create document embeddings.

## Vector Database

ChromaDB is used as the persistent vector store.

## Retrieval

The user question is embedded and compared with the policy
document embeddings.

The top relevant documents are retrieved and returned as sources.

## LangGraph

The application contains three nodes:

1. classify_intent
2. retrieve_and_answer
3. direct_answer

Flow:

START
→ classify_intent
→ policy question
→ retrieve_and_answer
→ END

OR

START
→ classify_intent
→ general question
→ direct_answer
→ END

## Mock LLM

The project uses a deterministic mock answer path for the
baseline implementation.

No paid external LLM service is required.

## FastAPI

The application exposes:

POST /ask

Example:

{
    "query": "What is the delivery fee?"
}

## Local Run

Install dependencies:

pip install -r requirements.txt

Run:

uvicorn main:app --host 0.0.0.0 --port 7860

## Docker

Build:

docker build -t zepto-support .

Run:

docker run -p 7860:7860 zepto-support

## Project Structure

support_assistant/

    docs/
        doc_01.txt
        doc_02.txt
        doc_03.txt
        doc_04.txt
        doc_05.txt
        doc_06.txt
        doc_07.txt
        doc_08.txt

    chroma_db/

    rag.py

    main.py

    requirements.txt

    Dockerfile

    README.md
---

## MOCK_LLM Configuration

The support assistant supports a deterministic offline mock mode.

By default:

`MOCK_LLM=true`

When MOCK_LLM=true, the assistant generates its answer from the
highest-ranked retrieved policy context. This allows the
application to run without an external LLM API key.

For the optional real-LLM path:

`MOCK_LLM=false`

When mock mode is disabled, the application can use the configured
real LLM provider. If the real LLM call fails, the application
falls back to the deterministic mock response.

The retrieval pipeline remains the same in both modes:

```text
Policy documents
      ↓
Chunking
      ↓
Embeddings
      ↓
ChromaDB
      ↓
Top-k retrieval
      ↓
Prompt/context
      ↓
MOCK_LLM or real LLM
      ↓
Grounded response
```
