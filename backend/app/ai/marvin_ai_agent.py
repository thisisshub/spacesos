import marvin
from pydantic import BaseModel
from backend.settings import log
from django.conf import settings
from typing import List, Dict, Any

if not settings.AI_MODEL.startswith("sk-"):
    raise ValueError("OpenAI API Key not found.")

marvin.settings.openai.api_key = settings.AI_MODEL

@marvin.fn
def summarize_tasks_by_priority(tasks: List[Dict[str, Any]]) -> list:
    """
    Summarizes tasks based on priority and returns a list of task summaries.

    Args:
        tasks (List[Dict[str, Any]]): A list of task dictionaries containing:
            - `id` (str): A unique identifier for the task.
            - `title` (str): The task's title or description.
            - `completed` (bool): Whether the task is completed.
            - `due_date` (str): The due date for the task in ISO 8601 format.
            - `priority` (str): The priority of the task (e.g., "HIGH", "MEDIUM", "LOW").
            - `client` (int): The client ID associated with the task.
            - `reminder_created` (bool): Whether a reminder has been created.

    Returns:
        List[Dict[str, str]]: A list of dictionaries summarizing tasks by priority:
            - `priority` (str): The priority of the task (e.g., "HIGH", "MEDIUM").
            - `title` (str): Comma-separated task titles for the given priority.
            - `summary` (str): A summary of the tasks.
            - `advisory` (str): A priority-based advisory.

    Example:
    ```python
    Input:
    [
        {"id": "1", "title": "Call John", "completed": False, "due_date": "2025-02-17T14:12:13+05:30", "priority": "HIGH", "client": 2, "reminder_created": False},
        {"id": "2", "title": "Email Report", "completed": False, "due_date": "2025-02-17T14:45:30+05:30", "priority": "MEDIUM", "client": 2, "reminder_created": False}
    ]

    Output:
    {
        "summary": "The following tasks requires you to...",
        "priority": "You can do them in following order",
        "advisory": "Requires immediate attention",
        "title": "Task XYZ"
    }
    ```
    """