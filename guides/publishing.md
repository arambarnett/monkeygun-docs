# Publishing

Send a rendered video to a hosted page, a download link, your Buffer channels or YouTube.

```bash
curl -X POST https://api.monkeygun.com/v1/videos/vid-391/publish \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{ "destination": "share-link" }'
```

The video must be `rendered`. `POST /v1/tools/publish` takes the same body with `videoId` in it.

## Destinations

| `destination` | What happens | Setup |
|---|---|---|
| `share-link` (default) | Returns a hosted page, `https://monkeygun.com/w/{id}?k=…`, with Open Graph tags for X, iMessage, Slack and Discord | None |
| `download` | Returns a keyed MP4 link you can download or re-host | None |
| `buffer` | Posts to your Buffer channels: X, Instagram, TikTok, YouTube, LinkedIn and anything else Buffer connects | Paste a Buffer access token in **Settings → Publishing** |
| `youtube` | Uploads straight to your YouTube channel | **Settings → Publishing → Connect YouTube** |

## Buffer

```bash
curl -X POST https://api.monkeygun.com/v1/videos/vid-391/publish \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "destination": "buffer",
    "autopost": true,
    "caption": "$AI traded $1.2M in its first 24 hours.\nyourexchange.com/ai",
    "captions": {
      "instagram": "$AI traded $1.2M in its first 24 hours. Trade it: link in bio.",
      "tiktok": "$AI, first 24 hours on yourexchange"
    },
    "instagramStory": true
  }'
```

```json
{ "ok": true, "destination": "buffer", "bufferPostId": "66f1…,66f1…,66f1…", "storyPostIds": ["66f1…"], "draft": false,
  "url": "https://api.monkeygun.com/api/media/videos/vid-391/vid-391.mp4?k=cb66…" }
```

| Field | What it does |
|---|---|
| `autopost` | `true` posts now. Leave it out to save a draft in Buffer, so someone approves it there |
| `caption` | Post text for every channel. Without it, the post uses the video's call to action or title |
| `captions` | Post text per Buffer service, keyed by Buffer's service name: `instagram`, `tiktok`, `twitter`, `youtube`, `linkedin`, … A service without an entry uses `caption` |
| `channelIds` | Buffer channel ids to post to. Default: the show's picks, else the channels selected in Settings → Publishing |
| `instagramStory` | With `autopost: true`, also posts the video as a Story on each Instagram channel after the Reel. Story ids come back in `storyPostIds` |

Every Instagram post goes out as a Reel, also shared to the feed. Instagram captions do not make links clickable, so write "link in bio" there and keep the full link for X and LinkedIn.

One channel failing does not stop the others. Failures come back in `failed`, for example `["instagram: …"]`, and `ok` is `false` only when no channel took the post.

`caption` on a designed video is written for this: see [Voices, languages and captions](voices-languages-captions.md#captions).

## YouTube

```bash
curl -X POST https://api.monkeygun.com/v1/videos/vid-391/publish \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{ "destination": "youtube", "privacy": "public", "caption": "$AI: the first 24 hours" }'
```

The title is `captions.youtube`, else `caption`, else the video title, cut to 100 characters. The description is the video's call to action and source link. `privacy` is `public`, `unlisted` or `private`; it defaults to `unlisted`, or `public` with `autopost: true`. The response has the YouTube `url`.

## Scheduled shows

Shows that post themselves use the same channels. See [Scheduled shows](scheduled-shows.md).
