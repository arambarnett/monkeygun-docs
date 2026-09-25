# Upload and brand pass

Take a clip your user already made, stamp it with your watermark and a branded end card, and put it in your feed.

## 1. Upload

```bash
curl -X POST https://api.monkeygun.com/v1/library/upload -H "Authorization: Bearer $MK_KEY" \
  -d '{ "url": "https://x.com/someone/status/123…", "filename": "clip.mp4" }'
# { "ok": true, "assetId": "778324edbbef508c", "filename": "clip.mp4", "mimeType": "video/mp4", "url": "https://api.monkeygun.com/api/…" }
```

`url` accepts any public https file, or a post permalink on X, YouTube, TikTok or Instagram (the media is resolved; public posts only). Send `data` (base64) instead of `url` for a file you already hold. 250 MB per file.

The `assetId` works everywhere a library file is accepted: `libraryAssetIds`, `musicAssetId`, `avatar.imageAssetId`, `attach_asset`, `brand_footage`, `index_footage`, `clean_footage`, `find_highlights`.

## 2. Brand pass

```bash
curl -X POST https://api.monkeygun.com/v1/tools/brand_footage -H "Authorization: Bearer $MK_KEY" \
  -d '{ "assetId": "778324edbbef508c", "channelId": "yourexchange", "cta": "Trade it on yourexchange.com", "endCardSeconds": 3 }'
# { "videoId": "vid-392", "status": "rendering" }
```

5 credits. The channel's logo watermark goes bottom-right and a branded end card (CTA pill plus disclaimer) is appended. Finish through the webhook or a poll like any other video.

## Review

Uploads are user content. tokenslop holds a creator's first three uploads for review before they reach the feed and clears them from an admin queue. Do the same on your side: keep a `review` flag on your record until you have seen it, or until the creator has a track record.
