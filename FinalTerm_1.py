import google.generativeai as genai
import os
from API_KEY import api_key
import streamlit as st
from pymongo import MongoClient
import pprint
import datetime

genai.configure(api_key=api_key)

system_instruction = """[페르소나 설정] 당신은 상담가입니다. 당시에게 오는 사람은 상담을 원하며 주제는 정해져 있지 않습니다.
최대한 친절하게 말해야 하며 방향을 제시해도 되고, 당장의 고민을 해결해줘도 좋습니다."""
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)

st.title("챗봇 상담사")
st.markdown("이 챗봇은 당신의 고민을 듣고 상담을 해줍니다. 어떠한 고민이든 괜찮습니다. 뭐든 물어보셔도 됩니다.")
st.markdown("-" * 50)

@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)
    print("model loaded...")
    return model

@st.cache_resource
def init_connection():
    return MongoClient(**st.secrets["mongo"])

client = init_connection()

@st.cache_resource
def setting_collection():
    db = client["finalterm_db"]
    collection = db["save_text"]
    return collection

collection = setting_collection()

@st.cache_resource
def insert_data(post):
    collection.insert_one(post)

model = load_model()

if "chat_session" not in st.session_state:
    st.session_state["chat_session"] = model.start_chat(history=[]) # ChatSession 반환

for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)

    
if prompt := st.chat_input("상담 하고자 하는 내용을 입력하세요."):
    with st.chat_message("user"):
        st.markdown(prompt)
        post = {
            "date": datetime.datetime.now(),
            "text": prompt
        }
        insert_data(post)
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)
        post = {
            "date": datetime.datetime.now(),
            "text": response.text
        }
        insert_data(post)
        
