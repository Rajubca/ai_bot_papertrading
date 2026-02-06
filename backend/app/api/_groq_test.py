from fastapi import APIRouter
from groq import Groq
from app.config import settings

router = APIRouter()

@router.get("/groq-test")
def groq_test():
    client = Groq(api_key=settings.GROQ_API_KEY)

    completion = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "user", "content": "Say hello in one sentence"}
        ],
        temperature=0.3,
        max_tokens=100,   # ✅ FIXED
        top_p=1,
    )

    return {
        "reply": completion.choices[0].message.content
    }
