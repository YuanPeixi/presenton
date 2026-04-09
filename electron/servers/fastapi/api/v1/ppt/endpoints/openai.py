from typing import Annotated, List
from fastapi import APIRouter, Body, HTTPException

from utils.available_models import list_available_openai_compatible_models, list_available_openrouter_models

OPENAI_ROUTER = APIRouter(prefix="/openai", tags=["OpenAI"])
OPENROUTER_ROUTER = APIRouter(prefix="/openrouter", tags=["OpenRouter"])


@OPENAI_ROUTER.post("/models/available", response_model=List[str])
async def get_available_models(
    url: Annotated[str, Body()],
    api_key: Annotated[str, Body()],
):
    try:
        return await list_available_openai_compatible_models(url, api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@OPENROUTER_ROUTER.post("/models/available", response_model=List[str])
async def get_available_openrouter_models(
    api_key: Annotated[str, Body()],
):
    try:
        return await list_available_openrouter_models(api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
