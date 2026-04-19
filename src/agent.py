import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

class AgenticRAG:
    def __init__(self, retriever):
        self.retriever = retriever
        # Consistency for API key
        if "GEMINI_API_KEY" in os.environ and "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]
            
        # Using Gemini Flash Latest for high RPM (15 Requests Per Minute) 
        # specifically to avoid 429 errors on the free tier.
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest", 
            temperature=0,
            max_retries=3
        )
        self.history = []  # List of tuples: (user_query, ai_response)
        self.max_history = 3

    def _format_history(self):
        if not self.history:
            return "No previous conversation."
        formatted = ""
        for i, (q, a) in enumerate(self.history):
            formatted += f"User: {q}\nSystem Element: {a}\n\n"
        return formatted
        
    def _route_query(self, query: str) -> bool:
        """Determines if the query requires querying the document database."""
        routing_prompt = f"""
You are a decision-making routing agent for a retrieval-augmented generation system.
Your job is to determine if a user's question requires searching an internal document database for NEW information, or if it can be handled using general knowledge or the existing conversation history.

Examples that REQUIRE searching the database (YES):
- "What does the document say about project X?"
- "Summarize the provided text."
- "What are the isotope generators mentioned in the report?" (Specific technical detail not in memory)
- "Tell me more about the Harmony Directives." (Seeking more detail than previously given)

Examples that DO NOT require searching (NO):
- "What is machine learning?" (General knowledge)
- "Explain that in simpler terms." (Transforming the PREVIOUS answer already in history)
- "Can you rephrase your last response?" (Transformation of memory)
- "What did YOU just say?" (Memory check)
- "Who are you?" (Identity)

Conversation History:
{self._format_history()}

Current User Query: {query}

Does this query require searching the internal document database for NEW context? 
Answer 'NO' if the user is simply asking to simplify, rephrase, or explain the PREVIOUS answer already present in the history.
Answer ONLY with the word 'YES' or 'NO'. 
"""
        response = self.llm.invoke([HumanMessage(content=routing_prompt)])
        decision = response.content.strip().upper()
        # If the LLM generates "YES", return True, else False
        return "YES" in decision

    def ask(self, query: str):
        """Processes the query using either RAG or direct knowledge, optimized for quota."""
        # Consolidated Routing & Direct Answer Prompt
        # This saves 1 API call by answering in-place if no RAG is needed.
        routing_and_general_prompt = f"""
You are an intelligent assistant. 
1. Determine if this question requires searching an internal document database for NEW information (e.g. details about Project Nexus, Rover protocols, specific technical reports).
2. If it DOES need a search, respond ONLY with the word 'YES'.
3. If it DOES NOT need a search (general knowledge, greetings, or rephrasing the history):
   - Provide the final answer immediately.
   - START your response with [MEMORY] if you are using the conversation history (like simplifying or follow-up).
   - START your response with [GENERAL] if it is general knowledge.

Conversation History:
{self._format_history()}

User Question: {query}
Answer:"""

        response = self.llm.invoke([HumanMessage(content=routing_and_general_prompt)])
        content = response.content.strip()
        
        sources = []
        answer = ""
        reasoning_type = "GENERAL"

        if content.upper() == "YES":
            reasoning_type = "RAG"
            # Phase 2: Retrieve context
            docs = self.retriever.invoke(query)
            context = "\n\n".join([doc.page_content for doc in docs])
            for doc in docs:
                sources.append(doc.metadata.get('source', 'Unknown Document'))
            
            # Phase 2: Generate grounded answer (Call #2)
            rag_prompt = f"""
You are an intelligent assistant. Use the provided context and history to answer.
If the answer is not in the context, say "I cannot answer this based on the provided documents."

Conversation History:
{self._format_history()}

Document Context:
{context}

User Question: {query}
Answer:"""
            response = self.llm.invoke([HumanMessage(content=rag_prompt)])
            answer = response.content
        else:
            # Answer was already generated in Call #1
            # Check for tags
            if content.startswith("[MEMORY]"):
                reasoning_type = "MEMORY"
                answer = content.replace("[MEMORY]", "").strip()
            elif content.startswith("[GENERAL]"):
                reasoning_type = "GENERAL"
                answer = content.replace("[GENERAL]", "").strip()
            else:
                # Fallback if model forgets tags
                answer = content
            
        # Maintain Memory
        self.history.append((query, answer))
        if len(self.history) > self.max_history:
            self.history.pop(0)
            
        return {
            "answer": answer,
            "reasoning_type": reasoning_type,
            "sources": list(set(sources))
        }
