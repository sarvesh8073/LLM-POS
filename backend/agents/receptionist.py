from langchain_community.chat_models import ChatOllama  # for local models like Mistral
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from backend.tools.patient_lookup_tool import PatientLookupTool

# ✅ Use Ollama Mistral
llm = ChatOllama(model="mistral", temperature=0.3)

# Tool setup
lookup_tool = PatientLookupTool().as_langchain_tool()

# Initialize the agent
receptionist_agent = initialize_agent(
    tools=[lookup_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors = True,
    verbose=True
)

def handle_patient_query(patient_name: str, patient_question: str = ""):
    if not patient_name:
        return "👋 Hi! May I know your name, please?"

    prompt = f"""
You are a Receptionist AI in a post-discharge medical assistant system.

Patient's name is: {patient_name}

Your tasks:
1. Use the `patient_lookup` tool to find their discharge report.
2. Greet the patient using their name and diagnosis from the report.
3. Ask how they are feeling and if they are following their medication.
4. If they mention any symptoms, tell them you'll connect them to the Clinical AI Agent.

Important:
- To use the tool, ONLY enter the name as a string like this: Paul Graham
- DO NOT use function calls like patient_lookup(name="...") ❌
"""

    if patient_question:
        prompt += f"\nThe patient says: {patient_question}"

    try:
        return receptionist_agent.invoke({"input": prompt})
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

