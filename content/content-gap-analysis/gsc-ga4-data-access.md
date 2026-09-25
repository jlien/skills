# GSC + GA4 Data Access — Pull Recipes

Companion to `SKILL.md`. All recipes here were verified live on 2026-09-25
with read-only calls (one GSC domain property, one GA4 property) from a
macOS host: LibreSSL-derived OpenSSL 3.x, rbenv Ruby.

## Inputs to gather

| Asset | Example | Note |
|---|---|---|
| Service-account JSON | `$SA_JSON` (any path you control) | needs `webmasters.readonly` + `analytics.readonly` scopes |
| Extracted PEM | `/tmp/sa_key.pem` | extract + chmod 600; see below |
| GSC site URL | `sc-domain:<domain>` | domain property; URL-prefix type uses the full origin |
| GA4 property | numeric id, no `properties/` prefix | from GA4 admin → property settings |

The SA must be added as a delegated user/viewer on the target properties
before any call succeeds. Never paste a real property id or SA path into
committed files — export them as environment variables at run time.

## Auth: JSON → PEM → token

The SA private key is PKCS#8 `BEGIN PRIVATE KEY`. macOS LibreSSL's
`openssl dgst -sign` can refuse it (EncryptedPrivateKeyInfo errors), so
extract the inner PEM with Ruby first:

```bash
export SA_JSON=/secure/path/service-account.json
ruby -rjson -e 'File.write("/tmp/sa_key.pem", JSON.parse(File.read(ARGV[0]))["private_key"].to_s)' "$SA_JSON"
chmod 600 /tmp/sa_key.pem
```

Mint a token (JWT bearer flow, ~1 hour TTL):

```bash
PEM=/tmp/sa_key.pem
iss=$(ruby -rjson -e 'print JSON.parse(File.read(ARGV[0]))["client_email"]' "$SA_JSON")
now=$(date +%s)
b64() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }
JWT=$(printf '{"alg":"RS256","typ":"JWT"}' | b64).$(printf \
  '{"iss":"%s","scope":"https://www.googleapis.com/auth/webmasters.readonly","aud":"https://oauth2.googleapis.com/token","iat":%s,"exp":%s}' \
  "$iss" "$now" "$((now+3600))" | b64)
ASSERTION="${JWT}.$(printf '%s' "$JWT" | openssl dgst -sha256 -sign "$PEM" -binary | b64)"

TOKEN=$(curl -s https://oauth2.googleapis.com/token \
  -d grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer \
  -d assertion="$ASSERTION" \
  | ruby -rjson -e 'print JSON.parse(STDIN.read)["access_token"]')
case ${#TOKEN} in [0-9][0-9][0-9]) echo "token len OK";; *) echo "token suspicious"; exit 1;; esac
```

Notes:
- JWT member order does not matter; the signature covers the exact
  `header.payload` string as encoded — b64 must be base64url (unpadded).
- Ruby parses the PKCS#8 key directly and can sign the RS256 JWT itself
  (`OpenSSL::PKey::RSA`), skipping the OpenSSL CLI entirely — the cleaner
  path when a Ruby runtime is available.

## GSC: search analytics

Endpoint: `POST https://searchconsole.googleapis.com/webmasters/v3/sites/{site_url}/searchAnalytics/query`
Scope: `https://www.googleapis.com/auth/webmasters.readonly`.

```bash
SITE="sc-domain:example.com"
enc() { ruby -rcgi -e 'print CGI.escape(ARGV[0])' "$1"; }
START=$(date -v-91d +%F); END=$(date -v-2d +%F)   # macOS; GNU: date -d '91 days ago'

curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  "https://searchconsole.googleapis.com/webmasters/v3/sites/$(enc "$SITE")/searchAnalytics/query" \
  -d "{\"startDate\":\"$START\",\"endDate\":\"$END\",\"dimensions\":[\"query\"],\"rowLimit\":25000}" \
  -o gsc_queries.json

# pages + query-page pairs: change dimensions accordingly
#   ["page"]        → gsc_pages.json
#   ["query","page"]→ gsc_pairs.json
```

