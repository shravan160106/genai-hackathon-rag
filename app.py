import streamlit as st
import os

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
        st.write("File ready for processing")

    process_button = st.button("Process Notes")

    if process_button:

        if os.path.exists("notes.pdf"):
            st.success("Notes will be processed with OCR")
        else:
            st.error("Please upload a PDF first!")

    st.markdown("---")
    st.write("Built for GenAI Hackathon")

# ---------------- MAIN PAGE ---------------- #

col1, col2 = st.columns([2,3])

with col1:

    st.subheader("Ask a Question")

    question = st.text_area("Type your question")

    ask_button = st.button("Ask AI")

with col2:

    st.subheader("AI Answer")

    if ask_button:
        st.info("AI answer will appear here")

    st.subheader("Source Notes")