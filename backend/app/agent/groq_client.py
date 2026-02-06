from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


def groq_chat(user_id: int, message: str) -> str:
    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI trading assistant. "
                    "Give concise, professional trading insights. "
                    "Never guess data."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        temperature=0.4,
        max_tokens=512,
    )

    return completion.choices[0].message.content.strip()
