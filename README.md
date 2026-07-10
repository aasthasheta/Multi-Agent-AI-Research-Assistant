# Multi-Agent-AI-Research-Assistant
# 🤖 Multi-Agent AI Research Assistant

> An advanced AI-powered research assistant that leverages multiple autonomous agents to perform intelligent research, document analysis, fact verification, and professional report generation using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📖 Overview

The **Multi-Agent AI Research Assistant** is an intelligent research platform that automates the complete research workflow using multiple AI agents. Instead of relying on a single chatbot, the system delegates tasks to specialized agents responsible for planning, searching, retrieving information, verifying facts, maintaining memory, summarizing findings, and generating professional reports.

The application combines **LangGraph**, **LangChain**, **LLMs**, and **Retrieval-Augmented Generation (RAG)** to produce accurate, citation-supported research reports from both uploaded documents and external knowledge sources.

---

# ✨ Features

- 🤖 Multi-Agent Architecture
- 🧠 Autonomous Task Planning
- 📚 Retrieval-Augmented Generation (RAG)
- 📄 PDF Document Upload & Analysis
- 🔍 Semantic Search
- 📑 Automatic Report Generation
- ✅ Fact Verification
- 🧠 Long-Term Memory
- 📖 Citation & Reference Generation
- 🌐 FastAPI REST API
- 📊 Streamlit Dashboard
- 📥 PDF & DOCX Export
- 🐳 Docker Support

---

# 🏗️ Architecture

```
                User Query
                     │
                     ▼
             Planner Agent
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼              ▼
Research Agent   RAG Agent    Memory Agent
      │              │              │
      └──────────────┼──────────────┘
                     ▼
          Fact Verification Agent
                     │
                     ▼
           Summarization Agent
                     │
                     ▼
          Report Generator Agent
                     │
                     ▼
          Research Report (PDF)
```

---

# 🧩 AI Agents

## 🗂 Planner Agent

- Understands user queries
- Breaks research into tasks
- Coordinates all agents

---

## 🔍 Research Agent

- Searches external sources
- Retrieves research papers
- Collects articles and references

---

## 📚 RAG Agent

- Reads uploaded PDFs
- Splits documents into chunks
- Generates embeddings
- Retrieves relevant information using ChromaDB

---

## ✅ Fact Verification Agent

- Cross-checks information
- Detects conflicting statements
- Calculates confidence scores

---

## 🧠 Memory Agent

- Stores previous conversations
- Maintains research context
- Supports follow-up questions

---

## 📝 Summarization Agent

- Extracts important findings
- Removes redundant information
- Produces concise summaries

---

## 📄 Report Generator Agent

Creates a professional report including:

- Executive Summary
- Introduction
- Literature Review
- Findings
- Conclusion
- References

---

# ⚙️ Tech Stack

## Programming Language

- Python 3.11

## AI Frameworks

- LangGraph
- LangChain
- OpenAI API
- Google Gemini API

## Backend

- FastAPI
- Uvicorn

## Frontend

- Streamlit

## Vector Database

- ChromaDB

## Embeddings

- OpenAI Embeddings
- Gemini Embeddings

## Document Processing

- PyMuPDF
- pypdf

## Deployment

- Docker
- GitHub Actions
- Railway
- Render

---

# 📂 Project Structure

```
multi-agent-ai-research-assistant/

│── app/
│   │
│   ├── agents/
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── rag_agent.py
│   │   ├── verifier.py
│   │   ├── memory.py
│   │   ├── summarizer.py
│   │   └── report_generator.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── ui/
│   │   └── app.py
│   │
│   └── utils/
│
│── uploads/
│── reports/
│── tests/
│── requirements.txt
│── Dockerfile
│── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/multi-agent-ai-research-assistant.git
```

Move into the project

```bash
cd multi-agent-ai-research-assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

Start FastAPI

```bash
uvicorn app.api.routes:app --reload
```

Run Streamlit

```bash
streamlit run app/ui/app.py
```

---

# 💡 Example Query

```
Generate a research report on the impact of Artificial Intelligence in Healthcare with references from recent research papers.
```

---

# 📤 Example Output

```
Title

Artificial Intelligence in Healthcare

Executive Summary

Introduction

Current Applications

Benefits

Challenges

Future Scope

Conclusion

References
```

---

# 🌐 REST API

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /research | Generate research report |
| POST | /upload | Upload PDF documents |
| POST | /chat | Chat with AI |
| GET | /report | Download report |
| GET | /status | Check system status |

---

# 📈 Future Enhancements

- Voice-based research assistant
- Knowledge Graph visualization
- Multi-language support
- AI-powered presentation generation
- Real-time collaborative research
- Live web browsing
- APA / MLA / IEEE citation formats
- Image and video understanding

---

# 🎯 Learning Outcomes

This project demonstrates:

- Multi-Agent AI Systems
- Agentic AI
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- LangGraph
- LangChain
- LLM Integration
- FastAPI Development
- Streamlit Dashboard
- Docker Deployment
- REST API Development

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👩‍💻 Author

**Aastha Sheta**

AI & Machine Learning Undergraduate | AI Engineer | Full Stack AI Developer

If you found this project useful, don't forget to ⭐ the repository!
