# URL to video

Point it at a page. The facts, stills and brand colors come out of the page, and the script can only say what the page says.

[![Cut from a single URL about the Pokémon card artist Mitsuhiro Arita: facts, stills and palette from the page, nothing invented.](https://monkeygun.com/deck/pokemon.jpg)](https://monkeygun.com/deck/v-mitsuhiro-arita.mp4)

{% embed url="https://monkeygun.com/deck/v-mitsuhiro-arita.mp4" %}
Cut from a single URL about the Pokémon card artist Mitsuhiro Arita: facts, stills and palette from the page, nothing invented.
{% endembed %}

## 1. Read the page

```bash
curl -X POST https://api.monkeygun.com/v1/sources -H "Authorization: Bearer $MK_KEY" \
  -d '{ "url": "https://en.wikipedia.org/wiki/Ken_Sugimori" }'
```

```json
{ "sourcePackId": "src-d6ae14", "title": "Mitsuhiro Arita", "httpStatus": 200,
  "summary": "Mitsuhiro Arita is a Japanese illustrator…",
  "facts": ["Illustrated the original Base Set Charizard in 1996", "…"],
  "stills": [{ "index": 0, "role": "hero", "alt": "page hero" }, { "index": 1, "alt": "Charizard card" }],
  "brand": { "colors": ["#1C2B4A", "#F2C94C"], "fonts": ["Georgia"] } }
```

Pages, PDFs and social posts work. A page that did not load or had no readable text returns `error` on the pack and the create call refuses it, so nothing is made up from a 404.

## 2. Make and render

```bash
curl -X POST https://api.monkeygun.com/v1/videos -H "Authorization: Bearer $MK_KEY" \
  -d '{ "brief": "A 30-second portrait of the artist for card collectors. Open on the Charizard, end on the site.", "sourcePackId": "src-d6ae14", "format": "9:16", "targetSeconds": 30, "images": "source", "captions": true }'
# { "videoId": "vid-012", "status": "scripted", "charged": 50, ... }

curl -X POST https://api.monkeygun.com/v1/videos/vid-012/render -H "Authorization: Bearer $MK_KEY"
```

Or in one call: `from-data` with `sourceUrl` and a `brief`, no `data`.

## Grounding

Every number, name, date and quote in the script must appear in the pack's `facts`. A thin page makes a shorter video rather than a padded one. Pass several pages with `sourcePackIds` on `create_video` to merge them; a `market_data` pack can be one of them.

## Brand from the page

The pack carries the page's colors and fonts. With no `brand` on the call, the first video from a site uses them, and the account's brand kit is learned from it (`learn_brand` does this on demand). Pass `brand` to override.
