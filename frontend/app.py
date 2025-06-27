# import streamlit as st
# import sys
# import os

# # Add backend path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
# from backend.agents.receptionist import handle_patient_query

# st.set_page_config(page_title="Post-Discharge Medical Assistant", page_icon="🩺")
# st.markdown("<h1 style='text-align: center;'>🩺 Post-Discharge Medical Chatbot</h1>", unsafe_allow_html=True)

# # Session state for chat memory
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "patient_name" not in st.session_state:
#     st.session_state.patient_name = ""

# # Ask for patient name once
# if st.session_state.patient_name == "":
#     name_input = st.text_input("👤 Enter your full name to begin:")
#     if name_input and st.button("Start Chat"):
#         st.session_state.patient_name = name_input
#         # st.session_state.chat_history.append(("assistant", f"👋 Hello {name_input}! I'm your post-discharge assistant. How are you feeling today?"))
#         response = handle_patient_query(st.session_state.patient_name, name_input)
#         st.markdown(response)
#         st.session_state.chat_history.append(("assistant", response))
#         st.rerun()
# else:
#     # Chat display
#     for sender, message in st.session_state.chat_history:
#         with st.chat_message(sender):
#             st.markdown(message)

#     # Chat input box
#     user_input = st.chat_input("Type your message...")
#     if user_input:
#         with st.chat_message("user"):
#             st.markdown(user_input)
#         st.session_state.chat_history.append(("user", user_input))

#         with st.chat_message("assistant"):
#             response = handle_patient_query(st.session_state.patient_name, user_input)
#             st.markdown(response)
#         st.session_state.chat_history.append(("assistant", response))
# import streamlit as st
# import sys
# import os

# # Add backend path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
# from backend.agents.receptionist import handle_patient_query
# from backend.agents.clinical import answer_medical_query  # ✅ added

# st.set_page_config(page_title="Post-Discharge Medical Assistant", page_icon="🩺")
# st.markdown("<h1 style='text-align: center;'>🩺 Post-Discharge Medical Chatbot</h1>", unsafe_allow_html=True)

# # Session state for chat memory
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "patient_name" not in st.session_state:
#     st.session_state.patient_name = ""

# if "active_agent" not in st.session_state:
#     st.session_state.active_agent = "receptionist"
    
# if "waiting_for_response" not in st.session_state:
#     st.session_state.waiting_for_response = False


# # Ask for patient name once
# if st.session_state.patient_name == "":
#     name_input = st.text_input("👤 Enter your full name to begin:")
#     if name_input and st.button("Start Chat"):
#         st.session_state.patient_name = name_input

#         # ✅ Get response as dict from receptionist
#         response = handle_patient_query(st.session_state.patient_name, name_input)
#         st.markdown(response["reply"])
#         st.session_state.chat_history.append(("assistant", response["reply"]))

#         # ✅ Clinical handoff on startup (edge case)
#         if response["clinical_needed"]:
#             clinical_reply = answer_medical_query(
#                 st.session_state.patient_name,
#                 name_input,
#                 response["patient_data"]
#             )
#             st.markdown("🔬 **Clinical Agent:**")
#             st.markdown(clinical_reply)
#             st.session_state.chat_history.append(("assistant", f"🔬 Clinical Agent:\n{clinical_reply}"))

#         st.rerun()

# else:
#     # Chat history display
#     for sender, message in st.session_state.chat_history:
#         with st.chat_message(sender):
#             st.markdown(message)

#     # Chat input box
#     user_input = None
#     if not st.session_state.waiting_for_response:
#         user_input = st.chat_input("Type your message...")

#     if user_input:
#         with st.chat_message("user"):
#             st.markdown(user_input)
#         st.session_state.chat_history.append(("user", user_input))

#         with st.chat_message("assistant"):
#             # response = handle_patient_query(st.session_state.patient_name, user_input)
#             # st.markdown(response["reply"])
#             # st.session_state.chat_history.append(("assistant", response["reply"]))

