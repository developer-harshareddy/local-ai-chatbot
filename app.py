
import streamlit as st
import requests
import hashlib

from document_loader import extract_pdf_text
from database import (
    create_session,
    get_messages,
    save_message,
    list_sessions,
    delete_session
)
from llm_service import stream_llm_response, MODEL_NAME

from chunking import chunk_pages
from embeddings import EmbeddingService
from vector_store import VectorStore
from rag_service import RAGService
from tool_service import chat_with_tools

# --------------------------------------------------
# SYSTEM CONFIGURATION
# --------------------------------------------------

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a helpful assistant specializing in Java, Spring Boot, "
        "Python, GenAI and fintech. Explain clearly with practical examples."
    )
}

st.set_page_config(
    page_title="Local AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 Local AI Chatbot")
st.caption(f"Local Ollama model: {MODEL_NAME}")


# --------------------------------------------------
# CACHED AI SERVICES
# --------------------------------------------------

@st.cache_resource
def get_embedding_service():
    return EmbeddingService()


@st.cache_resource
def get_vector_store():
    return VectorStore()

@st.cache_resource
def get_rag_service():
    return RAGService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store()
    )

# --------------------------------------------------
# SESSION INITIALIZATION
# --------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()

if "messages" not in st.session_state:
    st.session_state.messages = get_messages(
        st.session_state.session_id
    )

if "indexed_documents" not in st.session_state:
    st.session_state.indexed_documents = {}


# --------------------------------------------------
# SIDEBAR - CONVERSATION MANAGEMENT
# --------------------------------------------------

with st.sidebar:

    st.subheader("Conversations")

    if st.button(
        "🤖 New conversation",
        use_container_width=True
    ):
        st.session_state.session_id = create_session()
        st.session_state.messages = []
        st.rerun()

    st.caption("Saved conversations")

    for item in list_sessions():

        sid = str(item["id"])

        label = (
            f"{sid[:8]}… "
            f"({item['message_count']} messages)"
        )

        if st.button(
            label,
            key=f"open_{sid}",
            use_container_width=True
        ):
            st.session_state.session_id = sid
            st.session_state.messages = get_messages(sid)
            st.rerun()

    if st.button(
        "Delete current conversation",
        use_container_width=True
    ):
        delete_session(st.session_state.session_id)
        st.session_state.session_id = create_session()
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# CHAT HISTORY DISPLAY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# --------------------------------------------------
# CHAT WITH LOCAL OLLAMA MODEL + RAG
# --------------------------------------------------
chat_mode = st.selectbox(
    "Choose Chatbot Mode",
    options=[
        "Normal Chat",
        "Document RAG",
        "FinTech AI Tools"
    ],
    index=0
)

prompt = st.chat_input("Ask me anything…")

