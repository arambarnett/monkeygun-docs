# Sports stat desk

A short on the standings, the race or the stat of the day, from a public stats feed.

**For:** sports media, fantasy and betting-adjacent apps (with no betting advice), team and league content teams.

**Example:** "Game 162: one spot left", on the final day of the 2026 MLB regular season, when the National League's last wild card was still open.

## The data

The MLB Stats API is public:

- `GET https://statsapi.mlb.com/api/v1/standings?leagueId=104&season=2026&standingsTypes=wildCard` for the NL wild-card table (wins, losses, games back, elimination number).
- `GET https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2026-09-27&hydrate=probablePitcher` for today's games and starters.

Send the table and today's games, and put the rules of the race in `facts` so the video explains them correctly:

```json
{
  "asOf": "Sep 27, 2026 · before first pitch",
  "gamesLeft": 1,
  "nlWildCard": [
    { "team": "Padres", "w": 90, "l": 71, "gb": "+3.0" },
    { "team": "Cubs", "w": 88, "l": 73, "gb": "+1.0" },
    { "team": "Phillies", "w": 87, "l": 74, "gb": "—", "status": "holds last spot" },
    { "team": "D-backs", "w": 86, "l": 75, "gb": "1.0", "status": "elimination number 1" }
  ],
  "today": [
    { "game": "Rays @ Phillies", "timeET": "3:05 PM ET", "starters": "Martinez vs Wheeler" },
    { "game": "D-backs @ Padres", "timeET": "3:10 PM ET", "starters": "Soroka vs Vásquez" }
  ]
}
```

## The call

```bash
curl -X POST https://api.monkeygun.com/v1/videos/from-data \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "Game 162: one spot left",
    "data": { …the JSON above… },
    "summary": "Arizona needs a win and a Phillies loss just to finish level. Do not claim who wins a tiebreaker.",
    "brief": "A 25-second scoreboard short. Hook: 161 games down, one spot left. Show the wild-card table with the cut line, explain the elimination number plainly, then the two games side by side. Neutral, no betting talk, no predictions.",
    "style": "swiss-poster", "format": "9:16", "targetSeconds": 25
  }'
```

## What comes out

A 9:16 short with the standings table, a cut line between the last team in and the first team out, both games with start times and starters, and a caption that states the math.

## Run it on game days

Call it from your own scheduler before first pitch on the days that matter, or run a daily show with [Scheduled shows](../guides/scheduled-shows.md).
