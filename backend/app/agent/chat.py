import json
from app.agent.groq_client import ask_agent
from app.agent.prompts import SYSTEM_PROMPT, build_user_prompt

def chat_with_agent(user_message, context):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(user_message, context)}
    ]

    response = ask_agent(messages)

    content = response.choices[0].message.content

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return {
            "action": "ERROR",
            "summary": "Invalid AI response format",
            "raw": content
        }

    return parsed
