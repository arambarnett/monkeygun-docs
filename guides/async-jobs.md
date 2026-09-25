# Async jobs

Creations with AI clips or full AI video can take minutes. Ask for a job id and poll it.

Add `"async": true` to any `from-data` call.

```bash
curl -X POST https://api.monkeygun.com/v1/videos/from-data -H "Authorization: Bearer $MK_KEY" \
  -d '{ "async": true, "title": "…", "brief": "…", "data": { … }, "clips": { "provider": "kling", "count": 1, "seconds": 5 } }'
```

```json
HTTP 202
{ "ok": true, "jobId": "job-mug7lnzkvw449l", "status": "creating", "poll": "/v1/jobs/job-mug7lnzkvw449l",
  "note": "Creating. Poll the job (videoId appears when the script/voice/images are done), or listen for video.created then video.rendered on your webhook." }
```

The same route runs in the background with the same body. Internal limits still apply (the director call is capped at 150 seconds), so `async` protects you from your own edge timeouts, not from a brief that is too long for the model.

## Poll

```bash
curl https://api.monkeygun.com/v1/jobs/job-mug7lnzkvw449l -H "Authorization: Bearer $MK_KEY"
```

```json
{
  "id": "job-mug7lnzkvw449l",
  "status": "rendering",
  "createdAt": "…", "updatedAt": "…",
  "videoId": "vid-391",
  "videoStatus": "rendering",
  "media": { "public": true, "mediaKey": "cb66…", "url": "https://…/vid-391.mp4?k=cb66…", "renderUrl": null, "thumbnail": null, "watchUrl": "https://monkeygun.com/w/vid-391?k=cb66…" },
  "result": { "videoId": "vid-391", "status": "rendering", "charged": 160, "external_id": "…", "…": "…" },
  "error": null
}
```

| Job status | Meaning |
|---|---|
| `creating` | Script, voice and visuals in progress. No `videoId` yet |
| `rendering` | Video exists; the file is being made. `videoId` and `media` are set |
| `done` | `videoStatus` is `rendered`; `media.renderUrl` plays |
| `failed` | `error` says why. Anything charged for a failed step is refunded |

Poll every 5 to 10 seconds. `video.created` fires with `jobId` when creation finishes; `video.rendered` when the file exists. Jobs are per account; another account's job id is a 404.
