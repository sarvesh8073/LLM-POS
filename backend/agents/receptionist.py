# from langchain_community.chat_models import ChatOllama  # for local models like Mistral
# from langchain.agents import initialize_agent
# from langchain.agents.agent_types import AgentType
# from backend.tools.patient_lookup_tool import PatientLookupTool

# # ✅ Use Ollama Mistral
# llm = ChatOllama(model="mistral", temperature=0.3)

# # Tool setup
# lookup_tool = PatientLookupTool().as_langchain_tool()

# # Initialize the agent
# receptionist_agent = initialize_agent(
#     tools=[lookup_tool],
#     llm=llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     handle_parsing_errors = True,
#     verbose=True
# )

# def handle_patient_query(patient_name: str, patient_question: str = ""):
#     if not patient_name:
#         return "👋 Hi! May I know your name, please?"

#     prompt = f"""
# You are a Receptionist AI in a post-discharge medical assistant system.

# Patient's name is: {patient_name}

# Your tasks:
# 1. Use the `patient_lookup` tool to find their discharge report.
# 2. Greet the patient using their name and diagnosis from the report.
# 3. Ask how they are feeling and if they are following their medication.
# 4. If they mention any symptoms, tell them you'll connect them to the Clinical AI Agent.

# Important:
# - To use the tool, ONLY enter the name as a string like this: Paul Graham
# - DO NOT use function calls like patient_lookup(name="...") ❌
# """

#     if patient_question:
#         prompt += f"\nThe patient says: {patient_question}"

#     try:
#         return receptionist_agent.invoke({"input": prompt})
#     except Exception as e:
#         return f"⚠️ Error: {str(e)}"

from backend.tools.patient_lookup_tool import PatientLookupTool

tool = PatientLookupTool()

def handle_patient_query(patient_name: str, patient_message: str = ""):
    result = tool.lookup_patient(patient_name)

    if isinstance(result, str):  # Error message
        return result

    greeting = f"""
👋 Hello {patient_name}! I found your discharge report.

🩺 **Diagnosis:** {result['primary_diagnosis']}
📅 **Discharge Date:** {result['discharge_date']}
💊 **Medications:** {', '.join(result['medications'])}
⚠️ **Warning Signs:** {result['warning_signs']}

Are you taking your medications regularly?
"""

    msg_lower = patient_message.lower()

  


    # Symptom check
    symptom_keywords = ["swelling", "pain", "headache", "nausea", "vomit", "dizzy", "tired", "confused", "breath", "fatigue"]
    if any(word in msg_lower for word in symptom_keywords):
        greeting = "\n\n🔄 This sounds like a medical concern. I'll connect you to our Clinical AI Agent."

    # Medication affirmation
    affirmation_keywords = ["yes", "yeah", "i am", "of course", "regularly", "i take", "taking"]
    if any(word in msg_lower for word in affirmation_keywords):
        greeting = "\n\n✅ That's great to hear! Consistency with your meds is key to recovery. Keep it up! 💪"

    # Medication non-compliance
    negative_keywords = ["no", "not", "forgot", "missed", "skipped", "didn't", "did not"]
    if any(word in msg_lower for word in negative_keywords):
        greeting = "\n\n❗It’s important to follow your prescription carefully. Please try to stay consistent — it really helps with your recovery."

    return greeting.strip()

