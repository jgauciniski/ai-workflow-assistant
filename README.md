# AI Workflow Assistant

An AI-powered backend system that processes support tickets and answers questions using **LLMs, Retrieval-Augmented Generation (RAG), and semantic search**.

---

## 🚀 Overview

This project demonstrates how to design and build an **AI-driven workflow system** that:

- Transforms unstructured support tickets into structured data
- Uses LLMs for extraction, classification, and summarization
- Stores enriched data with embeddings for semantic retrieval
- Answers questions using RAG (Retrieval-Augmented Generation)
- Exposes functionality via **CLI and API (FastAPI)**

---

## 🧠 Key Features

### 🎫 Ticket Processing (LLM Workflow)
- Extract structured data:
  - Issue
  - Actions Taken
  - Requested Resolution
- Classify priority (low, medium, high)
- Generate summary
- Store enriched ticket with embeddings

---

### 🔍 Question Answering (RAG)
- Convert user question into embedding
- Retrieve relevant tickets using **cosine similarity**
- Provide **grounded answers** using LLM + retrieved context
- Reduce hallucination by limiting context

---

### ⚙️ Workflow Routing (Agent-like Behavior)
- Uses LLM to decide:
  - Process ticket
  - Answer question

---

### 🛡️ Reliability Layer
- Retry logic for LLM failures
- Safe JSON parsing
- Data validation

---

### 🌐 API Layer (FastAPI)
- REST endpoints
- Swagger UI: http://localhost:8000/docs

---

### 💻 CLI Interface
- Used for development and debugging

---

## 🏗️ Architecture

scripts/
app/
  api/
  commands/
  models/
  retrieval/
  utils/
  workflows/
  services/
data/

---

## 🔄 System Flow

### 🎫 Ticket Processing


User Input
↓
LLM Extraction (structured JSON)
↓
Validation
↓
Priority Classification
↓
Summary Generation
↓
Build Retrieval Document
↓
Generate Embedding
↓
Store Ticket


### 🔍 Question Answering (RAG)


User Question
↓
Generate Embedding
↓
Semantic Search (Cosine Similarity)
↓
Retrieve Top-K Tickets
↓
Build Context
↓
LLM Generates Answer

---

## 🧩 Core Concepts

- RAG (Retrieval-Augmented Generation)
- Embeddings
- Cosine Similarity

---

## ⚖️ Trade-offs

| Area | Current Approach | Limitation |
|------|----------------|-----------|
| Storage | In-memory + JSON | Not scalable |
| Retrieval | Brute-force similarity | Not efficient at scale |
| LLM usage | Multiple small calls | Higher cost |
| Architecture | Monolithic backend | Not fully production-ready |

---

## 🚧 Future Work / Production Improvements 

- Database (PostgreSQL)
- Vector storage (pgvector or vector DB)
- Authentication & user isolation
- Caching and async processing
- Monitoring & logging
- Scalable deployment (AWS, containers)

---

## 🧠 Technologies Used

- Python
- FastAPI
- OpenAI API (LLMs)
- Embeddings (semantic search)
- JSON-based persistence

---

## ▶️ Running the Project

### Run CLI

python -m scripts.cli

### Run API

uvicorn app.api.main:app --reload

### Open API Docs (Swagger)

http://localhost:8000/docs

---

## 🎯 Why This Project

This system simulates how AI can be used to automate real-world support workflows by:

- Reducing manual ticket processing effort
- Structuring unorganized data into actionable insights
- Enabling fast, intelligent retrieval of past issues
- Demonstrating how AI systems can drive operational efficiency

This aligns with real-world use cases where teams need to scale support, knowledge access, and decision-making using AI.

---

## 🧠 Learning Focus

This project was built to deepen understanding of:

- LLM-based workflows
- Retrieval-Augmented Generation (RAG)
- Backend system design for AI applications
- Trade-offs between accuracy, cost, and scalability

---

## 👨‍💻 Author

Juliano Gauciniski
