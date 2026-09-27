# Exchange movers desk

A daily "top movers" short for an exchange's users, built from its own market data.

**For:** exchanges, brokers and market-data companies that want a post every morning without a content team.

**Example:** "Kraken Movers", made from Kraken's public ticker API: [watch it on X](https://x.com/monkeygunhq/status/2104226218627272773).

## The data

Kraken's public REST API, no key needed:

- `GET https://api.kraken.com/0/public/AssetPairs` for pair names and quote currency.
- `GET https://api.kraken.com/0/public/Ticker` for every pair: last price `c[0]`, today's open `o` (00:00 UTC), 24h volume `v[1]` and 24h volume-weighted price `p[1]`.

Keep USD pairs, compute the change since the open, compute 24h USD volume as `v[1] × p[1]`, and drop thin pairs (under $1M of volume). Send the result, not the raw feed:

```json
{
  "asOf": "Sep 27, 2026 · 14:55 UTC",
  "window": "change since 00:00 UTC today; volume = rolling 24h in USD",
  "usdPairsTracked": 621, "pairsOver1M": 59,
  "gainers": [
    { "asset": "QNT", "changePct": 11.16, "lastUsd": 168.51, "volume24hUsd": 34629709 },
    { "asset": "WLD", "changePct": 8.69, "lastUsd": 0.5668, "volume24hUsd": 8382085 }
  ],
  "decliners": [ { "asset": "DASH", "changePct": -6.4, "lastUsd": 67.256, "volume24hUsd": 4974891 } ],
  "mostTraded": [ { "asset": "BTC", "volume24hUsd": 101805900, "changePct": 0.22, "lastUsd": 84611.7 } ]
}
```

## The call

```bash
curl -X POST https://api.monkeygun.com/v1/videos/from-data \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "Kraken movers, Sunday",
    "data": { …the JSON above… },
    "brief": "A 25-second daily movers short for exchange users. Open on the top gainer, then the top four gainers, the biggest decliners, and BTC as the anchor. State the window on screen. No advice, no predictions.",
    "cta": "Trade on yourexchange.com",
    "style": "trading-terminal", "format": "9:16", "targetSeconds": 25,
    "brand": { "accent": "#39FF7A", "watermark": "yourexchange.com" }
  }'
```

## What comes out

A 9:16 video with the top gainer as the hero number, a bar board of the top gainers against BTC, the as-of time and the source on every frame, a voiceover and a post `caption` like "QNT is Kraken's top USD gainer today, up 11.2% since midnight UTC." Every figure comes from `data`.

## Run it every day

Call it from your own cron after the daily open, or let Monkeygun run it: see [Scheduled shows](../guides/scheduled-shows.md). Post it with [Publishing](../guides/publishing.md).
