"""
Streamlit Dashboard for the Multi-Agent AI Research Assistant.

Run with:
    streamlit run ui/app.py

Talks to the FastAPI backend over HTTP, so the API server must be running
(see README for `uvicorn app.main:app`).
"""
import os
import requests
import streamlit as st

API_BASE = os.environ.get("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="Multi-Agent Research Assistant", page_icon="🔎", layout="wide")

if "session_id" not in st.session_state:
    st.session_state.session_id = "streamlit-session"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_report_id" not in st.session_state:
    st.session_state.last_report_id = None

st.title("🔎 Multi-Agent AI Research Assistant")
st.caption("Planner → Research → RAG → Fact-Check → Memory → Summarize → Report")

tab_research, tab_upload, tab_chat = st.tabs(["📑 New Research", "📤 Upload Documents", "💬 Follow-up Chat"])

# ---------------------------------------------------------------- Research
with tab_research:
    st.subheader("Generate a research report")
    query = st.text_area(
        "Research query",
        placeholder="e.g. Generate a research report on the impact of Generative AI in Healthcare",
        height=90,
    )
    col1, col2 = st.columns([1, 4])
    with col1:
        run_clicked = st.button("Run Research", type="primary")

    if run_clicked:
        if not query.strip():
            st.warning("Enter a research query first.")
        else:
            with st.spinner("Agents are working: planning → researching → retrieving → verifying → summarizing → writing report..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/research",
                        json={"query": query, "session_id": st.session_state.session_id},
                        timeout=300,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                except Exception as e:
                    st.error(f"Request failed: {e}")
                    data = None

            if data:
                st.session_state.last_report_id = data.get("report_id")
                st.success("Report generated.")

                st.markdown("### Research Objectives")
                for obj in data.get("objectives") or []:
                    st.markdown(f"- {obj}")

                st.markdown("### Fact-Verification Notes")
                st.info(data.get("verification_note") or "N/A")

                st.markdown("### Summary")
                st.write(data.get("summary") or "N/A")

    if st.session_state.last_report_id:
        st.markdown("### Download Report")
        rid = st.session_state.last_report_id
        c1, c2, c3 = st.columns(3)
        for col, fmt, label in zip((c1, c2, c3), ("md", "docx", "pdf"), ("Markdown", "Word (.docx)", "PDF")):
            with col:
                try:
                    file_resp = requests.get(f"{API_BASE}/report/{rid}/{fmt}", timeout=60)
                    if file_resp.status_code == 200:
                        st.download_button(
                            f"⬇️ {label}",
                            data=file_resp.content,
                            file_name=f"{rid}.{fmt}",
                            mime="application/octet-stream",
                            key=f"dl_{fmt}",
                        )
                except Exception:
                    st.caption(f"{label} not available yet.")

# ------------------------------------------------------------------ Upload
with tab_upload:
    st.subheader("Upload research PDFs for RAG retrieval")
    uploaded = st.file_uploader("Choose a PDF", type=["pdf"])
    if uploaded and st.button("Ingest into Vector Store"):
        with st.spinner("Extracting text, chunking, and embedding..."):
            try:
                files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
                resp = requests.post(f"{API_BASE}/upload", files=files, timeout=120)
                resp.raise_for_status()
                result = resp.json()
                st.success(f"Indexed {result['chunks_indexed']} chunks from {result['filename']}.")
            except Exception as e:
                st.error(f"Upload failed: {e}")

# -------------------------------------------------------------------- Chat
with tab_chat:
    st.subheader("Ask follow-up questions")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_msg = st.chat_input("Ask a follow-up question about your research...")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.write(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/chat",
                        json={"message": user_msg, "session_id": st.session_state.session_id},
                        timeout=120,
                    )
                    resp.raise_for_status()
                    answer = resp.json()["answer"]
                except Exception as e:
                    answer = f"Error: {e}"
                st.write(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

st.sidebar.header("⚙️ Backend")
st.sidebar.write(f"API: `{API_BASE}`")
try:
    h = requests.get(f"{API_BASE}/health", timeout=3).json()
    st.sidebar.success(f"Connected — provider: {h.get('llm_provider')}")
except Exception:
    st.sidebar.error("Backend not reachable. Start it with:\n`uvicorn app.main:app --reload`")
