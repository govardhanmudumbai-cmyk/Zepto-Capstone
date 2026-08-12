# Capstone Project — Zepto Data & AI Platform

An end-to-end AI/ML engineering project containing three connected modules:

1. Data Pipeline
2. Analytics Pipeline
3. GenAI Support Assistant

---

# Project Structure

```text
Zepto-Capstone/
│
├── data_pipeline/
│   ├── ...
│
├── analytics/
│   ├── ...
│
├── support_assistant/
│   ├── docs/
│   ├── rag.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── README.md
│   └── .gitignore
│
└── README.md
```

---

# Module 1 — Data Pipeline

Location: `data_pipeline/`

The data pipeline scrapes book catalogue data from books.toscrape.com,
cleans the data, converts GBP prices to INR, stores the result in a
normalized SQLite database, and demonstrates SQL and pandas analysis.

## Required Currency Conversion

**1 GBP = 105.50 INR**

This is the fixed project-defined conversion rate required by the assignment.

---

# Module 2 — Analytics Pipeline

Location: `analytics/`

The analytics pipeline loads the Titanic dataset once, performs profiling
and EDA, handles missing values, creates visualizations, trains three
classification models, evaluates imbalance strategies, performs
hyperparameter tuning, and completes a regression task.

The offline dataset is stored as:

`analytics/titanic.csv`

The modeling pipeline is saved as a joblib artifact.

---

# Module 3 — GenAI Support Assistant

Location: `support_assistant/`

The support assistant answers Zepto policy questions using a grounded
retrieval-augmented generation workflow.

## Components

- Eight Zepto policy documents
- Sentence Transformer embeddings
- ChromaDB vector store
- LangGraph orchestration
- FastAPI API
- Optional real LLM integration
- MOCK_LLM mode for deterministic grading

## Architecture

```text
Zepto Policy Documents
        ↓
Document Chunking
        ↓
Sentence Transformer Embeddings
        ↓
ChromaDB
        ↓
User Question
        ↓
Intent Classification
        ↓
Top-k Retrieval
        ↓
Prompt Construction
        ↓
MOCK_LLM / Real LLM
        ↓
Grounded Answer
        ↓
FastAPI JSON Response
```

## Running Module 3

From the `support_assistant` directory:

```bash
pip install -r requirements.txt
```

Then start the API:

```bash
uvicorn main:app --host 0.0.0.0 --port 7860
```

The API endpoint is:

`POST /ask`

Example request:

```json
{
  "query": "Can I cancel my order?"
}
```

## Mock LLM

The application supports deterministic mock mode for environments
where no external LLM API key is available.

The mock response is generated from the highest-ranked retrieved
policy context and therefore remains grounded in the supplied documents.

## Real LLM

The application also contains an optional real-LLM path. If the real
LLM call fails, the application falls back to the deterministic mock
response so that the service remains usable.

---

# Installation

Each module contains or documents its required dependencies.

Module 3 dependencies can be installed using:

```bash
cd support_assistant
pip install -r requirements.txt
```

---

# Git Workflow

The repository follows a feature-branch workflow.

A feature branch is created from `main`, committed to at least twice,
and then merged back into `main`.

```text
main
  │
  └── feature/module3
          │
          ├── commit 1
          │
          └── commit 2
                  │
                  ↓
              merge → main
```

---

# Design Summary

## Data Pipeline

A raw-to-relational pipeline that scrapes, cleans, converts and stores
catalogue data in a normalized SQLite database.

## Analytics Pipeline

A complete analyst-to-data-scientist workflow covering profiling, EDA,
preprocessing, classification, evaluation, tuning, regression and
model persistence.

## Support Assistant

A document-grounded GenAI service using vector retrieval and LangGraph
to answer questions from Zepto policy documents through a FastAPI API.

---

# No Paid Services

The project does not require paid services.

Module 1 uses the required fixed conversion rate:

**1 GBP = 105.50 INR**

Module 3 supports deterministic local mock inference and local
embedding/vector-search components.