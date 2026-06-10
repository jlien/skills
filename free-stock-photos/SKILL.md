---
name: free-stock-photos
description: "Find free-to-use (CC-licensed / public domain) photographs for any topic — landmarks, cities, nature, everyday life, cultural scenes. Searches Wikimedia Commons API with license filters."
version: 1.0.0
author: Jimmy Lien
license: MIT
metadata:
  hermes:
    tags: [stock-photos, creative-commons, wikimedia, free-photos, open-license, design-assets]
    related_skills: []
---

# Free Stock Photos

## Overview

Find free-to-use (CC-licensed or public domain) photographs via the Wikimedia Commons API. Covers any topic — landmarks, cities, nature, villages, temples, streets, everyday life, and more. Returns direct image URLs with verifiable licensing.

## When to Use

- The user needs free/open-license images for a project, presentation, blog, or design
- The user specifies categories like landmarks, mountains, villages, temples, streets, or everyday life
- The user needs verifiable CC-licensed photos (not generated or watermarked)
- Any topic, any country — not limited to Japan

## Core Workflow

### Step 1: Query Wikimedia Commons API

Use `curl` with the Commons API to search for photos in namespace 6 (image files), filtered to CC licenses:

```bash
curl -s 'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=<QUERY>&srnamespace=6&srlimit=10&srfilters=license:cc-by-3.0,cc-by-sa-3.0,cc-by-4.0,cc0-1.0&format=json' | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('query', {}).get('search', []):
    print(r['title'], '-', r.get('snippet', ''))
"
```

### Step 2: Get Image URLs

Once you have the desired file titles, query the API for image URLs:

```bash
curl -s 'https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url&titles=File:<TITLE1>|File:<TITLE2>&iiurlwidth=1200&format=json' | python3 -c "
import sys, json
data = json.load(sys.stdin)
for title, info in data['query']['pages'].items():
    ii = info.get('imageinfo', [{}])[0]
    print(title)
    print('  URL:', ii.get('thumburl', ii.get('url', '')))
"
```

## Query Patterns by Category

| Category | Query Pattern |
|----------|---------------|
| Mountains | `<mountain name> <country>` |
| Traditional village | `<country> village traditional` |
| City streets | `<city> street <country>` or `<famous crossing/district>` |
| Neon/nightlife | `<city district> night <country>` |
| Temples/religious | `<country> temple shrine` |
| Everyday life | `<city> people crossing` or `<district> <city>` |
| Parks | `<park name> <city>` |
| Nature/landscape | `<country> <landscape type>` |
| Seasonal | `season keyword <country>` (e.g. `cherry blossom sakura Japan`) |

### Example: Japan

| Category | Query |
|----------|-------|
| Mountains | `Mount Fuji Japan` |
| Traditional village | `Shirakawa-go Japan village` |
| City streets | `Tokyo street Japan` or `Shibuya crossing` |
| Neon/nightlife | `Shinjuku Kabukicho night Japan` |
| Temples | `Kyoto temple Japan` |
| Everyday life | `Tokyo people crossing street` or `Harajuku Tokyo` |
| Parks | `Shinjuku Gyoen Tokyo` |
| Rice paddies | `Japan rice paddy mountain` |
| Cherry blossoms | `cherry blossom sakura Japan` |

## Key Principles

1. **Always verify the license** — Wikimedia Commons files carry their own licenses. The query filters for CC licenses, but confirm on the file page if strict attribution is needed.
2. **Use `iiurlwidth=1200`** for a good balance of quality and file size. Use `iiurlwidth=1920` for full-resolution needs.
3. **Namespace 6 is images** — always include `srnamespace=6` in search queries.
4. **Filter to CC licenses** — use `srfilters=license:cc-by-3.0,cc-by-sa-3.0,cc-by-4.0,cc0-1.0` to exclude GFDL-only files (which require text-only attribution that's harder to satisfy with images).
5. **File titles use spaces and are case-sensitive** — copy exact titles from the search results into the imageinfo query.

## Fallback: Other Free Photo Sources

If Wikimedia Commons doesn't have what you need:

- **Unsplash** — `https://unsplash.com/s/photos/<query>` (free for commercial use, no attribution required)
- **Pexels** — `https://www.pexels.com/search/<query>/` (free for commercial use)
- **Pixabay** — `https://pixabay.com/images/search/<query>/` (CC0 / Pixabay license)

Stock photo APIs (Unsplash, Pexels) require API keys — if the user doesn't have one, browse via the web URLs above.
