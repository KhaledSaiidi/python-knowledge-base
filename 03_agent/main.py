import asyncio

from dotenv import load_dotenv

from agent import Agent
from config import load_settings, load_tools
from llm_client import LLMClient


async def main() -> None:
    load_dotenv()

    settings = load_settings()
    tools = load_tools("tools.json")

    llm_client = LLMClient(
        api_key=settings.api_key,
        base_url=settings.base_url,
        model_name=settings.model_name,
    )

    agent = Agent(
        llm_client=llm_client,
        tools=tools,
    )

    response = await agent.run(
        "Read main.py and tell me what it does."
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())