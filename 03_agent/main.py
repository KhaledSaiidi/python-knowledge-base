import asyncio
import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionFunctionToolParam

load_dotenv()


class LLMClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
    ):
        self.model_name = model_name
        try:
            self.client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url,
            )
        except Exception as exc:
            raise RuntimeError(
                "Failed to initialize the LLM client"
            ) from exc

    async def create_chat_completion(
        self,
        message: str,
        tools: list[ChatCompletionFunctionToolParam],
    ) -> str:
        response = await self.client.chat.completions.create(
            model=self.model_name,
            tools=tools,
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
        )

        return response.choices[0].message.content or ""

def load_access() -> tuple[str, str, str]:
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("BASE_URL")
    model_name = os.getenv("MODEL_NAME")

    missing = [
        name
        for name, value in {
            "API_KEY": api_key,
            "BASE_URL": base_url,
            "MODEL_NAME": model_name,
        }.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )

    assert api_key is not None
    assert base_url is not None
    assert model_name is not None

    return api_key, base_url, model_name

def load_tools(path: str) -> list[ChatCompletionFunctionToolParam]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

async def main():
    api_key, base_url, model_name = load_access()
    tools = load_tools("tools.json")

    llm_client = LLMClient(
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
    )

    response = await llm_client.create_chat_completion(
        "Explain Kubernetes in one sentence.",
        tools,
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())