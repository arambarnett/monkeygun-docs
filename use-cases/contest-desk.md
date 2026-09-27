# Live contest desk

A news-desk bulletin every few hours for a live competition: a trading contest, a leaderboard, a tournament.

**For:** anyone running a contest with a public scoreboard who wants the story told while it is happening.

**Example:** [Close Call](https://monkeygun.com/live/close-call), a news desk for Flop Labs' close-1 agent trading contest. A new video bulletin every 12 hours, with the latest bulletin at the top of the page and the archive below it.

## The data

Close Call reads the contest referee's public rooms on technocore.chat (state, price, positions and PnL). Each bulletin sends a snapshot plus what changed since the last one:

```json
{
  "agentKeys": 3851347, "newKeysSinceLastBulletin": 890363,
  "longPositions": 454838, "shortPositions": 463606,
  "nvdaMarkUsd": 224.43, "nvdaLow24hUsd": 220.51, "nvdaHigh24hUsd": 225.10,
  "leaderPnlPolf": 92.63, "leaderPeakPnlPolf": 513.62,
  "keysTiedAtTop25Score": 24, "tiedScorePolf": 84.76,
  "hoursToLock": 161, "prizeFlop": 1000000, "prizePlaces": 3
}
```

Facts that are not numbers go in `summary`, for example which key leads, whether the leader changed, and when scores lock.

## The call

```bash
curl -X POST https://api.monkeygun.com/v1/videos/from-data \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "Close Call bulletin, 2026-09-27 15:35 UTC",
    "summary": "Every agent key trades one NVDA future; a referee settles every five minutes; the top three at the lock share the prize. The leading key ends in xu7Hne and held first place since the last bulletin.",
    "data": { …the JSON above… },
    "brief": "A 12-hourly news bulletin. Open on what changed since the last bulletin, then the leader, longs vs shorts, the NVDA range, the tie at the top, time to lock and the prize. Broadcast-news tone, no hype, no advice. Keep the same look every bulletin.",
    "style": "trading-terminal", "format": "16:9", "targetSeconds": 30
  }'
```

## What comes out

A 30-second 16:9 bulletin with a live ticker, count-up numbers that land on the real values, and a sign-off with the next update time.

## Run it on a clock

Your scheduler calls `from-data` every 12 hours with the new snapshot and the diff, and `external_id` set to the bulletin time. Keep `style` fixed so the desk looks the same every time. See [Scheduled shows](../guides/scheduled-shows.md).
