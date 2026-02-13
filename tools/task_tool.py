# tools/task_tool.py
"""
Task management tool with rate limiting
Creates tasks with deadline tracking
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from security.rate_limiter import rate_limit
from security.sanitizer import sanitize_text
from config import TASK_DB_PATH

logger = logging.getLogger(__name__)

async def create_task(
    title: str,
    description: str = "",
    deadline: str = None,
    priority: str = "medium"
) -> str:
    """
    Create a new task (rate limited to 10/minute)
    
    Args:
        title: Task title
        description: Task description
        deadline: ISO format deadline (YYYY-MM-DD)
        priority: low/medium/high
    
    Returns:
        Confirmation message
    """
    try:
        # SECURITY: Rate limiting
        if not rate_limit("create_task", max_requests=10, time_window=60):
            return "Error: Rate limit exceeded (10 tasks per minute)"
        
        # SECURITY: Input sanitization
        title = sanitize_text(title, max_length=100)
        description = sanitize_text(description, max_length=500)
        
        # Validate priority
        if priority not in ["low", "medium", "high"]:
            priority = "medium"
        
        # Validate deadline format
        if deadline:
            try:
                datetime.fromisoformat(deadline)
            except ValueError:
                return "Error: Invalid deadline format (use YYYY-MM-DD)"
        
        # Load existing tasks
        tasks = []
        if TASK_DB_PATH.exists():
            with open(TASK_DB_PATH, 'r') as f:
                tasks = json.load(f)
        
        # Create new task
        new_task = {
            "id": len(tasks) + 1,
            "title": title,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        
        tasks.append(new_task)
        
        # Save to file
        with open(TASK_DB_PATH, 'w') as f:
            json.dump(tasks, f, indent=2)
        
        logger.info(f"Task created: {title} (priority: {priority})")
        
        return f"✓ Task created: {title}\nPriority: {priority}\nDeadline: {deadline or 'None'}"
    
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        return "Error: Failed to create task"
