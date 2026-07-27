from openai import AsyncOpenAI
from app.core.config import settings
import structlog

logger = structlog.get_logger(__name__)

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class LLMService:
    @staticmethod
    async def generate(prompt: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        try:
            response = await client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                temperature=settings.LLM_TEMPERATURE,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("LLM call failed", error=str(e))
            raise
