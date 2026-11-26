
import streamlit as st
import requests

from document_loader import extract_pdf_text
from database import (
    create_session, get_messages, save_message,
    list_sessions, delete_session
)
from llm_service import stream_llm_response, MODEL_NAME
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a helpful assistant specializing in Java, Spring Boot, "
        "Python, GenAI and fintech. Explain clearly with practical examples."
    )
}

st.set_page_config(page_title="Local AI Chatbot", page_icon="🤖")
st.title("🤖 Local AI Chatbot")
st.caption(f"Local Ollama model: {MODEL_NAME}")

# Create one session ID for this Streamlit browser session.
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()
if "messages" not in st.session_state:
    st.session_state.messages = get_messages(st.session_state.session_id)

with st.sidebar:
    st.subheader("Conversations")
    if st.button("🤖 New conversation", use_container_width=True):
        st.session_state.session_id = create_session()
        st.session_state.messages = []
        st.rerun()
    st.caption("Saved conversations")
    for item in list_sessions():
        sid = str(item["id"])
        label = f"{sid[:8]}… ({item['message_count']} messages)"
        if st.button(label, key=f"open_{sid}", use_container_width=True):
            st.session_state.session_id = sid
            st.session_state.messages = get_messages(sid)
            st.rerun()
    if st.button("Delete current conversation", use_container_width=True):
        delete_session(st.session_state.session_id)
        st.session_state.session_id = create_session()
        st.session_state.messages = []
        st.rerun()

# Display the selected conversation.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
prompt = st.chat_input("Ask me anything…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_message(st.session_state.session_id, "user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)
    llm_messages = [SYSTEM_MESSAGE] + st.session_state.messages
    
    with st.chat_message("assistant"):
        with st.spinner("The local model is thinking…"):
            answer_parts = []
            placeholder = st.empty()
            try:
                for piece in stream_llm_response(llm_messages):
                    answer_parts.append(piece)
                    placeholder.markdown("".join(answer_parts) + "▌")
                    answer = "".join(answer_parts)
                    placeholder.markdown(answer)
                    save_message(st.session_state.session_id, "assistant", answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
            except requests.exceptions.RequestException as exc:
                st.error(f"Ollama request failed: {exc}")

uploaded_pdf = st.file_uploader("Upload a PDF", type=["pdf"])
if uploaded_pdf:
    pages = extract_pdf_text(uploaded_pdf)
    extracted = "\n\n".join(
        f"[Page {p['page']}]\n{p['text']}" for p in pages
    )
    st.write(f"Extracted text from {len(pages)} pages.")
    st.text_area("Extraction preview", extracted, height=250)