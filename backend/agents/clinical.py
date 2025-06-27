import sys
import os

# Add root folder to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langchain_community.chat_models import ChatOllama
from backend.tools.patient_lookup_tool import PatientLookupTool
from backend.rag.rag_engine import RAGEngine

# Load components
llm = ChatOllama(model="mistral", temperature=0.3)
rag = RAGEngine()
lookup = PatientLookupTool()

def answer_medical_query(patient_name: str, question: str, patient_data: dict = None) -> str:
    # Step 1: Use provided data or lookup if needed
    if patient_data is None:
        patient_data = lookup.lookup_patient(patient_name)
        if isinstance(patient_data, str):  # Error case
            return patient_data

    # Step 2: Query RAG
    context, sources = rag.query(question)

    # Step 3: Construct prompt
    prompt = f"""
You are a Clinical AI Agent assisting post-discharge kidney patients.

Your task is to answer patient-specific medical questions using:
1. Their discharge summary
2. Trusted nephrology medical references (provided below)

Always return a clear, accurate, and empathetic response.
If information is based on the reference, cite it as [Ref].
Keep the response concise and adequate in length, not too huge.

---

💬 Patient question:
{question}

📄 Patient details:
- Name: {patient_data['patient_name']}
- Diagnosis: {patient_data['primary_diagnosis']}
- Discharge Date: {patient_data['discharge_date']}
- Medications: {', '.join(patient_data['medications'])}
- Dietary: {patient_data['dietary_restrictions']}
- Follow-up: {patient_data['follow_up']}
- Warning signs: {patient_data['warning_signs']}
- Instructions: {patient_data['discharge_instructions']}

📚 Reference Material (Nephrology):
{context}

---

📝 Provide your answer below, include citations as [Ref] where applicable.
""".strip()

    # Step 4: LLM call
    response = llm.invoke(prompt)
    return response.content

# For standalone testing
if __name__ == "__main__":
    ans = answer_medical_query("Steven Villa", "I feel dizzy after taking my meds, is that normal?")
    print(ans)
