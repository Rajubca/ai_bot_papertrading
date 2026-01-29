SYSTEM_PROMPT = """
You are an AI assistant for a PAPER TRADING platform.

- Never place trades
- Never assume data
- Always respond in strict JSON
"""

def build_user_prompt(user_message, context):
    return f"""
USER_MESSAGE:
{user_message}

CONTEXT (authoritative):
{context}

Respond only in valid JSON.
"""
