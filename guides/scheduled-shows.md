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
| `policy` | `hold` (episode waits for review; `episode.ready` fires), `digest`, `autopost` |
| `destination` | `share-link`, `download`, `buffer` (connect Buffer under Settings → Publishing) |

The first check is a silent baseline. Quiet checks are success and cost 1 credit (+5 when a browser fetch is needed). Each episode costs like a video from your account; a short wallet pauses the series and notifies you.

Manage it: `run_series` (check now; `dry: true` previews), `pause_series`, `list_series`, `list_notifications`.

## Data-driven triggers

Threshold rules (a rate crosses X, TVL moves Y percent, a wallet moves more than Z) are not in `start_series` today. Run those on your side and call `from-data`, or ask us to run them as part of a [Data Shows](../packages.md) engagement.
