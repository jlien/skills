---
name: Notion Product Backlog
description: Product Backlog database schema, story operations, and workflow transitions in Notion
---

# Product Backlog in Notion

Schema and workflows for the Product Backlog database. See `SKILL.md` for generic Notion API patterns (auth, query, PATCH, create).

---

## Database

**Database ID:** `306b272e-d659-8081-af46-d41c51b8604b`

### Properties

| Property | Type | Values |
|----------|------|--------|
| Status | `status` | "Not started", "Approved to Begin", "In progress", "Done" |
| Agents | `multi_select` | "plyoplanner-rails", "plyoplanner-mobile" |
| Name | `title` | Story title |

---

## Operations

### Search for a Story by Title

```bash
curl -s -X POST "https://api.notion.com/v1/databases/306b272e-d659-8081-af46-d41c51b8604b/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Name", "title": {"contains": "TITLE_HERE"}}}'
```

### Update Story Status

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

### Create a Story

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
          {"text": {"content": "Story title here"}}
        ]
      },
      "Status": {
        "status": {"name": "Not started"}
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

## Workflows

### Move a Story to "In progress"

1. Search for the page by title
2. Extract the page ID from the response
3. PATCH the page with `"Status": {"status": {"name": "In progress"}}`

### Move a Story to "Done"

Same as above, with `"name": "Done"`.
