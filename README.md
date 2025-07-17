# 🤖 PDF_ChatBot – Chat with Your PDFs Using Gemini

An interactive, theme-aware PDF Question-Answering chatbot powered by **LangChain**, **Google Gemini LLM**, and **FAISS**. Upload PDFs, ask natural language questions, and get precise answers from your documents—all in an elegant Streamlit interface!

![Gemini ChatPDF](https://img.shields.io/badge/LLM-Gemini_1.5_Flash-blue?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-powered-yellowgreen?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red?style=for-the-badge)

---

## 🚀 Features

- 📄 Upload and chat with **multiple PDFs**
- 🧠 **Context-aware** answers via Gemini + FAISS
- 🔎 Ask any question in natural language
- 🌓 Toggle between **Light and Dark** mode
- 💬 Clean, responsive Streamlit UI
- 🔐 Secure API key management using `.env`

---

## 🛠️ Tech Stack

| Tool                   | Purpose                                |
|------------------------|----------------------------------------|
| **Streamlit**          | Frontend Web UI                        |
| **LangChain**          | QA chain, chunking, prompt management  |
| **Gemini 1.5 Flash**   | LLM for answering questions            |
| **FAISS**              | Vector search for semantic retrieval   |
| **PyPDF2**             | PDF reading                            |
| **dotenv**             | Environment variable management        |

---

## 📦 Installation

```bash
git clone https://github.com/SankethHonavar/PDF_ChatBot.git
cd PDF_ChatBot
python -m venv venv
venv\Scripts\activate        # On Windows
# or
source venv/bin/activate     # On macOS/Linux

pip install -r requirements.txt
```
🔑 Setup
Create a .env file in the root directory and add your Google API key:
```
GOOGLE_API_KEY=your_google_gemini_api_key
```
🤖 How to Use
Upload one or more PDFs from the sidebar

Click 📎 Submit & Process

Ask a question using the input field

Get accurate answers based on your uploaded documents!

💡 If the answer isn't found in the documents, Gemini will tell you — no hallucinations.

🧠 Under the Hood
PyPDF2 reads and extracts text from PDFs

LangChain chunks the text and builds a QA chain

GoogleGenerativeAIEmbeddings generates embeddings

FAISS stores and retrieves relevant chunks using semantic similarity

Gemini 1.5 Flash responds with detailed, context-aware answers

📂 File Structure
```bash
Copy
Edit
📁 PDF_ChatBot
├── app.py                # Streamlit App
├── requirements.txt      # Project dependencies
├── .env                  # API keys (excluded from Git)
└── faiss_index/          # Vector DB (created at runtime)
```
📬 Contact
Built with ❤️ by Sanketh Honavar

📧 sankethhonavar25@gmail.com

