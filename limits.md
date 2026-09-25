# Limits

What to design around.

| Limit | Value |
|---|---|
| Render concurrency | 3 renders in parallel, shared across accounts, first come first served |
| Director call | 150 s cap. Send `script` to skip it |
| Creation with clips or AI video | 2 to 8 minutes. Use `async: true` |
| Webhook delivery | One attempt, 15 s timeout, no retry. Last 100 attempts readable |
| Upload | 250 MB per file |
| Stills from `data` | First 60 facts; one still per item with an image key, downloaded with a 15 s timeout each |
| Runtime | 1 s stings to long form; under 3 s is silent by default |
| AI clip length | MiniMax 5 to 15 s, Kling 5 or 10 s, Seedance Fast 4 to 15 s, Seedance 2.5 4 to 30 s |
| Image-to-video seed | 300 px minimum (smaller stills are placed on a full-frame canvas automatically) |
| Chart points | 2 to 60 on a line, up to 12 bars |
| Stat pills | 2 to 4 per data scene |
| Rate limit | None enforced today. Please stay under 10 creations per minute per key and ask before a bulk run |
| Embed token TTL | 5 minutes to 7 days |

All API accounts share one render region. Serve `renderUrl` through your own CDN for viewers far from it.
