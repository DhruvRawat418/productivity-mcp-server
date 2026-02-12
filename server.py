"""
Productivity MCP Server (stdio)
Tools:
- send_email_draft
- add_task
"""

import json, re, os
from pathlib import Path
from datetime import datetime
from typing import Any
from collections import defaultdict

import anyio
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

from dotenv import load_dotenv

load_dotenv()

# ----------------------------
# Security helpers
# ----------------------------

class SafeErrorHandler:
    @staticmethod
    def sanitize_error(error: Exception) -> str:
        error_msg = str(error)
        error_msg = re.sub(r"/[^\s]+\.py", "[REDACTED_PATH]", error_msg)
        error_msg = re.sub(r"C:\\[^\s]+\.py", "[REDACTED_PATH]", error_msg)
        error_msg = re.sub(r"line \d+", "line [REDACTED]", error_msg)
        return f"Operation failed: {error_msg}"


class InputSanitizer:
    @staticmethod
    def sanitize_email_field(text: str, field_name: str) -> str:
        if not isinstance(text, str):
            raise ValueError(f"{field_name} must be a string")

        max_lengths = {"subject": 200, "recipient": 100, "body": 10000}
        if len(text) > max_lengths.get(field_name, 10000):
            raise ValueError(f"{field_name} exceeds maximum length")

        if field_name in ["subject", "recipient"]:
            if re.search(r"[\r\n]", text):
                raise ValueError(f"{field_name} contains invalid characters (newlines)")

        dangerous_patterns = [
            r"\$\(",
            r"`",
            r"\|",
            r";",
            r"&&",
            r"\|\|",
            r">",
            r"<",
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, text):
                raise ValueError(f"{field_name} contains potentially dangerous characters")

        if field_name == "recipient":
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, text):
                raise ValueError("Invalid email format")

        return text

    @staticmethod
    def sanitize_task_title(title: str) -> str:
        if not isinstance(title, str):
            raise ValueError("Task title must be a string")
        if len(title) > 500:
            raise ValueError("Task title too long (max 500 characters)")
        title = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", title)
        return title.strip()


class RateLimiter:
    def __init__(self, limit_per_minute: int = 10):
        self.requests = defaultdict(list)
        self.limit = limit_per_minute

    def check_rate_limit(self, tool_name: str) -> bool:
        now = datetime.now()
        self.requests[tool_name] = [
            ts for ts in self.requests[tool_name] if (now - ts).seconds < 60
        ]
        if len(self.requests[tool_name]) >= self.limit:
            return False
        self.requests[tool_name].append(now)
        return True


# ----------------------------
# Storage
# ----------------------------

TASKS_FILE = Path(__file__).parent / "tasks.json"

def load_tasks() -> list[dict[str, Any]]:
    if not TASKS_FILE.exists():
        return []
    try:
        return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except Exception:
        raise Exception("Failed to load tasks")

def save_tasks(tasks: list[dict[str, Any]]) -> None:
    try:
        TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
    except Exception:
        raise Exception("Failed to save tasks")


# ----------------------------
# MCP server
# ----------------------------

app = Server("productivity-assistant")
rate_limiter = RateLimiter()

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="send_email_draft",
            description="Create an email draft with sanitized inputs",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipient": {"type": "string", "description": "Recipient email"},
                    "subject": {"type": "string", "description": "Subject line"},
                    "body": {"type": "string", "description": "Email body"},
                },
                "required": ["recipient", "subject", "body"],
            },
        ),
        types.Tool(
            name="add_task",
            description="Add a new task (stored in tasks.json)",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Task priority",
                    },
                },
                "required": ["title"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict
) -> list[types.TextContent]:
    if not rate_limiter.check_rate_limit(name):
        return [types.TextContent(type="text", text="Rate limit exceeded. Try again later.")]

    try:
        if name == "send_email_draft":
            recipient = InputSanitizer.sanitize_email_field(arguments.get("recipient", ""), "recipient")
            subject = InputSanitizer.sanitize_email_field(arguments.get("subject", ""), "subject")
            body = InputSanitizer.sanitize_email_field(arguments.get("body", ""), "body")

            return [
                types.TextContent(
                    type="text",
                    text=f"Email draft created:\n\nTo: {recipient}\nSubject: {subject}\n\n{body}",
                )
            ]

        if name == "add_task":
            title = InputSanitizer.sanitize_task_title(arguments.get("title", ""))
            priority = arguments.get("priority", "medium")
            if priority not in ["low", "medium", "high"]:
                priority = "medium"

            tasks = load_tasks()
            new_task = {
                "id": len(tasks) + 1,
                "title": title,
                "priority": priority,
                "created_at": datetime.now().isoformat(),
                "completed": False,
            }
            tasks.append(new_task)
            save_tasks(tasks)

            return [
                types.TextContent(
                    type="text",
                    text=f"Task added:\nID: {new_task['id']}\nTitle: {title}\nPriority: {priority}",
                )
            ]

        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except ValueError as e:
        return [types.TextContent(type="text", text=f"Validation error: {e}")]

    except Exception as e:
        return [types.TextContent(type="text", text=SafeErrorHandler.sanitize_error(e))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )

if __name__ == "__main__":
    anyio.run(main)