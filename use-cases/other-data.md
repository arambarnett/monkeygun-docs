# Other data feeds

Stocks, indices, ETFs, FX and weather are built in. Anything else arrives as JSON.

## Built-in feeds: market_data

```bash
curl -X POST https://api.monkeygun.com/v1/tools/market_data -H "Authorization: Bearer $MK_KEY" \
  -d '{ "kind": "stock", "symbols": ["NVDA", "^IXIC"], "range": "7d" }'
```

```json
{ "sourcePackId": "src-9a1f…", "facts": ["NVDA: $181.42, +3.1% over 7d, high $184.10, low $174.90", "…"], "series": { "NVDA": [ … ] } }
```

| `kind` | Source | `symbols` |
|---|---|---|
| `crypto` | CoinGecko | coins by symbol or name |
| `stock` | Yahoo Finance | tickers, indices (`^IXIC`, `^GSPC`), ETFs |
| `fx` | Frankfurter | currency codes, vs `base` (default USD) |
| `weather` | Open-Meteo | a place name |

`range` is `1d`, `7d`, `30d`, `90d` or `1y`. Free. The returned `sourcePackId` goes straight into `create_video`, and the `series` drops into a [chart scene](../guides/authored-scripts.md#charts).

```bash
curl -X POST https://api.monkeygun.com/v1/videos -H "Authorization: Bearer $MK_KEY" \
  -d '{ "brief": "The week in AI stocks, 30 seconds, for retail investors. End on the newsletter CTA.", "sourcePackId": "src-9a1f…", "targetSeconds": 30, "images": "none", "brand": { "pack": "editorial" } }'
```

## Any other JSON

Anything with numbers works the same way through `from-data`'s `data`: a listing, a filing, a fitness week, a sports box score, a real-estate comp sheet. Name money fields with `Usd`, percentages with `Pct`, and give items an `imageUrl`, and the narration and stills fall into place.

```json
{ "data": {
    "listing": "2-bed loft, Williamsburg", "priceUsd": 1450000, "pricePerSqftUsd": 1208, "daysOnMarket": 9,
    "comps": [ { "address": "…", "soldUsd": 1390000, "imageUrl": "https://…" }, { "address": "…", "soldUsd": 1510000, "imageUrl": "https://…" } ] },
  "title": "Is $1.45M fair for this loft?", "brief": "30 seconds for buyers. Lead with price per square foot, compare the two comps, end on the open-house CTA.", "cta": "Open house Sunday 1–3" }
```

[![A telehealth brand's patient journey, cut from their site and intake data (LevelUpRX, a Monkeygun customer).](https://monkeygun.com/deck/leveluprx.jpg)](https://monkeygun.com/deck/v-leveluprx-journey.mp4)

{% embed url="https://monkeygun.com/deck/v-leveluprx-journey.mp4" %}
A telehealth brand's patient journey, cut from their site and intake data (LevelUpRX, a Monkeygun customer).
{% endembed %}

## Feeds that keep producing

A page that changes (`kind: "page"`), an RSS feed (`kind: "rss"`) or a clock (`kind: "schedule"`) can run a series without you calling anything. See [Scheduled shows](../guides/scheduled-shows.md). `connect_feed` registers a source on a channel's knowledge graph after a real fetch, so later episodes can cite it.

## Regulated content

Yield rates, health, financial advice: put the disclaimer and the as-of language on the channel so every episode inherits it, and send your own `script` when the words must be exact. The grounding rule holds everywhere: a figure absent from the payload cannot appear on screen.
