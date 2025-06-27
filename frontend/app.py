import streamlit as st
import sys
import os

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from agents.receptionist import handle_patient_query

st.set_page_config(page_title="Post-Discharge Medical Assistant", page_icon="🩺")
st.markdown("<h1 style='text-align: center;'>🩺 Post-Discharge Medical Chatbot</h1>", unsafe_allow_html=True)

# Session state for chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

# Ask for patient name once
if st.session_state.patient_name == "":
    name_input = st.text_input("👤 Enter your full name to begin:")
    if name_input and st.button("Start Chat"):
        st.session_state.patient_name = name_input
        st.session_state.chat_history.append(("assistant", f"👋 Hello {name_input}! I'm your post-discharge assistant. How are you feeling today?"))
        st.rerun()
else:
    # Chat display
    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(message)

    # Chat input box
    user_input = st.chat_input("Type your message...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append(("user", user_input))

        with st.chat_message("assistant"):
            response = handle_patient_query(st.session_state.patient_name, user_input)
            st.markdown(response)
        st.session_state.chat_history.append(("assistant", response))
