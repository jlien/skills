---
name: Notion API
description: Notion REST API via curl for authentication, querying databases, and updating pages
---

# Notion API Guide

Use `curl` against the Notion REST API for reliable automation. Prefer this over the Notion MCP plugin.

For the Product Backlog database specifically (schema, status transitions, story creation), see `product-backlog.md`.

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

## Generic Operations

### Query a Database

Use the database query endpoint — NOT the `/v1/search` API, which may return 401 even with a valid token.

```bash
curl -s -X POST "https://api.notion.com/v1/databases/DATABASE_ID/query" \
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

### Update Page Properties

Use PATCH. The `status` property type uses `{"status": {"name": "VALUE"}}` format (NOT `select`).

```bash
curl -s -X PATCH "https://api.notion.com/v1/pages/PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "PROPERTY_NAME": { ... }
    }
  }'
```

Replace `PAGE_ID` with the page UUID (with or without hyphens).

### Create a Page

```bash
curl -s https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "DATABASE_ID"},
    "properties": { ... }
  }'
```

---

## Tips

- Page IDs in API responses are UUIDs with hyphens — both formats work in requests
- Pipe responses through `python3 -m json.tool` for readable output
- Update multiple properties in a single PATCH request
- Filter query results by `parent.database_id` if working across multiple databases
