# resources/task_resource.py
import json
from pathlib import Path
from config import TASK_DB_PATH

async def list_tasks_resource() -> str:
    """Fetch all tasks from database"""
    if not TASK_DB_PATH.exists():
        return "No tasks yet"
    
    with open(TASK_DB_PATH, 'r') as f:
        tasks = json.load(f)
    
    formatted = "# All Tasks\n\n"
    for task in tasks:
        formatted += f"- **{task['title']}** (Priority: {task['priority']})\n"
        if task['deadline']:
            formatted += f"  Deadline: {task['deadline']}\n"
        formatted += f"  Status: {'✓ Completed' if task['completed'] else '⏳ Pending'}\n\n"
    
    return formatted
