import sys
import os
from langchain_community.chat_models import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun

# Add root path to sys for clean imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Load Mistral and DuckDuckGo tool
llm = ChatOllama(model="mistral", temperature=0.3)
search = DuckDuckGoSearchRun()

def answer_with_web(question: str) -> str:
    # Step 1: Get live search result
    web_result = search.run(question)

    # Step 2: Build prompt with web content
    prompt = f"""
You are a Clinical AI Assistant helping patients with general medical queries.

The user asked:
❓ {question}

Here’s what we found from the web:
🌐 {web_result}

Please use the web content above to answer the user's question clearly, accurately, and empathetically.
Be concise and tag anything that came from search as [Web].

---

Answer:
""".strip()

    # Step 3: Generate response
    response = llm.invoke(prompt)
    return response.content.strip() + "\n\n🌐 _Web Sourced Information_"
if __name__ == "__main__":
    ans = answer_with_web("Is it safe to travel during monsoon with CKD?")
    print(ans)
