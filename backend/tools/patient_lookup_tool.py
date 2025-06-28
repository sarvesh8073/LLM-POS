from langchain.tools import Tool
import json
import os

class PatientLookupTool:
    def __init__(self, filepath='backend/data/patient_reports.json'):
        self.filepath = filepath
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")

    def lookup_patient(self, name: str):
        print(f"[🔍] Looking for patient: {name}")  # DEBUG
        with open(self.filepath, 'r') as f:
            patients = json.load(f)

        matches = [p for p in patients if p["patient_name"].lower().strip() == name.lower().strip()]
        print(f"[✅] Found: {len(matches)} matches")

        if len(matches) == 0:
            
            return f"❌ No patient found with the name: {name}, please reload & try again."
        # elif len(matches) > 1:
        #     return f"⚠️ Multiple patients found with the name: {name}. Please refine the search."
        else:
            return matches[0]

    def as_langchain_tool(self):
        return Tool.from_function(
            name="patient_lookup",
            description="Use this to look up a patient by their name. Input must be just the name string (e.g., 'Paul Graham').",
            func=self.lookup_patient
        )