Verified response shape (2026-09-25):

```json
{"rows": [{"clicks": 1, "impressions": 18, "ctr": 0.0555, "position": 4.22, "keys": ["example query one"]}]}
```

- The API caps at **25,000 rows per request**; `startRow` paginates forward
  in 25,000-row steps.
- Filter to ≥10 impressions and non-brand AFTER pulling; the API supports
  `dimensionFilterGroups` but client-side filtering is more transparent.
- 3-month single-call pulls: prefer `startDate = today−92d`, `endDate = today−2d`
  (data lag ~2 days), `rowLimit: 25000`.
- Property permission errors return HTTP 403 (insufficient permission): the SA
  must be added as a delegated user on the GSC property; a wrong property
  string usually 404s instead.

## GA4: Data API runReport

Endpoint: `POST https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport`
Scope: `https://www.googleapis.com/auth/analytics.readonly`.

```bash
PROPERTY=123456789   # numeric id, no "properties/" prefix
START=$(date -v-91d +%F); END=$(date -v-2d +%F)

curl -s -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  "https://analyticsdata.googleapis.com/v1beta/properties/$PROPERTY:runReport" \
  -d "{\"dateRanges\":[{\"startDate\":\"$START\",\"endDate\":\"$END\"}],\"dimensions\":[{\"name\":\"landingPage\"}],\"metrics\":[{\"name\":\"sessions\"}],\"limit\":25000}" \
  -o ga4_landings.json
```

Verified response shape (2026-09-25):

```json
{"dimensionHeaders":[{"name":"landingPage"}],"metricHeaders":[{"name":"sessions","type":"TYPE_INTEGER"}],
 "rows":[{"dimensionValues":[{"value":"/blog/example-post"}],"metricValues":[{"value":"25"}]}],
 "rowCount": 123}
```

- Verified metric types: `sessions → TYPE_INTEGER`, `keyEvents → TYPE_FLOAT`.
  Metric/type strings come straight from the response's `metricHeaders`; do
  not hardcode assumptions about them.
- Keep pulls to 90 days; longer ranges raise the chance of hitting the API's
  per-request quota and row caps.

## Ruby alternative (no shell quoting)

A thin Ruby client does the whole flow with stdlib only: `net/http` + `json`
for the calls, `OpenSSL::PKey::RSA` to sign the RS256 JWT — no google-auth
gem. Sign `iss`/`scope`/`aud`/`iat`/`exp`, POST the assertion to the token
endpoint, then POST JSON bodies to the same endpoints above. Keep one method
per service (queries, runReport) and pass dates/dimensions in as arguments;
the property id and SA paths stay in environment variables.

## Pitfalls

1. **Property mismatch**: a 403 on GSC means the SA lacks property access —
   add it as a user, don't retry with a different property string hoping.
2. **`position` is not a rank** — impression-weighted average across SERP
   layouts. Treat 1–2 excellent, 3–10 page one, 11–20 page two.
3. **25,000-row cap is per request.** Long date ranges on big sites need
   date-chunked pulls merged client-side.
4. **GA4 landingPage keeps null / "(other)" entries and query strings.**
   Normalize: strip query strings, drop `"/"` alone when not meaningful.
5. **Data lag 2–3 days.** Pulling through today's date returns zero rows for
   the newest days silently; end at today−2.
6. **Human-provided exports vary.** GSC UI exports can be tab- or
   semicolon-delimited with percent-formatted CTR; sniff the delimiter and
   verify number formats before trusting a parse. API JSON avoids all of this.
7. **Property ID shape**: the path must be `properties/<numeric-id>`. A
   `properties/properties/<id>` paste or a UA-style id (`UA-...`) fails with a
   shape error, not a permission error.
8. **Secrets hygiene**: never commit `SA_JSON` values, property ids, or
   domain property strings into skill files or PR text — they are plain
   environment inputs.