#             # # ✅ Handoff to clinical if symptom detected
#             # if response["clinical_needed"]:
#             #     clinical_reply = answer_medical_query(
#             #         st.session_state.patient_name,
#             #         user_input,
#             #         response["patient_data"]
#             #     )
#             #     st.markdown("🔬 **Clinical Agent:**")
#             #     st.markdown(clinical_reply)
#             #     st.session_state.chat_history.append(("assistant", f"🔬 Clinical Agent:\n{clinical_reply}"))
#             if st.session_state.active_agent == "receptionist":
#                 response = handle_patient_query(st.session_state.patient_name, user_input)
#                 st.markdown(response["reply"])
#                 st.session_state.chat_history.append(("assistant", response["reply"]))

#                 if response["clinical_needed"]:
#                     from backend.agents.clinical import answer_medical_query
#                     st.session_state.active_agent = "clinical"  # ✅ Switch permanently to clinical
#                     st.session_state.patient_data = response["patient_data"]  # ✅ Save for reuse

#                     with st.spinner("🔬 Clinical Agent is preparing a response..."):
#                         clinical_reply = answer_medical_query(
#                             st.session_state.patient_name,
#                             user_input,
#                             st.session_state.patient_data
#                         )
#                         st.markdown("🔬 **Clinical Agent:**")
#                         st.markdown(clinical_reply)
#                         st.session_state.chat_history.append(("assistant", f"🔬 Clinical Agent:\n{clinical_reply}"))

#             elif st.session_state.active_agent == "clinical":
#                 from backend.agents.clinical import answer_medical_query
#                 with st.spinner("🔬 Clinical Agent is preparing a response..."):
#                     clinical_reply = answer_medical_query(
#                         st.session_state.patient_name,
#                         user_input,
#                         st.session_state.patient_data  # ✅ Use stored patient info
#                     )
#                 st.markdown(clinical_reply)
#                 st.session_state.chat_history.append(("assistant", clinical_reply))





import streamlit as st
import sys
import os
from datetime import datetime

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from backend.agents.receptionist import handle_patient_query
from backend.agents.clinical import answer_medical_query
from backend.utils.logger import log_chat

st.set_page_config(page_title="Post-Discharge Medical Assistant", page_icon="🩺")
st.markdown("<h1 style='text-align: center;'>🩺 Post-Discharge Medical Chatbot</h1>", unsafe_allow_html=True)

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

            elif st.session_state.active_agent == "clinical":
                st.session_state.waiting_for_response = True

                with st.spinner("🔬 Clinical Agent is preparing a response..."):
                    clinical_reply = answer_medical_query(
                        st.session_state.patient_name,
                        user_input,
                        st.session_state.patient_data
                    )

                st.session_state.waiting_for_response = False
                st.markdown(clinical_reply)
                st.session_state.chat_history.append(("assistant", clinical_reply))

                # ✅ Log clinical response
                log_chat(
                    sender="assistant",
                    message=clinical_reply,
                    agent="clinical",
                    patient_name=st.session_state.patient_name,
                    source="web" if "web search" in clinical_reply.lower() else "rag"
                )






# import streamlit as st
# import sys
# import os

# # Add backend path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
# from backend.agents.receptionist import handle_patient_query
# from backend.agents.clinical import answer_medical_query
# from backend.agents.web_agent import answer_with_web  # ✅ NEW

# st.set_page_config(page_title="Post-Discharge Medical Assistant", page_icon="🩺")
# st.markdown("<h1 style='text-align: center;'>🩺 Post-Discharge Medical Chatbot</h1>", unsafe_allow_html=True)

# # Session state for chat memory
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# if "patient_name" not in st.session_state:
#     st.session_state.patient_name = ""

# if "active_agent" not in st.session_state:
#     st.session_state.active_agent = "receptionist"

# if "waiting_for_response" not in st.session_state:
#     st.session_state.waiting_for_response = False

