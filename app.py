### streamlit run sample_rag_app.py
# .venv\Scripts\activate

import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler

from dotenv import load_dotenv
load_dotenv()

st.sidebar.title('Settings')
groq_api_key = st.sidebar.text_input('Enter your Groq API key:',type='password')
if not groq_api_key:
    st.info('Please add your Groq API key')
    st.stop()
    
st.title('Custom Search Engine')

if "messages" not in st.session_state:
    st.session_state.messages = [{'role':'assistant', 'content':'Hi, How can i help you?'}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# DuckDuckGo Search Tool
ddg_search_tool = DuckDuckGoSearchRun(name="DuckDuckGo Search")

# Wikipedia Search Tool
wiki_search_tool = Tool(
    name="Wikipedia Search",
    func=WikipediaAPIWrapper().run,
    description="Use this tool to search Wikipedia articles."
)

# Arxiv Search Tool
arxiv_search_tool = Tool(
    name="Arxiv Search",
    func=ArxivAPIWrapper().run,
    description="Use this tool to search Arxiv papers."
)

response =''
if prompt := st.chat_input("Your question:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    llm=ChatGroq(model="Llama3-8b-8192",groq_api_key=groq_api_key, streaming = True)
    tools = [ddg_search_tool, wiki_search_tool, arxiv_search_tool]

    agents = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True, verbose=True)
    st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts = False)
    response = agents.run(st.session_state.messages, callbacks=[st_cb])
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with st.chat_message("assistant"):
        st.write(response)






