import google.generativeai as genai
import os
from API_KEY import api_key
import streamlit as st

genai.configure(api_key=api_key)


system_instruction = """[페르소나 설정] 당신은 상담가입니다. 당시에게 오는 사람은 상담을 원하며 주제는 정해져 있지 않습니다.
최대한 친절하게 말해야 하며 방향을 제시해도 되고, 당장의 고민을 해결해줘도 좋습니다."""
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)
chat_session = model.start_chat(history=[])


