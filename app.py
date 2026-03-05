import streamlit as st
import os

from ocr import extract_text_from_pdf
from rag import build_vector_db, search
from llm import generate_answer

st.set_page_config(
    page_title="AI Notes Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("📚 Handwritten Notes AI Assistant")
st.write("Upload handwritten notes and ask questions from them.")

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.header("Upload Notes")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="pdf_uploader"
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        with open("notes.pdf", "wb") as f:
            f.write(file_bytes)

        st.success("PDF uploaded successfully!")

    process_button = st.button("Process Notes")

    if process_button:

        if os.path.exists("notes.pdf"):

            with st.spinner("Running OCR and building RAG database..."):

                pages = extract_text_from_pdf("notes.pdf")

                vector_db, texts = build_vector_db(pages)

                st.session_state["vector_db"] = vector_db
                st.session_state["texts"] = texts

            st.success("Notes processed successfully!")

        else:
            st.error("Please upload a PDF first!")

    st.markdown("---")
    st.write("Built for GenAI Hackathon")

# ---------------- MAIN PAGE ---------------- #

col1, col2 = st.columns([2, 3])

with col1:

    st.subheader("Ask a Question")

    question = st.text_area("Type your question")

    ask_button = st.button("Ask AI")

with col2:

    st.subheader("AI Answer")

    if ask_button:

        if "vector_db" not in st.session_state:
            st.error("Please process notes first!")
        else:

            context = search(
                question,
                st.session_state["vector_db"],
                st.session_state["texts"]
            )

            answer = generate_answer(question, context)

            st.write(answer)

            st.subheader("Source Notes")

            for c in context:
                st.write(c)