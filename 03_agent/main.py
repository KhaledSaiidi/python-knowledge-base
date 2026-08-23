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

    print("Agent started. Type 'exit' or 'quit' to stop.")

    while True:
        message = input("\nYou: ").strip()

        if not message:
            continue

        if message.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        try:
            response = await agent.run(message)
            print(f"\nAssistant: {response}")

        except Exception as exc:
            print(f"\nError: {exc}")


if __name__ == "__main__":
    asyncio.run(main())