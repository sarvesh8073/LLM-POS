

from backend.tools.patient_lookup_tool import PatientLookupTool

tool = PatientLookupTool()

def handle_patient_query(patient_name: str, patient_message: str = ""):
    result = tool.lookup_patient(patient_name)

    if isinstance(result, str):  # Error message
        return {
            "reply": result,
            "clinical_needed": False,
            "patient_data": None
        }

    greeting = f"""
👋 Hello {patient_name}! I found your discharge report.

🩺 **Diagnosis:** {result['primary_diagnosis']}
📅 **Discharge Date:** {result['discharge_date']}
💊 **Medications:** {', '.join(result['medications'])}
⚠️ **Warning Signs:** {result['warning_signs']}

Are you taking your medications regularly?
"""

    msg_lower = patient_message.lower()
    clinical_needed = False  # <-- added flag

    # Symptom check
    symptom_keywords = ["swelling", "pain", "headache", "nausea", "vomit", "dizzy", "tired", "confused", "breath", "fatigue"]
    if any(word in msg_lower for word in symptom_keywords):
        greeting = "\n\n🔄 This sounds like a medical concern. I'll connect you to our Clinical AI Agent."
        clinical_needed = True  # <-- flag set
    permission_keywords = [
    "can i", "may i", "is it okay", "am i allowed", "should i", 
    "do you recommend", "is it safe", "would it be fine", 
    "can we", "can someone with", "can a patient", "is it advisable",
    "could i", "can i go", "can i eat", "can i travel", "can i work",
    "is it bad to", "am i good to", "is it harmful to", "would you suggest",
    "is it alright", "will it be okay", "do i need to avoid", "am i fit to"
]
    if any(word in msg_lower for word in permission_keywords):
        greeting = "\n\n🔄 Let's ask this to our Clinical agent! Allow me to connect you to it."
        clinical_needed = True  # <-- flag set

    # Medication affirmation
    affirmation_keywords = ["yes", "yeah", "of course", "regularly", "i take", "taking"]
    if any(word in msg_lower for word in affirmation_keywords):
        greeting = "\n\n✅ That's great to hear! Consistency with your meds is key to recovery. Keep it up! 💪"

    # Medication non-compliance
    negative_keywords = ["no", "not", "forgot", "missed", "skipped", "didn't", "did not"]
    if any(word in msg_lower for word in negative_keywords):
        greeting = "\n\n❗It’s important to follow your prescription carefully. Please try to stay consistent — it really helps with your recovery."
    followup = ["follow-up","followup","appointment","follow up"]
    if any(word in msg_lower for word in followup):
        greeting = f"Next Follow-Up schedule: \n\n {result['follow_up']}"
    return {
        "reply": greeting.strip(),
        "clinical_needed": clinical_needed,
        "patient_data": result  # pass patient object
    }

