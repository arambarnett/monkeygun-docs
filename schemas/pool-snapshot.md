# PoolSnapshot

A yield pool with its rate decomposed. The shape for rate videos where every number must trace to the feed.

```json
{
  "protocol": "Superform",
  "chain": "base",
  "pool": "USDC Vault",
  "poolUrl": "https://…",
  "asset": "USDC",
  "apyPct": 26.0,
  "apyBasePct": 0.0,
  "apyRewardPct": 26.0,
  "tvlUsd": 18400000,
  "tvlChange7dPct": 12.5,
  "utilizationPct": 71.0,
  "benchmarkName": "US savings account average",
  "benchmarkApyPct": 0.45,
  "asOf": "2026-09-25T00:00:00Z",
  "source": "DefiLlama",
  "imageUrl": "https://…/superform.png"
}
```

| Key | Type | Notes |
|---|---|---|
| `apyPct` | number | Headline rate |
| `apyBasePct` | number | The part paid by borrowers or fees. The honest number |
| `apyRewardPct` | number | The part paid in emissions |
| `tvlUsd`, `tvlChange7dPct` | number | Size and momentum |
| `benchmarkName`, `benchmarkApyPct` | string, number | For "beat your bank" comparisons |
| `asOf`, `source` | string | Shown on screen under a compliance preset |

## Compliance presets

For yield content, lock these on the channel so every episode inherits them:

- Disclaimer with the `asOf` timestamp and `source` on every frame.
- Current-rates language only: no future tense, no projections, no annualising a short window. Say it in the show's `styleNotes` and the director follows it; with an authored script you control the words.
- The renderer draws every numeral from the payload; a figure absent from the payload cannot appear.

## Authored Rate Split scene set

```json
"scenes": [
  { "type": "title", "text": "How much of this 26% is real?", "duration": 4, "motion": "slam", "sfx": "riser", "stillIndex": 0 },
  { "type": "chart", "text": "USDC Vault · APY split", "duration": 6, "chart": { "kind": "bars", "series": [ { "t": "borrowers", "v": 0.0 }, { "t": "emissions", "v": 26.0 } ], "valueFormat": "pct", "title": "DefiLlama · as of Sep 25" } },
  { "type": "data", "text": "Beat your bank?", "duration": 5, "stats": [ { "value": "26.0%", "label": "this pool" }, { "value": "0.45%", "label": "savings average" } ] },
  { "type": "cta", "text": "Current rates. Not advice. superform.xyz", "duration": 3 }
]
```
