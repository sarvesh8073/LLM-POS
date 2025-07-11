


import streamlit as st
import sys
import os
from datetime import datetime
import time

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from backend.agents.receptionist import handle_patient_query
from backend.agents.clinical import answer_medical_query
from backend.utils.logger import log_chat

st.set_page_config(page_title="Post-Discharge Medical Assistant", page_icon="🩺")
st.markdown("<h1 style='text-align: center;'>🩺 Post-Discharge Medical Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>This is an AI assistant for educational purposes only</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>Always consult healthcare professionals for medical advice</h3>", unsafe_allow_html=True)

# Session state for chat memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "patient_name" not in st.session_state:
    st.session_state.patient_name = ""

if "active_agent" not in st.session_state:
    st.session_state.active_agent = "receptionist"

if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# Ask for patient name once
if st.session_state.patient_name == "":
    name_input = st.text_input("👤 Enter your full name to begin:")
    if name_input and st.button("Start Chat"):
        st.session_state.patient_name = name_input

        response = handle_patient_query(st.session_state.patient_name, name_input)
        st.markdown(response["reply"])
        st.session_state.chat_history.append(("assistant", response["reply"]))

        # ✅ Log receptionist response
        log_chat(
            sender="assistant",
            message=response["reply"],
            agent="receptionist",
            patient_name=st.session_state.patient_name,
            source="manual"
        )

        if response["clinical_needed"]:
            st.session_state.active_agent = "clinical"
            st.session_state.patient_data = response["patient_data"]
            st.session_state.waiting_for_response = True

            with st.spinner("🔬 Clinical Agent is preparing a response..."):
                clinical_reply = answer_medical_query(
                    st.session_state.patient_name,
                    name_input,
                    st.session_state.patient_data
                )

            st.session_state.waiting_for_response = False
            st.markdown("🔬 **Clinical Agent:**")
            st.markdown(clinical_reply)
            st.session_state.chat_history.append(("assistant", f"🔬 Clinical Agent:\n{clinical_reply}"))

            # ✅ Log clinical response
            log_chat(
                sender="assistant",
                message=clinical_reply,
                agent="clinical",
                patient_name=st.session_state.patient_name,
                source="web" if "web search" in clinical_reply.lower() else "rag"
            )

        st.rerun()
# if st.button("🔎 Go to Patient Lookup Page"):
#     st.switch_page("pages/Patient Lookup.py")
else:
    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(message)

    user_input = None
    if not st.session_state.waiting_for_response:
        user_input = st.chat_input("Type your message...")

        # ✅ Suggested prompts
        with st.expander("💡 Suggested Questions"):
            cols = st.columns(2)
            if cols[0].button("I have leg swelling"):
                st.session_state.suggested_input = "I have leg swelling"
                st.rerun()
            if cols[1].button("I forgot to take my meds"):
                st.session_state.suggested_input = "I forgot to take my meds"
                st.rerun()
            if cols[0].button("When is my next follow-up?"):
                st.session_state.suggested_input = "When is my next follow-up?"
                st.rerun()
            if cols[1].button("Can I eat bananas with CKD?"):
                st.session_state.suggested_input = "Can I eat bananas with CKD?"
                st.rerun()
    # ✅ Handle suggested input if present
    if "suggested_input" in st.session_state:
        user_input = st.session_state.suggested_input
        del st.session_state.suggested_input  # prevent replay on rerun


    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append(("user", user_input))
        log_chat(
            sender="user",
            message=user_input,
            agent=st.session_state.active_agent,
            patient_name=st.session_state.patient_name,
            source="user"
        )


        with st.chat_message("assistant"):
            if st.session_state.active_agent == "receptionist":
                response = handle_patient_query(st.session_state.patient_name, user_input)
                st.markdown(response["reply"])
                st.session_state.chat_history.append(("assistant", response["reply"]))

                # ✅ Log receptionist response
                log_chat(
                    sender="assistant",
                    message=response["reply"],
                    agent="receptionist",
                    patient_name=st.session_state.patient_name,
                    source="manual"
                )

                if response["clinical_needed"]:
                    st.session_state.active_agent = "clinical"
                    st.session_state.patient_data = response["patient_data"]
                    st.session_state.waiting_for_response = True

                    with st.spinner("🔬 Clinical Agent is preparing a response..."):
                        clinical_reply = answer_medical_query(
                            st.session_state.patient_name,
                            user_input,
                            st.session_state.patient_data
                        )

                    st.session_state.waiting_for_response = False
                    st.markdown("🔬 **Clinical Agent:**")
                    # st.markdown(clinical_reply)
                    # st.session_state.chat_history.append(("assistant", f"🔬 Clinical Agent:\n{clinical_reply}"))
                    placeholder = st.empty()
                    typed_text = ""
                    for word in clinical_reply.split():
                        typed_text += word + " "
                        # placeholder.markdown(typed_text + "▌")  # Cursor effect
                        placeholder.markdown(typed_text.replace("\n", "<br>") + "▌", unsafe_allow_html=True)
                        time.sleep(0.05)  # Speed: 50ms per word

                    placeholder.markdown(clinical_reply)
                    st.session_state.chat_history.append(("assistant", clinical_reply))


                    # ✅ Log clinical response
                    log_chat(
                        sender="assistant",
                        message=clinical_reply,
                        agent="clinical",
                        patient_name=st.session_state.patient_name,
                        source="web" if "web search" in clinical_reply.lower() else "rag"
                    )

            elif st.session_state.active_agent == "clinical":
                st.session_state.waiting_for_response = True

                with st.spinner("🔬 Clinical Agent is preparing a response..."):
                    clinical_reply = answer_medical_query(
                        st.session_state.patient_name,
                        user_input,
                        st.session_state.patient_data
                    )

                st.session_state.waiting_for_response = False
                # st.markdown(clinical_reply)
                # st.session_state.chat_history.append(("assistant", clinical_reply))
                placeholder = st.empty()
                typed_text = ""
                for word in clinical_reply.split():
                    typed_text += word + " "
                    # placeholder.markdown(typed_text + "▌")  # Cursor effect
                    placeholder.markdown(typed_text.replace("\n", "<br>") + "▌", unsafe_allow_html=True)
                    time.sleep(0.05)  # Speed: 50ms per word

                placeholder.markdown(clinical_reply)
                st.session_state.chat_history.append(("assistant", clinical_reply))


                # ✅ Log clinical response
                log_chat(
                    sender="assistant",
                    message=clinical_reply,
                    agent="clinical",
                    patient_name=st.session_state.patient_name,
                    source="web" if "web search" in clinical_reply.lower() else "rag"
                )






