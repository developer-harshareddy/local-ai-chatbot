

import streamlit as st
import requests

from llm_service import get_llm_response, MODEL_NAME


# ----------------------------------
# Page configuration
# ----------------------------------

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ----------------------------------
# System instructions
# ----------------------------------

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a helpful AI assistant specializing in "
        "Java, Spring Boot, Python, GenAI and fintech. "
        "Explain concepts clearly with practical examples."
    )
}


# ----------------------------------
# Initialize session state
# ----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [SYSTEM_MESSAGE]


# ----------------------------------
# Application heading
# ----------------------------------

st.title("🤖 Local AI Chatbot")

st.caption(f"Powered by Ollama | Model: {MODEL_NAME}")

st.info("Your conversations are handled by your local LLM.")


# ----------------------------------
# Sidebar
# ----------------------------------

with st.sidebar:
    st.header("Chat Settings")

    st.write("Model:", MODEL_NAME)

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = [SYSTEM_MESSAGE]
        st.rerun()


# ----------------------------------
# Display conversation history
# ----------------------------------

for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ----------------------------------
# Accept user input
# ----------------------------------

user_input = st.chat_input("Ask me anything...")

if user_input:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:
                answer = get_llm_response(
                    st.session_state.messages
                )

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.exceptions.RequestException as error:
                st.error(f"Could not communicate with Ollama: {error}")

            except (ValueError, KeyError) as error:
                st.error(f"Invalid response from Ollama: {error}")
