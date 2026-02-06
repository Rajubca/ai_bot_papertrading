from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "Say hello in one sentence"}
    ],
    temperature=0.4,
    max_tokens=256,   # ✅ FIXED
)

print(completion.choices[0].message.content)
