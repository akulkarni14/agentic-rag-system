import streamlit as st
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from document_processor import setup_retriever
from agent import AgenticRAG

st.set_page_config(
    page_title="Agentic RAG Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    *, html, body, [class*="css"] {
        font-family: 'Sora', sans-serif !important;
    }

    :root {
        --bg-base:      #05070f;
        --bg-surface:   #0b0f1e;
        --bg-elevated:  #111827;
        --border:       rgba(139, 92, 246, 0.12);
        --border-hover: rgba(139, 92, 246, 0.35);
        --accent-1:     #8b5cf6;
        --accent-2:     #a78bfa;
        --accent-3:     #c4b5fd;
        --accent-glow:  rgba(139, 92, 246, 0.22);
        --text-primary: #ede9fe;
        --text-muted:   #6b7280;
        --text-dim:     #374151;
        --green:        #34d399;
        --indigo:       #818cf8;
    }

    .stApp {
        background: var(--bg-base) !important;
        color: var(--text-primary) !important;
    }

    /* Violet glow top-right */
    .stApp::after {
        content: '';
        position: fixed;
        top: -25vh;
        right: -15vw;
        width: 65vw;
        height: 65vh;
        background: radial-gradient(ellipse, rgba(139,92,246,0.09) 0%, transparent 68%);
        pointer-events: none;
        z-index: 0;
    }

    /* Indigo glow bottom-left */
    .stApp::before {
        content: '';
        position: fixed;
        bottom: -20vh;
        left: -10vw;
        width: 55vw;
        height: 55vh;
        background: radial-gradient(ellipse, rgba(99,102,241,0.06) 0%, transparent 65%);
        pointer-events: none;
        z-index: 0;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--bg-surface) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] > div {
        padding: 2rem 1.3rem 1.5rem !important;
    }

    /* ── Headings ── */
    h1 {
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(130deg, #c4b5fd 0%, #a78bfa 45%, #818cf8 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 0.3rem !important;
    }
    h2, h3 {
        color: var(--text-muted) !important;
        font-size: 0.67rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.13em !important;
        text-transform: uppercase !important;
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 20px 22px !important;
        margin-bottom: 12px !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    }
    [data-testid="stChatMessage"]:hover {
        border-color: var(--border-hover) !important;
        box-shadow: 0 4px 40px var(--accent-glow) !important;
    }

    /* ── Chat input ── */
    [data-testid="stChatInput"] textarea {
        background: var(--bg-elevated) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        color: var(--text-primary) !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.9rem !important;
        transition: border-color 0.25s, box-shadow 0.25s !important;
        caret-color: var(--accent-2) !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--accent-1) !important;
        box-shadow: 0 0 0 3px var(--accent-glow) !important;
        outline: none !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--text-dim) !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, rgba(139,92,246,0.14), rgba(99,102,241,0.08)) !important;
        color: var(--accent-3) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        font-family: 'Sora', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        padding: 0.55rem 1rem !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(139,92,246,0.28), rgba(99,102,241,0.18)) !important;
        border-color: var(--accent-1) !important;
        color: #fff !important;
        box-shadow: 0 0 22px var(--accent-glow) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: rgba(139,92,246,0.04) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        margin-top: 12px !important;
    }
    [data-testid="stExpander"] summary {
        color: var(--text-muted) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stExpander"] summary:hover { color: var(--accent-3) !important; }

    hr {
        border: none !important;
        border-top: 1px solid var(--border) !important;
        margin: 1.4rem 0 !important;
    }

    [data-testid="stAlert"] {
        background: var(--bg-elevated) !important;
        border-color: var(--border) !important;
        border-radius: 12px !important;
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.28); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(139,92,246,0.48); }

    /* ── Custom components ── */
    .sidebar-logo-title {
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        background: linear-gradient(130deg, #c4b5fd, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .sidebar-logo-sub {
        font-size: 0.67rem;
        color: #2d3748;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 500;
        margin-top: 3px;
    }

    .file-chip {
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 8px 12px;
        background: rgba(139,92,246,0.06);
        border: 1px solid rgba(139,92,246,0.15);
        border-radius: 9px;
        margin-bottom: 7px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #a78bfa;
        transition: background 0.2s, border-color 0.2s;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }
    .file-chip:hover {
        background: rgba(139,92,246,0.12);
        border-color: rgba(139,92,246,0.3);
        color: #c4b5fd;
    }

    .sysinfo-block {
        margin-top: 8px;
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }
    .sysinfo-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        font-size: 0.78rem;
        border-bottom: 1px solid rgba(139,92,246,0.07);
    }
    .sysinfo-row:last-child { border-bottom: none; }
    .sysinfo-label { color: #4b5563; font-weight: 500; }
    .sysinfo-value {
        color: #9ca3af;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        background: rgba(139,92,246,0.08);
        padding: 2px 8px;
        border-radius: 5px;
    }

    .retrieval-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        margin-top: 16px;
        padding: 6px 14px 6px 10px;
        border-radius: 100px;
        font-size: 0.76rem;
        font-weight: 500;
        border: 1px solid;
        backdrop-filter: blur(4px);
    }
    .pill-rag {
        background: rgba(52,211,153,0.07);
        border-color: rgba(52,211,153,0.25);
        color: #6ee7b7;
    }
    .pill-no {
        background: rgba(129,140,248,0.07);
        border-color: rgba(129,140,248,0.25);
        color: #a5b4fc;
    }
    .pill-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .dot-rag { background: #34d399; box-shadow: 0 0 7px #34d399; }
    .dot-no  { background: #818cf8; box-shadow: 0 0 7px #818cf8; }
    .pill-tag { color: #6b7280; font-weight: 400; }

    .source-item {
        display: flex;
        align-items: center;
        gap: 9px;
        padding: 7px 12px;
        background: rgba(139,92,246,0.05);
        border-left: 2px solid rgba(139,92,246,0.4);
        border-radius: 0 7px 7px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #9ca3af;
        margin-bottom: 6px;
    }

    .welcome-sub {
        color: #374151;
        font-size: 0.87rem;
        font-weight: 300;
        margin-top: 4px;
        margin-bottom: 2rem;
        padding-bottom: 1.2rem;
        border-bottom: 1px solid var(--border);
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)


# ── Helper ───────────────────────────────────────────────────────────────────
def retrieval_pill(reasoning_type):
    cfg = {
        "RAG":     ("Yes, context searched",       "pill-rag", "dot-rag"),
        "MEMORY":  ("No, used memory",             "pill-no",  "dot-no"),
        "GENERAL": ("No, general knowledge used",  "pill-no",  "dot-no"),
    }
    label, pill_cls, dot_cls = cfg.get(reasoning_type, ("Processed", "pill-no", "dot-no"))
    st.markdown(f"""
        <div class='retrieval-pill {pill_cls}'>
            <span class='pill-dot {dot_cls}'></span>
            <span class='pill-tag'>Retrieval Used:&nbsp;</span>
            <span>{label}</span>
        </div>
    """, unsafe_allow_html=True)


# ── Init ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_agent():
    load_dotenv()
    data_dir = os.path.join(os.getcwd(), "data")
    db_dir   = os.path.join(os.getcwd(), "chroma_db")
    retriever = setup_retriever(data_dir=data_dir, persist_directory=db_dir)
    return AgenticRAG(retriever=retriever)

try:
    agent = get_agent()
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style='margin-bottom:1.6rem;'>
            <div class='sidebar-logo-title'>⚡ RAG Assistant</div>
            <div class='sidebar-logo-sub'>Agentic &nbsp;·&nbsp; Intelligent</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📁 Indexed Documents")

    data_path = os.path.join(os.getcwd(), "data")
    if os.path.exists(data_path):
        files = [f for f in os.listdir(data_path) if f.endswith(('.pdf', '.txt'))]
        if files:
            for f in files:
                icon = "📄" if f.endswith('.txt') else "📑"
                st.markdown(f"<div class='file-chip'>{icon}&nbsp; {f}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#374151;font-size:0.82rem;'>No documents indexed yet.</span>",
                        unsafe_allow_html=True)
    else:
        st.info("No `data/` folder found.")

    st.markdown("---")
    st.subheader("⚙️ System Info")
    st.markdown("""
        <div class='sysinfo-block'>
            <div class='sysinfo-row'>
                <span class='sysinfo-label'>🧠 Model</span>
                <span class='sysinfo-value'>gemini-flash-latest</span>
            </div>
            <div class='sysinfo-row'>
                <span class='sysinfo-label'>🔢 Embeddings</span>
                <span class='sysinfo-value'>Embeddings 001</span>
            </div>
            <div class='sysinfo-row'>
                <span class='sysinfo-label'>🗄️ Vector DB</span>
                <span class='sysinfo-value'>ChromaDB</span>
            </div>
            <div class='sysinfo-row'>
                <span class='sysinfo-label'>🔀 Routing</span>
                <span class='sysinfo-value'>Agentic</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️  Clear Conversation"):
        st.session_state.messages = []
        agent.history = []
        st.rerun()


# ── Main ─────────────────────────────────────────────────────────────────────
st.title("Agentic RAG Assistant")
st.markdown(
    "<p class='welcome-sub'>Ask anything — I'll intelligently decide whether to search your private documents, "
    "recall from conversation memory, or draw on general knowledge.</p>",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "meta" in message:
            meta = message["meta"]
            retrieval_pill(meta["reasoning_type"])
            if meta["reasoning_type"] == "RAG" and meta["sources"]:
                with st.expander("📚 View Sources"):
                    for s in meta["sources"]:
                        name = s.split(os.sep)[-1] if os.sep in s else s
                        st.markdown(f"<div class='source-item'>📎 &nbsp;{name}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Ask me anything…"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            try:
                result = agent.ask(prompt)
                st.markdown(result["answer"])
                retrieval_pill(result["reasoning_type"])

                if result["reasoning_type"] == "RAG" and result["sources"]:
                    with st.expander("📚 View Sources"):
                        for s in result["sources"]:
                            name = s.split(os.sep)[-1] if os.sep in s else s
                            st.markdown(f"<div class='source-item'>📎 &nbsp;{name}</div>", unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "meta": {
                        "reasoning_type": result["reasoning_type"],
                        "sources": result["sources"],
                    },
                })

            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    st.warning("⚠️ **API Rate Limit Hit!** Please wait 60 seconds and try again. & If RPD Limit is hit use differnt aistudio.google.com Account & Try Again ")
                else:
                    st.error(f"Error: {e}")