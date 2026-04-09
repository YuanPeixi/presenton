import aiohttp
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from google import genai


async def list_available_openai_compatible_models(url: str, api_key: str) -> list[str]:
    client = AsyncOpenAI(api_key=api_key, base_url=url)
    models = (await client.models.list()).data
    if models:
        return list(map(lambda x: x.id, models))
    return []


async def list_available_openrouter_models(api_key: str) -> list[str]:
    """Fetch OpenRouter models via direct HTTP to avoid OpenAI SDK schema validation issues."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://openrouter.ai/api/v1/models", headers=headers
        ) as response:
            response.raise_for_status()
            data = await response.json()
            models = data.get("data", [])
            return [model["id"] for model in models if "id" in model]


async def list_available_anthropic_models(api_key: str) -> list[str]:
    client = AsyncAnthropic(api_key=api_key)
    return list(map(lambda x: x.id, (await client.models.list(limit=50)).data))


async def list_available_google_models(api_key: str) -> list[str]:
    client = genai.Client(api_key=api_key)
    return list(map(lambda x: x.name, client.models.list(config={"page_size": 50})))
