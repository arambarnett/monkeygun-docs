# Scheduled shows

An episode every day, or every time your data moves, with no scheduler on your side.

Two ways to run a show. Pick by who owns the trigger.

## You own the trigger

Call `from-data` with `channelId`, `showId` and `seriesId` whenever your system decides an episode should exist: a new listing, a mover crossing a threshold, a nightly recap. The show's defaults and brand lock apply, the episode is filed, and the webhook tells you when it is ready. This is how tokenslop runs its nightly shows.

## Monkeygun owns the trigger

```bash
curl -X POST https://api.monkeygun.com/v1/tools/start_series -H "Authorization: Bearer $MK_KEY" \
  -d '{ "channelId": "yourexchange", "showId": "movers-report", "seriesId": "daily",
        "kind": "schedule", "schedule": "weekdays 8am",
        "url": "https://yourexchange.com/markets",
        "policy": "hold", "destination": "share-link" }'
```

| Field | Values |
|---|---|
| `kind` | `page` or `rss`: an episode only when the source changed. `schedule`: an episode every run |
| `schedule` | `hourly`, `every 30m`, `daily 9am`, `weekdays 8am`, `weekly mon 9am` |
| `url` | The page or feed to read (for `page` and `rss`, and as the source for `schedule`) |
| `policy` | `hold` (episode waits for review; `episode.ready` fires), `digest`, `review` (an AI reviewer checks each render, then posts it or holds it with the issues), `autopost` |
| `destination` | `share-link`, `download`, `buffer` (connect Buffer under Settings → Publishing) |

The first check is a silent baseline. Quiet checks are success and cost 1 credit (+5 when a browser fetch is needed). Each episode costs like a video from your account; a short wallet pauses the series and notifies you.

Manage it: `run_series` (check now; `dry: true` previews), `pause_series`, `list_series`, `list_notifications`.

## Autopilot

Autopilot is the shortest path to a show that runs itself: point it at a source, pick one of the suggested shows, choose where it posts. Every episode is designed from the fresh data, rendered and posted on the schedule. The routes are under `/v1` with your API key.

```bash
# 1. Read a source and get show ideas for it
curl -X POST https://api.monkeygun.com/v1/autopilot/suggest -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{ "source": { "kind": "json", "url": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=10" } }'
# → { "source": { … }, "shows": [ { "title": …, "premise": …, "cadence": …, "style": …, "format": …, "targetSeconds": …, "sampleEpisodeTitle": … }, … ] }

# 2. Start one
curl -X POST https://api.monkeygun.com/v1/autopilot/start -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "source": { "kind": "json", "url": "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=10" },
    "show": { "title": "Top 10 Daily", "premise": "The biggest 24h moves in the top 10, one story per day.",
              "cadence": "daily 9am", "targetSeconds": 30, "style": "trading-terminal",
              "link": { "url": "https://yourexchange.com/markets", "label": "Trade on yourexchange" }, "voiceId": "pFZP5JQG7iQjIQuC4Bku", "language": "English" },
    "destinations": { "buffer": { "channelIds": ["66f0…"] } },
    "policy": "review",
    "tz": "America/New_York"
  }'
# → { "channelId": "autopilot-…", "showId": "top-10-daily-…", "seriesId": "ap-…", "nextRunAt": "…", "firstVideoId": "vid-…", "policy": "review", "creditsPerEpisode": 250 }
```

| Route | What it does |
|---|---|
| `GET /autopilot/starters` | Ready-made sources with no URL needed: Pokémon card prices, top 10 crypto, top stock gainers, weather for a city, Hacker News |
| `POST /autopilot/suggest` | `{ source: { kind, url } }` or `{ starter, city? }`. `kind` is `url`, `rss`, `json`, `csv` or `pricecharting` |
| `GET /autopilot/voices` | House voices, your cloned voices and the language list |
| `POST /autopilot/start` | Creates the show and makes episode one right away |
| `GET /autopilot` | Your shows, with cadence, policy, destinations, next run and the last five episodes |
| `PATCH /autopilot/{seriesId}` | Change `cadence`, `policy`, `destinations`, `channelIds`, `title`, `premise`, `link`, `targetSeconds`, `style`, `format`, `tz`, `voiceId`, `language`, `paused` |
| `POST /autopilot/{seriesId}/pause`, `/resume` | Stop or restart the schedule |
| `POST /autopilot/{seriesId}/episodes/{videoId}/approve` | Post an episode that is waiting for approval |

`cadence` is `daily 9am`, `weekly mon`, `hourly` or `weekdays`, or a clock like `daily 7am`, `weekly fri 5pm` or `every 30m`. `targetSeconds` snaps to 15, 30, 60 or 90. An episode costs 250 credits up to 30 seconds, 300 up to 60 and 350 up to 90. Without Buffer channels the policy defaults to `hold` and episodes get a share link; with channels it defaults to `review`. `link` is the money link, `{ url, label }`: the end card shows it, and each post is the episode title plus the link.

## Data-driven triggers

Threshold rules (a rate crosses X, TVL moves Y percent, a wallet moves more than Z) are not in `start_series` today. Run those on your side and call `from-data`, or ask us to run them as part of a [Data Shows](../packages.md) engagement.
