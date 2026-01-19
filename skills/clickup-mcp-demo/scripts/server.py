#!/usr/bin/env python3
"""
ClickUp MCP Server - Demo Version

A simple MCP server demonstrating ClickUp integration.
Perfect for 15-minute team demos and learning MCP basics.

Usage:
    1. Set your API token: export CLICKUP_API_TOKEN="your_token"
    2. Run: python server.py

Requirements:
    pip install mcp httpx
"""

import os
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("ClickUp Demo")

# Configuration
API_TOKEN = os.environ.get("CLICKUP_API_TOKEN")
BASE_URL = "https://api.clickup.com/api/v2"


def get_headers():
    """Return authorization headers for ClickUp API."""
    if not API_TOKEN:
        raise ValueError("CLICKUP_API_TOKEN environment variable not set")
    return {"Authorization": API_TOKEN, "Content-Type": "application/json"}


# =============================================================================
# TOOL 1: List Workspaces (Teams)
# =============================================================================
@mcp.tool()
async def clickup_list_workspaces() -> str:
    """
    List all workspaces (teams) you have access to.
    This is usually your first call to find your team_id.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/team", headers=get_headers())
        response.raise_for_status()

        teams = response.json().get("teams", [])
        if not teams:
            return "No workspaces found."

        lines = ["**Your ClickUp Workspaces:**", ""]
        for team in teams:
            lines.append(f"- **{team['name']}** (ID: `{team['id']}`)")

        return "\n".join(lines)


# =============================================================================
# TOOL 2: List Spaces
# =============================================================================
@mcp.tool()
async def clickup_list_spaces(team_id: str) -> str:
    """
    List all spaces in a workspace.

    Args:
        team_id: The workspace/team ID (get from clickup_list_workspaces)
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/team/{team_id}/space",
            headers=get_headers()
        )
        response.raise_for_status()

        spaces = response.json().get("spaces", [])
        if not spaces:
            return f"No spaces found in workspace {team_id}."

        lines = ["**Spaces:**", ""]
        for space in spaces:
            lines.append(f"- **{space['name']}** (ID: `{space['id']}`)")

        return "\n".join(lines)


# =============================================================================
# TOOL 3: List Folders in a Space
# =============================================================================
@mcp.tool()
async def clickup_list_folders(space_id: str) -> str:
    """
    List all folders in a space.

    Args:
        space_id: The space ID (get from clickup_list_spaces)
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/space/{space_id}/folder",
            headers=get_headers()
        )
        response.raise_for_status()

        folders = response.json().get("folders", [])
        if not folders:
            return f"No folders found in space {space_id}."

        lines = ["**Folders:**", ""]
        for folder in folders:
            lines.append(f"- **{folder['name']}** (ID: `{folder['id']}`)")
            # Also show lists inside folders
            for lst in folder.get("lists", []):
                lines.append(f"  - List: {lst['name']} (ID: `{lst['id']}`)")

        return "\n".join(lines)


# =============================================================================
# TOOL 4: List Tasks
# =============================================================================
@mcp.tool()
async def clickup_list_tasks(list_id: str) -> str:
    """
    List all tasks in a ClickUp list.

    Args:
        list_id: The list ID to fetch tasks from
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/list/{list_id}/task",
            headers=get_headers()
        )
        response.raise_for_status()

        tasks = response.json().get("tasks", [])
        if not tasks:
            return f"No tasks found in list {list_id}."

        lines = ["**Tasks:**", ""]
        for task in tasks:
            status = task.get("status", {}).get("status", "unknown")
            priority = task.get("priority")
            priority_str = f" [{priority['priority']}]" if priority else ""
            lines.append(f"- [{status}]{priority_str} **{task['name']}** (ID: `{task['id']}`)")

        return "\n".join(lines)


# =============================================================================
# TOOL 5: Create Task
# =============================================================================
@mcp.tool()
async def clickup_create_task(
    list_id: str,
    name: str,
    description: str = ""
) -> str:
    """
    Create a new task in a ClickUp list.

    Args:
        list_id: The list ID where the task will be created
        name: The name/title of the task
        description: Optional description for the task
    """
    async with httpx.AsyncClient() as client:
        payload = {
            "name": name,
            "description": description,
        }

        response = await client.post(
            f"{BASE_URL}/list/{list_id}/task",
            headers=get_headers(),
            json=payload
        )
        response.raise_for_status()

        task = response.json()
        return f"Created task: **{task['name']}**\n- ID: `{task['id']}`\n- URL: {task.get('url', 'N/A')}"


# =============================================================================
# TOOL 6: Update Task Status
# =============================================================================
@mcp.tool()
async def clickup_update_task_status(task_id: str, status: str) -> str:
    """
    Update the status of a task.

    Args:
        task_id: The task ID to update
        status: The new status (e.g., "open", "in progress", "complete")
    """
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{BASE_URL}/task/{task_id}",
            headers=get_headers(),
            json={"status": status}
        )
        response.raise_for_status()

        task = response.json()
        new_status = task.get("status", {}).get("status", status)
        return f"Updated task **{task['name']}** to status: **{new_status}**"


# =============================================================================
# Run the server
# =============================================================================
if __name__ == "__main__":
    print("Starting ClickUp MCP Server...")
    print("Tools available: clickup_list_workspaces, clickup_list_spaces,")
    print("                 clickup_list_folders, clickup_list_tasks,")
    print("                 clickup_create_task, clickup_update_task_status")
    mcp.run(transport="stdio")
