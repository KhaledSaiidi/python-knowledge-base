import json
from typing import Any, cast

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionFunctionToolParam,
    ChatCompletionMessageParam,
)

from llm_client import LLMClient
from tool_registry import execute_tool


class Agent:
    def __init__(
        self,
        llm_client: LLMClient,
        tools: list[ChatCompletionFunctionToolParam],
        max_iterations: int = 10,
    ):
        self.llm_client = llm_client
        self.tools = tools
        self.max_iterations = max_iterations
        self.messages: list[ChatCompletionMessageParam] = []

    async def run(self, message: str) -> str:
        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

        for _ in range(self.max_iterations):
            response = await self.llm_client.create_chat_completion(
                messages=self.messages,
                tools=self.tools,
            )

            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls

            if not tool_calls:
                return assistant_message.content or ""

            assistant_message_param = cast(
                ChatCompletionAssistantMessageParam,
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": [
                        tool_call.model_dump()
                        for tool_call in tool_calls
                    ],
                },
            )

            self.messages.append(assistant_message_param)

            for tool_call in tool_calls:
                if tool_call.type != "function":
                    continue

                result = self._execute_function_tool(tool_call)

                self.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    }
                )

        raise RuntimeError(
            f"Agent exceeded maximum iterations: {self.max_iterations}"
        )

    def _execute_function_tool(self, tool_call: Any) -> str:
        tool_name = tool_call.function.name

        try:
            tool_args = json.loads(
                tool_call.function.arguments
            )

            if not isinstance(tool_args, dict):
                raise ValueError(
                    "Tool arguments must be a JSON object"
                )

            return execute_tool(
                tool_name=tool_name,
                tool_args=tool_args,
            )

        except json.JSONDecodeError as exc:
            return (
                f"Invalid JSON arguments for tool "
                f"'{tool_name}': {exc}"
            )

        except Exception as exc:
            return (
                f"Tool '{tool_name}' failed: {exc}"
            )