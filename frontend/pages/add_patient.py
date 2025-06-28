import streamlit as st
import json
import os

st.set_page_config(page_title="Add New Patient", page_icon="➕")
st.markdown("<h2 style='text-align: center;'>➕ Add New Patient Discharge Details</h2>", unsafe_allow_html=True)

DATA_PATH = "backend/data/patient_reports.json"

# Load existing patients
if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        patient_data = json.load(f)
else:
    patient_data = []

# 📝 Patient Entry Form
with st.form("new_patient_form"):
    patient_name = st.text_input("👤 Full Name").title().strip()
    discharge_date = st.date_input("📅 Discharge Date")
    primary_diagnosis = st.text_input("🩺 Primary Diagnosis")
    medications = st.text_area("💊 Medications (comma separated)")
    dietary_restrictions = st.text_area("🍽️ Dietary Restrictions")
    follow_up = st.text_input("📞 Follow-up Instructions")
    warning_signs = st.text_area("⚠️ Warning Signs")
    discharge_instructions = st.text_area("📋 Discharge Instructions")

    submitted = st.form_submit_button("✅ Save Patient")

if submitted:
    if not patient_name or not primary_diagnosis:
        st.error("❗ Name and diagnosis are required.")
    else:
        new_entry = {
            "patient_name": patient_name,
            "discharge_date": discharge_date.strftime("%Y-%m-%d"),
            "primary_diagnosis": primary_diagnosis,
            "medications": [med.strip() for med in medications.split(",") if med.strip()],
            "dietary_restrictions": dietary_restrictions,
            "follow_up": follow_up,
            "warning_signs": warning_signs,
            "discharge_instructions": discharge_instructions
        }

        patient_data.append(new_entry)

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(patient_data, f, indent=4)

        st.success(f"✅ New patient '{patient_name}' added successfully.")
