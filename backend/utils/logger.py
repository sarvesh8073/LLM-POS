# backend/utils/logger.py

import os
import json
from datetime import datetime

LOG_FILE = "logs/conversation_log.jsonl"

def log_chat(sender: str, message: str, agent: str, patient_name: str, source: str = "manual", citations: list = None):
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "sender": sender,
        "message": message.strip(),
        "agent": agent,
        "source": source,
        "patient_name": patient_name,
    }
    if citations:
        log_entry["citations"] = citations
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
