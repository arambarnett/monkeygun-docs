# TokenSnapshot

One asset at one moment. The shape tokenslop sends for every token video and the exchange listing shape.

```json
{
  "symbol": "AI",
  "name": "Artificial Inu",
  "address": "0x2e8c…",
  "chain": "robinhood",
  "priceUsd": 0.22,
  "change24hPct": -8.7,
  "change7dPct": 41.2,
  "volume24hUsd": 1200000,
  "marketCapUsd": 223000000,
  "liquidityUsd": 940000,
  "holders": 52772,
  "trades24h": 3140,
  "ageDays": 12,
  "imageUrl": "https://…/ai.png",
  "website": "https://…",
  "x": "https://x.com/…",
  "asOf": "2026-09-25T00:00:00Z"
}
```

| Key | Type | Spoken as |
|---|---|---|
| `symbol`, `name` | string | "Artificial Inu, A I" |
| `priceUsd` | number | "twenty-two cents"; sub-cent prices are read as "a third of a millionth of a dollar" when you add `priceSpoken` |
| `change24hPct`, `change7dPct` | number | "down eight point seven percent" |
| `volume24hUsd`, `marketCapUsd`, `liquidityUsd` | number | "one point two million dollars in volume" |
| `holders`, `trades24h` | integer | "fifty-two thousand holders" |
| `ageDays` | integer | "twelve days old" |
| `imageUrl` | URL | The logo, used as the opening still and as the seed for a logo clip |

Add any extra keys you have (`fdvUsd`, `top10HoldersPct`, `listingDate`); they become facts too. Add `<key>Spoken` string fields when you want a figure said a particular way.

## A movers report from a list

```json
{ "asOf": "…", "window": "24h",
  "movers": [
    { "symbol": "AI", "name": "Artificial Inu", "change24hPct": 41.2, "volume24hUsd": 1200000, "iconUrl": "https://…/ai.png" },
    { "symbol": "GOKU", "name": "Goku", "change24hPct": -18.0, "volume24hUsd": 310000, "iconUrl": "https://…/goku.png" }
  ] }
```

Each item's `iconUrl` becomes a still in order, so an authored script can put `stillIndex: 1` on the $AI scene and `stillIndex: 2` on the $GOKU scene (index 0 is the top-level `imageUrl`).

<figure><img src="https://api.monkeygun.com/api/media/videos/vid-316/vid-316-thumb.jpg" alt="Trenches Report"><figcaption><p>Trenches Report, a tokenslop show cut from a movers list (vid-316).</p></figcaption></figure>
