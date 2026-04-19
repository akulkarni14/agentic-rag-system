# Agentic RAG System

A Retrieval-Augmented Generation (RAG) system with **agentic decision-making** that intelligently chooses between document retrieval and general knowledge responses.

---

## 🎯 Objective

Build a system that:

* Uses RAG for document-based queries
* Skips retrieval for general knowledge
* Uses memory for follow-up questions

---

## ⚙️ Setup Instructions

1. Clone the repository:

```bash
git clone <repo-url>
cd agentic_rag
```

2. Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment:
   Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ How to Run (CLI - Main)

```bash
python src/main.py
```

### Example

```
You: Summarize the document
→ Retrieval Used: Yes

You: What is machine learning?
→ Retrieval Used: No

You: Explain that in simpler terms
→ Retrieval Used: No (uses memory)
```

---

## 💻 Optional UI (Additional)

```bash
streamlit run src/app.py
```

---

## 🧠 Approach / Design Decisions

### 1. RAG Pipeline

* Documents are loaded, chunked, and embedded
* Stored in ChromaDB
* Top-K relevant chunks retrieved

---

### 2. Agentic Routing (Core Feature)

* System decides:

  * **Use RAG** → document-based queries
  * **Skip RAG** → general knowledge or follow-ups
* Implemented using prompt-based decision logic

---

### 3. Memory Handling

* Maintains last **3 interactions**
* Used for:

  * Follow-up queries
  * Simplification / rephrasing

---

### 4. LLM Usage

* Context passed only when needed
* Avoids unnecessary retrieval → improves efficiency

---

## 🏗️ Architecture

* **LLM**: Google Gemini
* **Vector DB**: ChromaDB
* **Framework**: LangChain
* **Memory**: Sliding window (3 turns)

🔍 LLM Choice :- 
Google Gemini was used for its easy API setup, good performance, and seamless LangChain integration.
Ollama was not used due to local setup and resource requirements.
OpenAI was avoided to keep the project free and simple without billing setup.

🔍 Vector DB Choice :- 
ChromaDB was used for its lightweight setup and local persistence.
Avoided cloud DBs to keep the system simple and self-contained.

🔍 Routing Strategy :- 
Prompt-based routing was chosen for flexibility and better decision-making.
Rule-based logic was avoided as it is rigid and less scalable.

🔍 Memory Design :- 
Sliding window (last 3 interactions) used for simplicity and efficiency.
Full conversation memory avoided to reduce context size and cost.

---

## ⚠️ Limitations

* Requires manual deletion of `chroma_db` to refresh documents
* Limited memory (only last 3 interactions stored)
* Retrieval uses basic similarity (no reranking)
* Depends on external API availability

---

## 📌 Key Highlights

* ✅ Correct RAG implementation
* ✅ Agentic decision-making (not always retrieving)
* ✅ Proper memory handling
* ✅ Clean modular structure

---

## 🚀 Future Improvements

* Add semantic reranking
* Expand memory using summarization
* Support multiple APIs (OpenAI / local models)

---
