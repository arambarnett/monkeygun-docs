# Voices, languages and captions

Pick who narrates, in which language, and get post text written for each video.

These options apply to designed videos: `from-data` (the default designed path), `POST /v1/videos/token` and Autopilot shows.

## Voices

`voiceId` picks the narrator. Leave it out for the house default (George, a warm narrator).

```bash
curl -X POST https://api.monkeygun.com/v1/tools/list_voices \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" -d '{}'
```

```json
{
  "house": [
    { "voiceId": "JBFqnCBsd6RMkjVDRZzb", "name": "George — warm narrator (house default)", "previewUrl": "https://…" },
    { "voiceId": "EXAVITQu4vr4xnSDxMaL", "name": "Sarah — clear, friendly", "previewUrl": "https://…" },
    { "voiceId": "onwK4e9ZLuTAKqWW03F9", "name": "Daniel — deep, confident", "previewUrl": "https://…" },
    { "voiceId": "XB0fDUnXU5powFXDhCwa", "name": "Charlotte — bright, modern", "previewUrl": "https://…" },
    { "voiceId": "pFZP5JQG7iQjIQuC4Bku", "name": "Lily — calm, precise", "previewUrl": "https://…" }
  ],
  "cloned": []
}
```

`house` also lists more ElevenLabs premade voices after these five. `cloned` holds the voices your account cloned with `clone_voice`, which needs recorded consent. You can use a house voice, an ElevenLabs premade voice or your own clone. Another account's clone is refused.

`voiceover: false` makes a video with no narration.

## Languages

`language` sets the narration and every word on screen. It takes a name or a code.

| Language | Code |
|---|---|
| English (default) | `en` |
| Spanish | `es` |
| Portuguese (Brazil) | `pt-BR` |
| French | `fr` |
| German | `de` |
| Italian | `it` |
| Turkish | `tr` |
| Indonesian | `id` |
| Japanese | `ja` |
| Korean | `ko` |
| Chinese (Simplified) | `zh-CN` |
| Hindi | `hi` |
| Arabic | `ar` (right to left) |

Figures are spoken as words in that language, and labels the pipeline writes (source line, disclaimer) are translated. Japanese, Korean and Chinese are timed by characters, not words. Another plausible language name, like `"Dutch"`, is written in that language, but the pipeline labels stay in English. Input that is not a language name returns `400`.

Pick a voice that speaks the language well. The house voices are English narrators; `list_voices` shows others, and a clone recorded in the language works best.

```bash
curl -X POST https://api.monkeygun.com/v1/videos/from-data \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "title": "Artificial Inu ($AI)",
    "data": { "symbol": "AI", "priceUsd": 0.22, "change24hPct": -8.7, "volume24hUsd": 1200000 },
    "cta": "在 yourexchange.com 交易 $AI",
    "language": "zh-CN",
    "format": "9:16", "targetSeconds": 30
  }'
```

## Pace

Narration runs at a calm pace by default. Each line gets a word budget for its scene, about 2.3 words a second in English, where a spoken figure counts as about five words. A line that is too long is sent back to the designer and rewritten before anything is recorded. A line that still runs a little long is not sped up to fit. The next line starts later instead.

## Captions

Every designed video comes with a `caption`: post text the designer wrote for that video. It is one to three short lines, under 240 characters, leads with the most surprising true thing in the video, and has no hashtags or links. Its figures come from your data through the same slots as the voiceover, so the model cannot type a number, and the check rejects a caption that tries.

`caption` is on `GET /v1/videos/{id}` and on the `video.rendered` webhook.

```json
{ "videoId": "vid-512", "title": "Kraken movers, Sunday",
  "caption": "QNT is Kraken's top USD gainer today, up 11.2% since midnight UTC.\nBTC still led volume at $101.8M and moved just 0.2%." }
```

Scheduled shows without a money link post the caption, plus the source link. For a one-off post, pass it to [`publish`](publishing.md) as `caption`, or per network as `captions`.
