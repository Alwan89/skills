---
name: clickup-mcp-demo
description: A beginner-friendly demo for connecting Claude to ClickUp via MCP (Model Context Protocol). Use this skill when learning MCP basics, demoing ClickUp integration, or building your first MCP server.
---

# ClickUp MCP Demo

A 15-minute introduction to connecting Claude with ClickUp using MCP.

## What You'll Learn

1. **What MCP is** - How Claude connects to external tools
2. **Basic MCP server** - A simple Python server for ClickUp
3. **3 Demo Tools** - List spaces, list tasks, create task

## Prerequisites

- Python 3.10+
- ClickUp API token (get from ClickUp Settings > Apps > API Token)
- Claude Code or Claude Desktop

---

## Part 1: Understanding MCP (2 min)

**MCP (Model Context Protocol)** lets Claude talk to external services through "tools".

```
┌─────────────┐     MCP Protocol     ┌─────────────┐     HTTP API     ┌─────────────┐
│   Claude    │ ◄──────────────────► │ MCP Server  │ ◄──────────────► │  ClickUp    │
└─────────────┘                      └─────────────┘                  └─────────────┘
```

- **Claude** asks the MCP server to do things
- **MCP Server** translates requests to ClickUp API calls
- **ClickUp** returns data that Claude can use

---

## Part 2: Quick Setup (5 min)

### Step 1: Create project folder

```bash
mkdir clickup-mcp && cd clickup-mcp
```

### Step 2: Install dependencies

```bash
pip install mcp httpx
```

### Step 3: Set your API token

```bash
export CLICKUP_API_TOKEN="your_token_here"
```

### Step 4: Create the server

Create `server.py` - see the example in `scripts/server.py` or copy below:

```python
import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ClickUp Demo")
API_TOKEN = os.environ.get("CLICKUP_API_TOKEN")
BASE_URL = "https://api.clickup.com/api/v2"

def headers():
    return {"Authorization": API_TOKEN}

@mcp.tool()
async def clickup_list_spaces(team_id: str) -> str:
    """List all spaces in a ClickUp workspace/team."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/team/{team_id}/space", headers=headers())
        spaces = r.json().get("spaces", [])
        return "\n".join([f"- {s['name']} (ID: {s['id']})" for s in spaces])

@mcp.tool()
async def clickup_list_tasks(list_id: str) -> str:
    """List tasks in a ClickUp list."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE_URL}/list/{list_id}/task", headers=headers())
        tasks = r.json().get("tasks", [])
        return "\n".join([f"- [{t['status']['status']}] {t['name']}" for t in tasks])

@mcp.tool()
async def clickup_create_task(list_id: str, name: str, description: str = "") -> str:
    """Create a new task in a ClickUp list."""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{BASE_URL}/list/{list_id}/task",
            headers=headers(),
            json={"name": name, "description": description}
        )
        task = r.json()
        return f"Created task: {task['name']} (ID: {task['id']})"

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

---

## Part 3: Connect to Claude (3 min)

### For Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "clickup": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "CLICKUP_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

### For Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "clickup": {
      "command": "python",
      "args": ["/full/path/to/server.py"],
      "env": {
        "CLICKUP_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

---

## Part 4: Demo It! (5 min)

Once connected, try these prompts with Claude:

### Demo 1: List your spaces
> "List all my ClickUp spaces for team ID 12345678"

### Demo 2: View tasks
> "Show me tasks in list 987654321"

### Demo 3: Create a task
> "Create a task called 'Review MCP demo' in list 987654321"

### Finding your IDs

- **Team ID**: ClickUp Settings > Workspaces > click workspace > ID in URL
- **List ID**: Open any list > ID is in the URL

---

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "Unauthorized" | Check your API token is set correctly |
| "Server not found" | Verify the path in your config file |
| "No spaces returned" | Confirm team_id is correct |

---

## Next Steps

After the demo, explore:

1. **Add more tools** - Update tasks, manage folders, time tracking
2. **Error handling** - Add try/catch and better error messages
3. **Caching** - Reduce API calls for frequently accessed data
4. **See `mcp-builder` skill** - For comprehensive MCP development guide

---

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [ClickUp API Docs](https://clickup.com/api)
- [FastMCP Python Library](https://github.com/jlowin/fastmcp)
