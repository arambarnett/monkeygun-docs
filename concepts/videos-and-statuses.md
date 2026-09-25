# Videos and statuses

The lifecycle of a video and the shape every endpoint returns.

## Lifecycle

```
draft → scripted → rendering → rendered
                            ↘ error   (lastError says why; the render charge is refunded)
```

| Status | Meaning |
|---|---|
| `draft` | Reserved id, nothing made yet (rare; async jobs only) |
| `scripted` | Script, voice and visuals exist. `POST /videos/{id}/render` produces the file |
| `rendering` | In the render queue or rendering. `from-data` returns 202 in this state |
| `rendered` | File exists. `renderUrl` is set |
| `error` | Creation or render failed. `lastError` has the reason. Paid steps that failed are refunded |

There is no `ready`, `failed` or `done` status on a video. (`done` and `failed` exist on [jobs](../guides/async-jobs.md).)

## The video object

Every call that returns a video (`from-data`, `GET /videos/{id}`, render, edit, the tool catalog) returns this shape:

```json
{
  "videoId": "vid-391",
  "title": "Artificial Inu ($AI)",
  "status": "rendered",
  "duration": 29.4,
  "format": "9:16",
  "language": "en",
  "version": 1,
  "scenes": [{ "n": 1, "type": "title", "text": "…", "duration": 3, "media": "source image" }],
  "captions": true, "presenter": false, "music": true,
  "sourcePackId": "src-2fbd3c", "sourceUrl": null,
  "edits": [],
  "video": "/api/videos/vid-391/file/vid-391.mp4",
  "public": true,
  "mediaKey": "cb66914c20d5ae776c90",
  "url": "https://api.monkeygun.com/api/media/videos/vid-391/vid-391.mp4?k=cb66…",
  "renderUrl": "https://api.monkeygun.com/api/media/videos/vid-391/vid-391-v1.mp4?k=cb66…",
  "thumbnail": "https://api.monkeygun.com/api/media/videos/vid-391/vid-391-thumb.jpg?k=cb66…",
  "watchUrl": "https://monkeygun.com/w/vid-391?k=cb66…",
  "check": { "warnings": [] },
  "lastError": null,
  "cost": { "credits": 60, "breakdown": [ { "type": "script", "count": 1, "credits": 20 } ] },
  "charged": 60,
  "external_id": "listing-AI-2026-09-25"
}
```

- `video` is a relative path that needs a session or the media key. Use `url` or `renderUrl` instead.
- `version` increments on every edit and re-render. `renderUrl` always points at the file for the current version.
- `cost` is recorded on videos made through the API and the studio. It is `null` on scheduled series episodes today.
- `charged` is what this call spent. The render charge (10 credits per started minute) lands when the render finishes and is not echoed in the 202.

## Versions and edits

`POST /videos/{id}/edit { notes }` rewrites the script from your notes and returns the video as `scripted` with `version + 1`; render again to get a new file. Send `script` instead of `notes` to control it exactly. `list_versions` and `restore_version` in the tool catalog move between versions.
