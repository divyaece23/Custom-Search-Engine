# Custom-Search-Engine
A Streamlit-based Q&amp;A chatbot like a Search engine that uses LangChain, Groq LLM and Chroma embeddings to answer questions from uploaded PDFs, Wikipedia, Arxiv, and custom search queries, while maintaining persistent chat history.

## Features

- Conversational interface with persistent chat history.
- Integrates multiple sources for information retrieval:
  - **Arxiv**: academic papers
  - **Wikipedia**: encyclopedic knowledge
  - **DuckDuckGo**: web search
- Uses **Groq LLM (`Llama3-8b-8192`)** for natural language understanding.
- Handles parsing errors and agent reasoning gracefully.
- Streamlit interface for interactive Q&A.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/Custom_Search_Engine.git
cd Custom_Search_Engine

2. Create a virtual environment:

python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate   # Mac/Linux

3. Install requirements:

pip install -r requirements.txt

4. Create a .env file with your API keys:

GROQ_API_KEY=your_groq_api_key

5. Run the Streamlit app:

streamlit run sample_rag_app.py