# # Ask for patient name once
# if st.session_state.patient_name == "":
#     name_input = st.text_input("👤 Enter your full name to begin:")
#     if name_input and st.button("Start Chat"):
#         st.session_state.patient_name = name_input

#         response = handle_patient_query(st.session_state.patient_name, name_input)
#         st.markdown(response["reply"])
#         st.session_state.chat_history.append(("assistant", response["reply"]))

#         if response["clinical_needed"]:
#             st.session_state.active_agent = "clinical"
#             st.session_state.patient_data = response["patient_data"]
#             st.session_state.waiting_for_response = True

#             with st.spinner("🔬 Clinical Agent is preparing a response..."):
#                 clinical_reply = answer_medical_query(
#                     st.session_state.patient_name,
#                     name_input,
#                     st.session_state.patient_data
#                 )

#             st.session_state.waiting_for_response = False
#             st.markdown("🔬 **Clinical Agent:**")
#             st.markdown(clinical_reply)
#             st.session_state.chat_history.append(("assistant", f"🔬 Clinical Agent:\n{clinical_reply}"))

#         st.rerun()

# else:
#     # Chat history display
#     for sender, message in st.session_state.chat_history:
#         with st.chat_message(sender):
#             st.markdown(message)

#     # Chat input box
#     user_input = None
#     if not st.session_state.waiting_for_response:
#         user_input = st.chat_input("Type your message...")

#     if user_input:
#         with st.chat_message("user"):
#             st.markdown(user_input)
#         st.session_state.chat_history.append(("user", user_input))

#         with st.chat_message("assistant"):
#             if st.session_state.active_agent == "receptionist":
#                 response = handle_patient_query(st.session_state.patient_name, user_input)
#                 st.markdown(response["reply"])
#                 st.session_state.chat_history.append(("assistant", response["reply"]))

#                 if response["clinical_needed"]:
#                     st.session_state.active_agent = "clinical"
#                     st.session_state.patient_data = response["patient_data"]
#                     st.session_state.waiting_for_response = True

#                     with st.spinner("🔬 Clinical Agent is preparing a response..."):
#                         clinical_reply = answer_medical_query(
#                             st.session_state.patient_name,
#                             user_input,
#                             st.session_state.patient_data
#                         )

#                     st.session_state.waiting_for_response = False
#                     st.markdown("🔬 **Clinical Agent:**")
#                     st.markdown(clinical_reply)
#                     st.session_state.chat_history.append(("assistant", f"🔬 Clinical Agent:\n{clinical_reply}"))

#             elif st.session_state.active_agent == "clinical":
#                 st.session_state.waiting_for_response = True

#                 with st.spinner("🔬 Clinical Agent is preparing a response..."):
#                     clinical_reply = answer_medical_query(
#                         st.session_state.patient_name,
#                         user_input,
#                         st.session_state.patient_data
#                     )

#                 st.session_state.waiting_for_response = False
#                 st.markdown(clinical_reply)
#                 st.session_state.chat_history.append(("assistant", clinical_reply))

#     # 🌐 Web Agent Section
#     st.divider()
#     st.markdown("#### 🌐 Didn't find what you needed?")
#     web_question = st.text_input("Ask Web AI (Live Search):", key="web_input")

#     if st.button("🌍 Ask Web AI"):
#         if not web_question.strip():
#             st.warning("Please enter a question for the Web Agent.")
#         else:
#             with st.chat_message("user"):
#                 st.markdown(web_question)
#             st.session_state.chat_history.append(("user", web_question))

#             with st.chat_message("assistant"):
#                 with st.spinner("🌐 Web Agent is searching..."):
#                     web_reply = answer_with_web(web_question)
#                 st.markdown("🔵 **Web AI:**")
#                 st.markdown(web_reply)

#             st.session_state.chat_history.append(("assistant", f"🔵 Web AI:\n{web_reply}"))
