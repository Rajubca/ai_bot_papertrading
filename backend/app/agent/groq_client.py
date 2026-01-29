# app/agent/groq_client.py
from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def ask_agent(messages):
    return client.chat.completions.create(
        model="llama-3.1-70b",
        messages=messages,
        temperature=0.2
    )
