---
name: japan-stock-photos
description: "Use when the user needs free-to-use images of Japan (landmarks, everyday life, mountains, villages, temples, cities). Searches Wikimedia Commons API for CC-licensed photos."
version: 1.0.0
author: Jimmy Lien
license: MIT
metadata:
  hermes:
    tags: [stock-photos, japan, creative-commons, wikimedia, free-photos, travel, design-assets]
    related_skills: []
---

# Japan Free Stock Photos

## Overview

Find free-to-use (CC-licensed) photographs of Japan via the Wikimedia Commons API. Covers landmarks, everyday life, city scenes, traditional villages, mountains, temples, and nature. Returns direct image URLs with proper licensing attribution.

## When to Use

- The user needs free/open-license images of Japan for a project, presentation, blog, or design
- The user specifies categories like landmarks, mountains, villages, temples, streets, or everyday life
- The user needs verifiable CC-licensed photos (not generated or watermarked)

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

## Recommended Search Queries by Category

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

## Curated Photo Collection

These have been verified to return quality results:

### Mountains
- **Mount Fuji from Arakura-yama Sengen Park** — `File:View towards Mount Fuji from Arakurayama Sengen Park in Fujiyoshida, Yamanashi, Japan, 2024 May - 2.jpg`

### Traditional Village
- **Shirakawa-go in snow (UNESCO)** — `File:Shirakawago village and snowy mountain (13087582315).jpg`

### City — Landmarks
- **Kabukicho neon gate, Shinjuku** — `File:Kabukicho red gate and colorful neon street signs at night, Shinjuku, Tokyo, Japan.jpg`
- **Shinjuku Gyoen + DoCoMo tower** — `File:Shinjuku Gyoen National Garden and NTT DoCoMo Yoyogi Building, Tokyo, Japan.jpg`
- **Tokyo Skytree worm's-eye view** — `File:Worm's-eye view of Tokyo Skytree with vertical symmetry impression, a sunny day, in Japan.jpg`

### Everyday Life
- **Shibuya Scramble Crossing** — `File:Tokyo Shibuya Scramble Crossing 2018-10-09.jpg`
- **Omotesando crowd, Harajuku** — `File:Street crowd reflecting in the polyhedral mirrors of the station Tokyu Plaza Omotesando, Harajuku, Tokyo, Japan.jpg`
- **Kappabashi cup-shaped balconies** — `File:Cream and red coffee cup-shaped balconies, Niimi Tableware, Kappabashi Dougu Street, Tokyo, Japan.jpg`

### Temples
- **Kiyomizu-dera North Gate** — `File:Four ladies wearing a yukata in front of the North Gate of Kiyomizu-dera temple Kyoto Japan.jpg`
- **Kinkaku-ji reflection** — `File:Water reflection of Kinkaku-ji Temple a sunny day, Kyoto, Japan.jpg`

## Key Principles

1. **Always verify the license** — Wikimedia Commons files carry their own licenses. The query filters for CC licenses, but confirm on the file page if strict attribution is needed.
2. **Use `iiurlwidth=1200`** for a good balance of quality and file size. Use `iiurlwidth=1920` for full-resolution needs.
3. **Namespace 6 is images** — always include `srnamespace=6` in search queries.
4. **Filter to CC licenses** — use `srfilters=license:cc-by-3.0,cc-by-sa-3.0,cc-by-4.0,cc0-1.0` to exclude GFDL-only files (which require text-only attribution that's harder to satisfy with images).
5. **File titles use spaces and are case-sensitive** — copy exact titles from the search results into the imageinfo query.

## Fallback: Web Search for Other Sources

If Wikimedia Commons doesn't have what you need, search for Unsplash, Pexels, or Pixabay results. Stock photo APIs (Unsplash, Pexels) require API keys — if the user doesn't have one, search via DuckDuckGo image search or construct direct URLs like `https://unsplash.com/s/photos/japan+<keyword>`.
