### streamlit run sample_rag_app.py
# .venv\Scripts\activate

import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

from dotenv import load_dotenv
load_dotenv()

st.sidebar.title('Settings')
groq_api_key = st.sidebar.text_input('Enter your Groq API key:',type='password')
if not groq_api_key:
    st.info('Please add your Groq API key')
    st.stop()
    
arxiv_wrapper = ArxivAPIWrapper(
    top_k_results = 1,
    ARXIV_MAX_QUERY_LENGTH = 300,
    load_all_available_meta = False,
    doc_content_chars_max = 200
)
arxiv= ArxivQueryRun(api_wrapper= arxiv_wrapper)

wikipedia_wrapper = WikipediaAPIWrapper(
    top_k_results = 1,
    ARXIV_MAX_QUERY_LENGTH = 300,
    load_max_docs = 3,
    load_all_available_meta = False,
    doc_content_chars_max = 200
)
wikipedia= WikipediaQueryRun(api_wrapper= wikipedia_wrapper)

search_eng = DuckDuckGoSearchRun(name ='Search')

st.title('Custom Search Engine')

if "messages" not in st.session_state:
    st.session_state.messages = [{'role':'assistant', 'content':'Hi, How can i help you?'}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

response =''
if prompt := st.chat_input("Your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    llm=ChatGroq(model="Llama3-8b-8192",groq_api_key=groq_api_key, streaming = True)
    tools =[arxiv, wikipedia, search_eng]

    agents = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True, verbose=True)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts = False)
        response = agents.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.write(response)
