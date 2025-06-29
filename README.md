🩺 Post-Discharge Medical AI Assistant
This project is a multi-agent chatbot system built with LangChain, Streamlit, and Mistral (via Ollama) to assist kidney disease patients after discharge. It includes patient lookup, symptom tracking, medication guidance, and web-enhanced clinical responses.

🚀 Features
🤖 Receptionist Agent – Welcomes patients, checks medication adherence, detects symptoms.

🧑‍⚕️ Clinical Agent – Answers medical questions using:

Discharge summary

RAG with Nephrology PDF

Web search fallback

📁 Patient Lookup – View discharge info using patient name.

➕ Add Patient – Add new patient details to JSON.

💬 Streaming Chat – Like ChatGPT (word-by-word display).

📝 Interaction Logger – Stores all chat logs in JSON.

🧱 Tech Stack
🧠 LLM: Mistral via Ollama

🔗 Framework: LangChain

🧾 RAG: FAISS + HuggingFaceEmbeddings

🌐 Web Tool: LangChain WebSearch

💻 Frontend: Streamlit
