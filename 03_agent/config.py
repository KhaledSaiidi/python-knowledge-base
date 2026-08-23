import json
import os
from dataclasses import dataclass
from typing import cast

from openai.types.chat import ChatCompletionFunctionToolParam


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    model_name: str


def load_settings() -> Settings:
    values = {
        "API_KEY": os.getenv("API_KEY"),
        "BASE_URL": os.getenv("BASE_URL"),
        "MODEL_NAME": os.getenv("MODEL_NAME"),
    }

    missing = [
        name
        for name, value in values.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing required environment variables: "
            f"{', '.join(missing)}"
        )

    return Settings(
        api_key=cast(str, values["API_KEY"]),
        base_url=cast(str, values["BASE_URL"]),
        model_name=cast(str, values["MODEL_NAME"]),
    )


def load_tools(
    path: str,
) -> list[ChatCompletionFunctionToolParam]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "Tool definition file must contain a JSON array"
        )

    return cast(
        list[ChatCompletionFunctionToolParam],
        data,
    )