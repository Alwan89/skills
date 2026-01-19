# ClickUp API Quick Reference

A cheat sheet for the most common ClickUp API operations.

## Authentication

All requests require an API token in the `Authorization` header:

```
Authorization: pk_12345678_ABCDEFGHIJKLMNOP
```

**Get your token:** ClickUp > Settings > Apps > API Token

## Base URL

```
https://api.clickup.com/api/v2
```

## ClickUp Hierarchy

```
Workspace (Team)
  └── Space
        └── Folder (optional)
              └── List
                    └── Task
```

## Common Endpoints

### Workspaces

| Action | Method | Endpoint |
|--------|--------|----------|
| List workspaces | GET | `/team` |

### Spaces

| Action | Method | Endpoint |
|--------|--------|----------|
| List spaces | GET | `/team/{team_id}/space` |
| Get space | GET | `/space/{space_id}` |
| Create space | POST | `/team/{team_id}/space` |

### Folders

| Action | Method | Endpoint |
|--------|--------|----------|
| List folders | GET | `/space/{space_id}/folder` |
| Get folder | GET | `/folder/{folder_id}` |
| Create folder | POST | `/space/{space_id}/folder` |

### Lists

| Action | Method | Endpoint |
|--------|--------|----------|
| Lists in folder | GET | `/folder/{folder_id}/list` |
| Lists in space | GET | `/space/{space_id}/list` |
| Create list | POST | `/folder/{folder_id}/list` |

### Tasks

| Action | Method | Endpoint |
|--------|--------|----------|
| List tasks | GET | `/list/{list_id}/task` |
| Get task | GET | `/task/{task_id}` |
| Create task | POST | `/list/{list_id}/task` |
| Update task | PUT | `/task/{task_id}` |
| Delete task | DELETE | `/task/{task_id}` |

## Example: Create Task

```python
import httpx

response = httpx.post(
    "https://api.clickup.com/api/v2/list/123456/task",
    headers={"Authorization": "pk_your_token"},
    json={
        "name": "My Task",
        "description": "Task description",
        "priority": 2,  # 1=urgent, 2=high, 3=normal, 4=low
        "due_date": 1704067200000,  # Unix ms timestamp
        "assignees": [12345678],  # User IDs
        "tags": ["tag1", "tag2"]
    }
)
```

## Task Statuses

Default statuses (vary by list):
- `to do`
- `in progress`
- `complete`
- `closed`

## Priority Levels

| Value | Meaning |
|-------|---------|
| 1 | Urgent |
| 2 | High |
| 3 | Normal |
| 4 | Low |
| null | No priority |

## Rate Limits

- **100 requests per minute** per token
- Rate limit headers in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Finding IDs

### Team/Workspace ID
1. Go to ClickUp Settings
2. Click on Workspaces
3. The ID is in the URL: `app.clickup.com/settings/team/{team_id}`

### Space/List/Task ID
The ID appears in the URL when viewing any item:
- Space: `app.clickup.com/{team_id}/v/s/{space_id}`
- List: `app.clickup.com/{team_id}/v/li/{list_id}`
- Task: `app.clickup.com/t/{task_id}`

## Error Responses

| Code | Meaning |
|------|---------|
| 400 | Bad request - check your parameters |
| 401 | Unauthorized - invalid API token |
| 403 | Forbidden - no access to resource |
| 404 | Not found - resource doesn't exist |
| 429 | Rate limited - slow down requests |
| 500 | Server error - try again later |

## Useful Query Parameters

For `GET /list/{list_id}/task`:

| Parameter | Description |
|-----------|-------------|
| `archived` | Include archived tasks (true/false) |
| `page` | Page number (starts at 0) |
| `subtasks` | Include subtasks (true/false) |
| `statuses[]` | Filter by status |
| `assignees[]` | Filter by assignee |
| `due_date_gt` | Due date greater than (Unix ms) |
| `due_date_lt` | Due date less than (Unix ms) |
