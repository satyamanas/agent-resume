#Load Modules

from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain

st.set_page_config(layout="wide")
st.title("AI RESUME GENERATOR")
st.write("""This app helps user to build customized Professional Resume with latest Job apply links""")

st.image("https://raw.githubusercontent.com/satyamanas/agent-resume/refs/heads/main/poster.png")

st.sidebar.title("Fill Important Details")
st.sidebar.image("https://raw.githubusercontent.com/satyamanas/agent-resume/refs/heads/main/poster.png")

#api keys

TAVILY_API_KEY = st.sidebar.text_input("Tavily-API", type = "password")
api = st.sidebar.text_input("Gemini-API", type = "password")
gapi = st.sidebar.text_input("Groq-API", type = "password")

all_API = [TAVILY_API_KEY, api ,gapi]

if not all(all_API):
    st.error("Must give API keys")
    st.stop()
elif all(all_API):
    model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = api
    )
else: 
    st.info("Pass all API-Keys")

# MULTISELECT OPTION
options = ["Delhi", "Mumbai", "Pune", "Banglore",
           "Gurugram/Gurgaon"]
location = st.sidebar.multiselect("Select Location",
                                  options = options)
profile_op = ["Data Analysts", "AI Engineer","Gen AI Developer", "Full-Stack Dev",
              "Data Scientist"]

profile = st.sidebar.multiselect("Select Job Profile",
                                 options = profile_op)

#GET USER INFO
st.markdown("""###Get user info###""")
user_info = st.text_area("""Write your resume Description: """)



#model creation



#response = model.invoke("Hello Buddy!")
#response. content [-1] ['text' ]

#search latest news jobs

def search_latest_news_jobs (query):
    """This function helps to fetch latest
    news or jobs related article using
    tavily"""

    client = TavilyClient(
        api_key = TAVILY_API_KEY)
    response = client. search (query)
    return response

#create agent

agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs]
)

 # agent

#prompt to generate cv 

def main_agent(agent, query):
    """This is main agent, or leader agent
    orchestrate sub agents"""


    # Giving prompt to create detailed prompt
    # for code generation
    prompt = """You are AI assistant and
    below given is a prompt, your task is to give detailed prompt for
    this. You are a professional Resume generator where user will give their personal info,
    you have to create detailed Resume
    for students or professional one,it must be with dynamic UI and UX and,
    with advanced CSS Professional DesigningMake sure to give output in HTML format only
    no markdowns allowed
    """
    response = agent. invoke({'messages': [{'role':'user',
    'content' :prompt}]})
    detailed_prompt = response['messages' ][-1].content[-1] ['text']
    # SAVE PROMPT using File Handling
    with open('prompt.txt','w') as f:
        f.write(detailed_prompt)
    user_details = f"""Below Given is a user details
    generate Resume based on that, if not
    given keep: Default Resume: Python Developer
    user details: {query}"""

    final_prompt = prompt + detailed_prompt + user_details

    response = agent. invoke({'messages' : [ {'role':'user',
    'content' : final_prompt}]})

    code = response['messages' ] [-1].content[-1] ['text']

    return code

#display jons

# code = main_agent(agent, "Manas Satya, GEN AI EXPERT")
# from IPython import display as DISPLAY 
# DISPLAY.HTML(code)

#fetch jobs related to cv

def get_jobs(agent,
            Location = "Noida,Delhi",
            Profile = "Data Analysts, AI Engineer"):
    Location = "Noida, Delhi"
    Profile = "Data Analysts, AI Engineer"

    prompt = f"""Based on user given Job profile,
    fetch latest jobs or job apply article
    using Naukri, Linkedin, Indeed, or all popular
    Job apply platforms, Show Results with
    JOB PROFILE NAME, LOCATION, SALARY, COMPANY NAME,
    SHOW jobs only related to given
    {Location} and {Profile}. Output must be in
    Professional HTML Naukri theme cards with Dynamic Design,
    Show atleast Top 10-20 results with direct apply link"""

    response = agent.invoke ({'messages':[{'role':'user',
                                           'content':prompt}]})

    code = response['messages' ][-1]. content[-1]['text' ]

    return code

if st.button("Generate Resume"):
    with st.spinner("Agent Running"):
        code = main_agent(agent, user_info)
        st.html(code , width="stretch", 
                unsafe_allow_javascript=True)
        st.divider() # to give horizontal div
        jobe_code = get_jobs(agent, location, profile)   
        st.html(code , width="stretch", 
                unsafe_allow_javascript=True)
            
#display jobs 

#code = get_jobs(agent)
#DISPLAY.HTML(code)
