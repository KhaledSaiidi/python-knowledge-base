from collections.abc import Callable
from typing import Any

from tools_helpers import read_file, write_file


TOOL_REGISTRY: dict[str, Callable[..., str]] = {
    "Read": read_file,
    "Write": write_file,
}


def execute_tool(
    tool_name: str,
    tool_args: dict[str, Any],
) -> str:
    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    return tool(**tool_args)