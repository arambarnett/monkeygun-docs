# Weather desk

A calm, precise weather short from official advisories.

**For:** local news, weather apps, insurers and travel brands that want a timely post when the weather matters.

**Example:** "Five storms, one map", from the National Hurricane Center's advisories on a morning with five tropical systems active at once: [watch it on X](https://x.com/monkeygunhq/status/2104205143936020873).

## The data

- `GET https://www.nhc.noaa.gov/CurrentStorms.json` lists every active system with its position, intensity and a link to its public advisory.
- Each public advisory has the sustained wind in mph, the location in words and any watches or warnings.

Use the advisory's mph figure rather than converting knots yourself, and add the classification rule you want explained as a fact:

```json
{
  "asOf": "Sep 27, 2026, 12:00 UTC",
  "activeSystems": 5, "hurricanes": 3,
  "storms": [
    { "name": "Polo", "type": "Hurricane", "category": 3, "windMph": 120, "lat": 20.7, "lon": -113.7,
      "where": "285 mi WSW of Cabo San Lucas, Mexico",
      "alert": "Hurricane Warning: Baja California Sur coasts" },
    { "name": "Nolo", "type": "Hurricane", "category": 2, "windMph": 100, "lat": 16.5, "lon": -157.3,
      "where": "335 mi S of Honolulu, Hawaii" },
    { "name": "Fay", "type": "Tropical Depression", "windMph": 35, "lat": 29.2, "lon": -43.9,
      "where": "1,145 mi WSW of the Azores" }
  ]
}
```

## The call

```bash
curl -X POST https://api.monkeygun.com/v1/videos/from-data \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "Five storms, one map",
    "data": { …the JSON above… },
    "summary": "Category 3 means sustained winds of 111 to 129 mph (Saffir-Simpson). Polo is the only major hurricane.",
    "brief": "A 25-second weather-desk short. Hook: five systems on one map. Plot them to scale, then Polo and its warnings, then the rest. Calm broadcast-meteorologist tone, no fear-mongering; tell people in the warning area to follow local officials.",
    "style": "breaking-news", "format": "9:16", "targetSeconds": 25
  }'
```

## What comes out

A 9:16 short with a map, the count of systems, the strongest storm's category and warnings, the as-of time and the source on every frame.

## Run it

Advisories update every few hours. Call it when a new advisory changes something you care about, or run a daily forecast show with the `weather-city` Autopilot starter. See [Scheduled shows](../guides/scheduled-shows.md#autopilot).
