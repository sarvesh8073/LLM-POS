import streamlit as st
import json
import os

st.set_page_config(page_title="Patient Lookup", page_icon="🔍")
st.markdown("<h2 style='text-align: center;'>🔍 Patient Discharge Report Lookup</h2>", unsafe_allow_html=True)

# Load patient data from your backend
DATA_PATH = "backend/data/patient_reports.json"


try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        patient_data = json.load(f)
except Exception as e:
    st.error(f"❌ Could not load patient data: {e}")
    st.stop()

# Input box
name = st.text_input("Enter full patient name:")

# Search and display result
if name:
    match = next((p for p in patient_data if p["patient_name"].lower() == name.lower()), None)

    if match:
        st.success(f"✅ Found patient: {match['patient_name']}")
        st.markdown("---")
        st.markdown(f"**🩺 Diagnosis:** {match['primary_diagnosis']}")
        st.markdown(f"**📅 Discharge Date:** {match['discharge_date']}")
        st.markdown(f"**💊 Medications:** {', '.join(match['medications'])}")
        st.markdown(f"**🍽️ Dietary Restrictions:** {match['dietary_restrictions']}")
        st.markdown(f"**📞 Follow-up:** {match['follow_up']}")
        st.markdown(f"**⚠️ Warning Signs:** {match['warning_signs']}")
        st.markdown(f"**📋 Instructions:** {match['discharge_instructions']}")
    else:
        st.error("❌ No patient found with that name.")
