import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv(dotenv_path=".env")
print("API KEY:", os.getenv("GROQ_API_KEY"))

with open("knowledge_base.json") as f:
    KB = json.load(f)


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=os.getenv("GROQ_API_KEY")
)
def mock_lead_capture(name, email, platform):
    print(f"\n✅ Lead captured successfully: {name}, {email}, {platform}\n")

def detect_intent(user_message: str) -> str:
    prompt = f"""Classify the user intent. Reply with ONLY one word:
GREETING or PRODUCT_QUERY or HIGH_INTENT

HIGH_INTENT means user wants to sign up or buy.

User message: {user_message}"""
    response = llm.invoke([HumanMessage(content=prompt)])
    intent = response.content.strip().upper()
    if "HIGH_INTENT" in intent:
        return "HIGH_INTENT"
    elif "PRODUCT_QUERY" in intent:
        return "PRODUCT_QUERY"
    return "GREETING"

def rag_answer(user_message: str) -> str:
    kb_context = json.dumps(KB, indent=2)
    prompt = f"""You are AutoStream assistant. Answer using this knowledge base only:
{kb_context}

User question: {user_message}
Be concise and helpful."""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

state = {
    "lead": {"name": None, "email": None, "platform": None},
    "collecting_lead": False,
    "lead_captured": False,
}

def agent_respond(user_input: str) -> str:
    if state["collecting_lead"] and not state["lead_captured"]:
        lead = state["lead"]
        if lead["name"] is None:
            lead["name"] = user_input.strip()
            return "Got it! What is your email address?"
        elif lead["email"] is None:
            lead["email"] = user_input.strip()
            return "Which platform do you create content on? (YouTube, Instagram, TikTok)"
        elif lead["platform"] is None:
            lead["platform"] = user_input.strip()
            mock_lead_capture(lead["name"], lead["email"], lead["platform"])
            state["lead_captured"] = True
            state["collecting_lead"] = False
            return f"Perfect! Welcome to AutoStream, {lead['name']}! Our team will contact you soon."

    intent = detect_intent(user_input)

    if intent == "GREETING":
        return "Hey there! I am the AutoStream assistant. Ask me about our plans or get started today!"
    elif intent == "PRODUCT_QUERY":
        return rag_answer(user_input)
    elif intent == "HIGH_INTENT":
        state["collecting_lead"] = True
        return "Great choice! Let me get you signed up. First, what is your name?"

if __name__ == "__main__":
    print("AutoStream AI Agent — type 'quit' to exit\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue
        reply = agent_respond(user_input)
        print(f"\nAgent: {reply}\n")