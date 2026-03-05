import streamlit as st
from ocr import extract_text_from_pdf
from rag import build_vector_db, search
from llm import generate_answer
from report import generate_pdf_report

import os

st.set_page_config(
    page_title="AI Notes Assistant",
    layout="wide"
)

st.title("📚 AI Notes Assistant")

st.write("Upload handwritten notes and ask questions from them.")

# ---------------- SESSION MEMORY ---------------- #

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:

    with open("notes.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())

    st.success("PDF uploaded")

# ---------------- PROCESS NOTES ---------------- #

if st.button("Process Notes"):

    if os.path.exists("notes.pdf"):

        with st.spinner("Processing notes..."):

            pages = extract_text_from_pdf("notes.pdf")

            vector_db, texts = build_vector_db(pages)

            st.session_state.vector_db = vector_db
            st.session_state.texts = texts

        st.success("Notes processed")

# ---------------- CHAT INTERFACE ---------------- #

st.subheader("Chat with your notes")

question = st.text_input("Ask a question")

if st.button("Ask"):

    if "vector_db" not in st.session_state:

        st.warning("Process notes first")

    else:

        context = search(
            question,
            st.session_state.vector_db,
            st.session_state.texts
        )

        answer = generate_answer(question, context)

        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
            "sources": context
        })

# ---------------- DISPLAY CHAT ---------------- #

for chat in st.session_state.chat_history:

    st.markdown("### 🙋 Question")
    st.write(chat["question"])

    st.markdown("### 🤖 Answer")
    st.write(chat["answer"])

    st.markdown("### 📄 Sources")

    for c in chat["sources"]:
        st.write("- " + c)

    st.divider()

# ---------------- PDF REPORT ---------------- #

if st.button("Generate PDF Report"):

    path = generate_pdf_report(st.session_state.chat_history)

    with open(path, "rb") as f:
        st.download_button(
            label="Download Report",
            data=f,
            file_name="report.pdf",
            mime="application/pdf"
        )