if prompt:

    # Save user message.
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    save_message(
        st.session_state.session_id,
        "user",
        prompt
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        answer = ""
        results = []
        llm_messages = []

        try:

            # --------------------------------------
            # STEP 1: PREPARE THE RESPONSE
            # --------------------------------------

            if chat_mode == "Document RAG":

                with st.spinner("Retrieving document context..."):

                    rag_service = get_rag_service()

                    results = rag_service.retrieve_context(
                        question=prompt,
                        top_k=3
                    )

                if results:

                    llm_messages = rag_service.build_rag_messages(
                        question=prompt,
                        results=results
                    )

                else:

                    answer = (
                        "I could not find sufficient information "
                        "in the uploaded documents. Please upload "
                        "and index a relevant PDF first."
                    )

            elif chat_mode == "FinTech AI Tools":

                with st.spinner("Processing FinTech request..."):

                    answer = chat_with_tools(prompt)

            else:

                # Existing normal chatbot behavior.
                llm_messages = (
                    [SYSTEM_MESSAGE] +
                    st.session_state.messages
                )

            # --------------------------------------
            # STEP 2: GENERATE RESPONSE
            # --------------------------------------

            if chat_mode != "FinTech AI Tools" and not answer:

                answer_parts = []

                for piece in stream_llm_response(llm_messages):

                    answer_parts.append(piece)

                    placeholder.markdown(
                        "".join(answer_parts) + "▌"
                    )

                answer = "".join(answer_parts)

            # --------------------------------------
            # STEP 3: ADD RAG SOURCE REFERENCES
            # --------------------------------------

            if chat_mode == "Document RAG" and results:

                sources = []

                for result in results:

                    metadata = result.get("metadata", {})

                    source = metadata.get("source", "Unknown")
                    page = metadata.get("page", "Unknown")

                    reference = f"- {source}, Page {page}"

                    if reference not in sources:
                        sources.append(reference)

                if sources:

                    answer += (
                        "\n\n**Sources:**\n" +
                        "\n".join(sources)
                    )

            # --------------------------------------
            # STEP 4: DISPLAY AND SAVE RESPONSE
            # --------------------------------------

            placeholder.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

            save_message(
                st.session_state.session_id,
                "assistant",
                answer
            )

        except Exception as exc:

            error_message = (
                f"Sorry, something went wrong while processing "
                f"your request: {exc}"
            )

            placeholder.error(error_message)

# --------------------------------------------------
# PDF UPLOAD AND DOCUMENT INDEXING
# --------------------------------------------------

st.divider()

st.subheader("📄 Document Knowledge Base")

st.write(
    "Upload a PDF and index its contents for semantic search."
)

uploaded_pdf = st.file_uploader(
    "Upload a PDF",
    type=["pdf"],
    key="pdf_uploader"
)


if uploaded_pdf:

    # Read the uploaded file content.
    pdf_bytes = uploaded_pdf.getvalue()

    # Generate a stable ID based on file contents.
    document_id = hashlib.sha256(
        pdf_bytes
    ).hexdigest()

    source_name = uploaded_pdf.name

    st.write(f"**Selected document:** {source_name}")

    try:

        # ------------------------------------------
        # STEP 1: PDF EXTRACTION
        # ------------------------------------------

        pages = extract_pdf_text(uploaded_pdf)

        st.write(
            f"Extracted text from {len(pages)} pages."
        )

        if not pages:

            st.warning(
                "No readable text was found in this PDF. "
                "It may be a scanned document requiring OCR."
            )

        else:

            extracted = "\n\n".join(
                f"[Page {p['page']}]\n{p['text']}"
                for p in pages
            )

            with st.expander("Preview extracted PDF text"):

                st.text_area(
                    "Extraction preview",
                    extracted,
                    height=250
                )

            # --------------------------------------
            # STEP 2: INDEX DOCUMENT
            # --------------------------------------

            already_indexed = (
                document_id
                in st.session_state.indexed_documents
            )

            if already_indexed:

                st.success(
                    "This document is already indexed "
                    "in the current Streamlit session."
                )

            elif st.button(
                "🚀 Index PDF in Vector Database",
                type="primary"
            ):

                with st.spinner(
                    "Processing document and generating embeddings..."
                ):

                    # Create text chunks.
                    chunks = chunk_pages(
                        pages,
                        chunk_size=1000,
                        overlap=200,
                        source=source_name
                    )

                    if not chunks:

                        st.warning(
                            "No text chunks were generated."
                        )

                    else:

                        # Prefix IDs with the document hash.
                        # This prevents different PDFs from
                        # overwriting each other's chunks.

                        for chunk in chunks:

                            chunk["id"] = (
                                f"{document_id[:16]}-"
                                f"{chunk['id']}"
                            )

                            chunk["metadata"]["document_id"] = (
                                document_id
                            )

                        # Extract chunk text.
                        chunk_texts = [
                            chunk["text"]
                            for chunk in chunks
                        ]

                        # Generate embeddings.
                        embedding_service = (
                            get_embedding_service()
                        )

                        embeddings = (
                            embedding_service.generate_embeddings(
                                chunk_texts
                            )
                        )

                        # Store chunks and embeddings.
                        vector_store = get_vector_store()

                        vector_store.upsert_chunks(
                            chunks,
                            embeddings
                        )

                        # Remember this document in the
                        # current Streamlit session.
                        st.session_state.indexed_documents[
                            document_id
                        ] = {
                            "filename": source_name,
                            "chunk_count": len(chunks)
                        }

                        st.success(
                            f"Successfully indexed {source_name}!"
                        )

                        st.write(
                            f"Generated chunks: {len(chunks)}"
                        )

                        st.write(
                            f"Generated embeddings: {len(embeddings)}"
                        )

                        st.write(
                            "Embedding dimensions: 384"
                        )

                        st.write(
                            "Stored in ChromaDB successfully."
                        )

                        st.write(
                            "Total chunks in vector database:",
                            vector_store.get_total_chunks()
                        )

    except Exception as exc:

        st.error(
            f"Document processing failed: {exc}"
        )


# --------------------------------------------------
# SEMANTIC SEARCH FROM STREAMLIT
# --------------------------------------------------

st.divider()

st.subheader("🔎 Search Your Uploaded Documents")

st.write(
    "Ask a question and retrieve relevant information "
    "from documents stored in ChromaDB."
)

search_question = st.text_input(
    "Enter your document-related question",
    placeholder="Example: How can a customer transfer money?"
)

top_k = st.slider(
    "Number of matching chunks",
    min_value=1,
    max_value=5,
    value=3
)

if st.button("Search Documents", type="primary"):

    if not search_question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Searching document knowledge base..."):

                # Generate query embedding.
                embedding_service = get_embedding_service()

                query_embedding = (
                    embedding_service.generate_embedding(
                        search_question
                    )
                )

                # Search ChromaDB.
                vector_store = get_vector_store()

                results = vector_store.search(
                    query_embedding,
                    top_k=top_k
                )

            if not results:

                st.warning(
                    "No indexed document chunks were found. "
                    "Please upload and index a PDF first."
                )

            else:

                st.success(
                    f"Found {len(results)} relevant document chunks."
                )

                for index, result in enumerate(results, start=1):

                    metadata = result["metadata"]

                    with st.expander(
                        f"Result {index} | "
                        f"Page {metadata.get('page', 'Unknown')}"
                    ):

                        st.markdown("**Source document:**")

                        st.write(
                            metadata.get("source", "Unknown")
                        )

                        st.markdown("**Retrieved content:**")

                        st.write(result["text"])

                        st.markdown("**Chunk ID:**")

                        st.code(result["id"])

                        st.markdown("**Cosine distance:**")

                        st.write(
                            round(result["distance"], 4)
                        )

        except Exception as exc:

            st.error(
                f"Document search failed: {exc}"
            )
