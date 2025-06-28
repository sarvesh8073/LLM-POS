
import sys
import os

# Add root folder to sys.path dynamically
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from langchain_community.chat_models import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from backend.tools.patient_lookup_tool import PatientLookupTool
from backend.rag.rag_engine import RAGEngine

# Load components
llm = ChatOllama(model="mistral", temperature=0.3)
rag = RAGEngine()
lookup = PatientLookupTool()
search = DuckDuckGoSearchRun()  # ✅ Web search tool

def answer_medical_query(patient_name: str, question: str, patient_data: dict = None) -> str:
    # Step 1: Use provided data or lookup if needed
    if patient_data is None:
        patient_data = lookup.lookup_patient(patient_name)
        if isinstance(patient_data, str):  # Error case
            return patient_data

    # Step 2: Query RAG
    context, sources = rag.query(question)
    web_trigger_keywords = ["latest", "new", "current", "recent", "update", "advancement", "research", "clinical trial"]
    msg_lower = question.lower()
    triggered_by_keywords = any(keyword in msg_lower for keyword in web_trigger_keywords)
    use_web = triggered_by_keywords or not sources or all(len(chunk.strip()) < 50 for chunk in sources)

    # Step 3: Determine if RAG was useful (based on source string lengths)
    # use_web = not sources or all(len(chunk.strip()) < 50 for chunk in sources)

    web_info = ""
    web_notice = ""
    if use_web:
        web_info = search.run(question)
        context = f"{context}\n\n[Web] {web_info}".strip()
        web_notice = "\n\n🌐 _This answer includes information retrieved via live web search._"

    # Step 4: Construct prompt
    prompt = f"""
You are a Clinical AI Agent assisting post-discharge kidney patients.

Your task is to answer patient-specific medical questions using:
1. Their discharge summary
2. Trusted nephrology medical references (provided below)

Always return a clear, accurate, and empathetic response.
If information is based on the reference, cite it as [Ref] or [Web] appropriately.
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

📚 Reference Material:
{context}

---

📝 Provide your answer below, include citations as [Ref] or [Web] where applicable.
""".strip()

    # Step 5: Get answer from LLM
    response = llm.invoke(prompt)

    # Step 6: Build citation footer
    if sources and not use_web:
        citation_text = "\n\n📚 **Reference Chunks Used (Preview):**\n\n"
        for idx, chunk in enumerate(sources, 1):
            snippet = chunk.strip()[:300]  # Limit to first 300 characters
            if len(chunk.strip()) > 300:
                snippet += "..."  # Add ellipsis if it's truncated
            citation_text += f"{idx}. {snippet}\n\n"

    elif use_web:
        citation_text = f"\n\n📚 **Web Info Used:**\n\n{web_info.strip()}"
    else:
        citation_text = "\n\n📚 **Reference Chunks Used:**\n\n_No specific content chunks found._"

    # Step 7: Return full reply
    return response.content.strip() + web_notice + citation_text

# For standalone testing
if __name__ == "__main__":
    ans = answer_medical_query("Steven Villa", "What's the latest research on SGLT2 inhibitors for kidney disease?")
    print(ans)

