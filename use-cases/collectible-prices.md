# Collectible price show

A daily show about one collectible and what its market did, told as a story.

**For:** card shops, graders, marketplaces, collectors' media and anyone with price history for physical items.

**Example:** "Grail Report", a daily show on one original Pokémon Base Set card per episode: [episode 2, Blastoise](https://x.com/monkeygunhq/status/2104238057423839496).

## The data

- **PriceCharting** item pages give average sale prices by grade (Ungraded, Grade 7 through 9.5 from any grader, PSA 10) with history, and a photo of the card.
- **TCGplayer** gives the market price for raw near-mint copies, the number of listings and sellers, the lowest listing, and the card text.

The two measure different things, so label them apart in `facts`:

```json
{
  "psa10Usd": 6870.66, "psa10YearAgoUsd": 3219.67, "psa10PeakUsd": 8136.07,
  "grade95Usd": 1361.0, "grade9Usd": 1150.0, "grade8Usd": 369.99, "grade7Usd": 257.41,
  "ungradedAvgSaleUsd": 100.0, "ungradedYearAgoUsd": 72.48,
  "tcgplayerMarketUsd": 222.34, "tcgplayerListings": 179, "tcgplayerSellers": 129, "tcgplayerLowestUsd": 42.0,
  "cardNumber": 2, "setSize": 102
}
```

## The call

```bash
curl -X POST https://api.monkeygun.com/v1/videos/from-data \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "Grail Report: Blastoise, Base Set #2",
    "data": { …the JSON above… },
    "summary": "Blastoise, number 2 of 102 in the original Base Set, Stage 2, Pokémon Power: Rain Dance. TCGplayer figures are raw near-mint marketplace data; PriceCharting figures are sale averages in any condition. Grades 7 to 9.5 are PriceCharting buckets from any grader.",
    "imageUrl": "https://…/blastoise-front.jpg",
    "brief": "A calm, story-driven collector show, not a hype reel. Reveal the real card, say who it is, tell the one market story in the data, show the grade ladder, sign off with Tomorrow: another grail.",
    "style": "nature-doc", "format": "9:16", "targetSeconds": 45
  }'
```

## What comes out

A 45-second 9:16 episode built around the real card photo: a slow reveal, the card's power, a one-year chart, the TCGplayer numbers, and a grade ladder from Ungraded to PSA 10.

## Run it daily

The `pokemon-prices` Autopilot starter reads a PriceCharting item, and `source.kind: "pricecharting"` takes any PriceCharting item URL. Rotate items across episodes on your side and call `from-data`, or let Autopilot run one item on a schedule. See [Scheduled shows](../guides/scheduled-shows.md#autopilot).
