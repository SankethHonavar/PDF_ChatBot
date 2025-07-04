import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    If the answer is not in the context, say "answer is not available in the context". Do not guess.

    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain.invoke({"input_documents": docs, "question": user_question})
    st.write("📌 **Answer:**", response["output_text"])

def main():
    st.set_page_config("Chat PDF", page_icon="📚")

    # 🌗 Theme toggle
    with st.sidebar:
        st.title("📁 Menu")
        theme_mode = st.radio("🌓 Theme", ["Light", "Dark"], horizontal=True)

    # ✅ Apply theme styles
    if theme_mode == "Dark":
        st.markdown("""
        <style>
        :root {
            --text-color: #eee;
            --primary-color: #025c97;
        }
        body, .stApp {
            background-color: #1e1e1e !important;
            color: var(--text-color) !important;
        }
        .stTextInput input {
            background-color: #333 !important;
            color: var(--text-color) !important;
        }
        .stTextInput label {
            color: var(--text-color) !important;
        }
        input::placeholder {
            color: #bbb !important;
            opacity: 1 !important;
        }
        .stButton>button {
            background-color: #444 !important;
            color: var(--text-color) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        :root {
            --text-color: #111;
            --primary-color: #025c97;
        }
        body, .stApp {
            background-color: #ffffff !important;
            color: var(--text-color) !important;
        }
        .stTextInput input {
            background-color: #f0f0f0 !important;
            color: var(--text-color) !important;
        }
        .stTextInput label {
            color: var(--text-color) !important;
        }
        input::placeholder {
            color: #444 !important;
            opacity: 1 !important;
        }
        .stButton>button {
            background-color: #e0e0e0 !important;
            color: var(--text-color) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # 🚀 App header and input
    st.header("📚 Chat with Your PDFs using Gemini 💁")

    user_question = st.text_input(
        "💬 Ask a Question from the PDF",
        placeholder="e.g., What is the summary of this document?",
        label_visibility="visible"
    )

    if user_question:
        user_input(user_question)

    st.markdown("""
    ---
    ### 🤖 How to Use:
    1. 📄 Upload PDF files from the sidebar
    2. ⚙️ Click **Submit & Process**
    3. ❓ Ask questions above

    Gemini will answer based on your uploaded files 💡
    """)

    if not os.path.exists("faiss_index"):
        st.info("📝 Please upload a PDF file first using the sidebar to begin chatting.")

    # 📂 PDF Upload & Submit
    with st.sidebar:
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        if st.button("📎 Submit & Process", disabled=not pdf_docs):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("✅ PDFs processed successfully!")

        # 📬 Contact Info
        st.markdown("---")
        st.markdown("### 📬 Contact Me")
        st.markdown("[📧 Email](mailto:sankethhonavar25@gmail.com)")
        st.markdown("[🔗 LinkedIn](https://linkedin.com/in/sankethhonavar)")

    # ✨ Floating contact buttons
    st.markdown("""
    <style>
    .floating-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 9999;
    }
    .floating-button a {
        background-color: #0077b5;
        color: white;
        padding: 10px 14px;
        border-radius: 50%;
        text-align: center;
        font-size: 20px;
        text-decoration: none;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        transition: background-color 0.3s;
    }
    .floating-button a:hover {
        background-color: #005983;
    }
    .floating-button a.email {
        background-color: #444444;
    }
    .floating-button a.email:hover {
        background-color: #222222;
    }
    </style>

    <div class="floating-button">
        <a href="mailto:sankethhonavar25@gmail.com" class="email" title="Email Me">✉</a>
        <a href="https://linkedin.com/in/sankethhonavar" target="_blank" title="Connect on LinkedIn">in</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
