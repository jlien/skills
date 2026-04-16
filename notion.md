# Notion API Guide

Manage the Product Backlog in Notion via the REST API using `curl`. Use this instead of the Notion MCP plugin for reliable automation.

---

## Authentication & Headers

Every request requires these headers:

```bash
-H "Authorization: Bearer $NOTION_TOKEN" \
-H "Notion-Version: 2022-06-28" \
-H "Content-Type: application/json"
```

`NOTION_TOKEN` is set in `~/.bashrc`.

**Loading the token:** The Bash tool runs in a non-interactive shell, so `source ~/.bashrc` may not work (interactive-shell guards). Instead, grep the token value directly and export it:

```bash
eval "$(grep 'NOTION_TOKEN' ~/.bashrc)"
```

Run this once at the start of any session that needs Notion access.

---

## Product Backlog Database

**Database ID:** `306b272e-d659-8081-af46-d41c51b8604b`

### Key Properties

| Property | Type | Values |
|----------|------|--------|
| Status | `status` | "Not started", "Approved to Begin", "In progress", "Done" |
| Agents | `multi_select` | "plyoplanner-rails", "plyoplanner-mobile" |
| Name | `title` | Story title |

---

## Operations

### Search for a Page by Title

**Important:** Use the database query endpoint, NOT the search API. The search API may return 401 even with a valid token.

```bash
curl -s -X POST "https://api.notion.com/v1/databases/306b272e-d659-8081-af46-d41c51b8604b/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Name", "title": {"contains": "TITLE_HERE"}}}'
```

The response includes `results[].id` (the page ID) and `results[].properties`.

### Get Page Content (Blocks)

```bash
curl -s "https://api.notion.com/v1/blocks/PAGE_ID/children?page_size=100" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28"
```

### Update Page Status

Use PATCH to update a page's status. The `status` property type uses `{"status": {"name": "VALUE"}}` format (NOT `select`).

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Status": {
        "status": {
          "name": "Done"
        }
      }
    }
  }'
```

Replace `PAGE_ID` with the page UUID (with or without hyphens).

### Create a New Page

```bash
curl -s https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {
      "database_id": "306b272e-d659-8081-af46-d41c51b8604b"
    },
    "properties": {
      "Name": {
        "title": [
          {
            "text": {
              "content": "Story title here"
            }
          }
        ]
      },
      "Status": {
        "status": {
          "name": "Not started"
        }
      },
      "Agents": {
        "multi_select": [
          {"name": "plyoplanner-rails"}
        ]
      }
    }
  }'
```

---

## Common Workflows

### Move a Story to "In progress"

1. Search for the page by title
2. Extract the page ID from the response
3. PATCH the page with `"Status": {"status": {"name": "In progress"}}`

### Move a Story to "Done"

Same as above but with `"name": "Done"`.

---

## Tips

- Page IDs in search results are UUIDs with hyphens — both formats work in the API
- Pipe responses through `python3 -m json.tool` for readable output
- The search endpoint returns pages across all databases — filter results by checking `parent.database_id` if needed
- To update multiple properties at once, include them all in the same PATCH request
