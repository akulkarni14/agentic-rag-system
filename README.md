# Agentic RAG System

A Retrieval-Augmented Generation (RAG) system with **agentic decision-making** that intelligently chooses between document retrieval and general knowledge responses.

---

## 🎯 Objective

Build a system that:

* Uses RAG for document-based queries
* Skips retrieval for general knowledge
* Uses memory for follow-up questions

---

## ⚙️ Setup Instructions (Detailed)

### 1. Clone the Repository

```bash
git clone <repo-url>
cd agentic_rag
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

* **Windows**

```bash
venv\Scripts\activate
```

* **Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

(Optional but recommended)

```bash
pip install --upgrade pip
```

---

### 4. Configure Environment Variables

1. Create a `.env` file in the root directory
2. Add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

👉 Get your API key from: https://aistudio.google.com

---

### 5. Documents

* Sample documents are already included in the `data/` folder.
* You can add your own `.pdf` or `.txt` files to this folder:

```text
data/
├── sample.txt
├── rover_report.pdf
```

* Restart the application to process and index any new documents.

---

### 6. Run the System

```bash
python src/main.py
```

---

## ▶️ How to Use (CLI - Main)

Example interaction:

```text
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

> Note: CLI is the primary interface as per assignment requirements. UI is provided for better demonstration.

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

---

### 🔍 LLM Choice

Google Gemini was used for its easy API setup, good performance, and seamless LangChain integration.
Ollama was avoided due to local setup and resource requirements.
OpenAI was not used to keep the project free and simple without billing setup.

---

### 🔍 Vector DB Choice

ChromaDB was chosen for its lightweight setup and local persistence.
Cloud databases were avoided to keep the system simple and self-contained.

---

### 🔍 Routing Strategy

Prompt-based routing was selected for flexibility and better decision-making.
Rule-based logic was avoided as it is rigid and less scalable.

---

### 🔍 Memory Design

A sliding window (last 3 interactions) is used for simplicity and efficiency.
Full conversation memory was avoided to reduce context size and cost.

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
