from openai import AsyncOpenAI

from app.core.config import settings

SYSTEM_PROMPT = "You are a reliable, concise, and security-conscious AI assistant."

async def generate_assistant_reply(messages: list[dict[str, str]]) -> str:
    if not settings.openai_api_key:
        return "AI service is not configured. Add OPENAI_API_KEY to the API environment."
    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages])
    return response.choices[0].message.content or ""
