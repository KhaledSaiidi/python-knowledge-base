from openai import AsyncOpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionFunctionToolParam,
    ChatCompletionMessageParam,
)


class LLMClient:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        model_name: str,
    ):
        self.model_name = model_name

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    async def create_chat_completion(
        self,
        messages: list[ChatCompletionMessageParam],
        tools: list[ChatCompletionFunctionToolParam],
    ) -> ChatCompletion:
        return await self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            tools=tools,
        )