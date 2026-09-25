# Webhooks and polling

The exact payload of every event, how to verify it, and the reconciler you should run beside it.

## Register

```bash
curl -X POST https://api.monkeygun.com/v1/webhooks -H "Authorization: Bearer $MK_KEY" \
  -d '{ "url": "https://yourapp.com/monkeygun", "events": ["video.created", "video.rendered", "video.render_failed"] }'
# { "webhook": { "id": "wh_b5fd", "secret": "whsec_…", "events": [...] } }
```

The URL must be https and publicly routable (private and loopback addresses are refused, and re-checked at send time). `events: ["*"]` subscribes to everything. The secret is shown once.

## Delivery

```
POST https://yourapp.com/monkeygun
Content-Type: application/json
X-Monkeygun-Event: video.rendered
X-Monkeygun-Signature: sha256=<hex HMAC-SHA256(secret, raw request body)>
```

One attempt, 15-second timeout, no retry. Failed attempts are logged; read them with `GET /v1/webhooks/{id}/deliveries` (last 100).

## Payloads

{% tabs %}
{% tab title="video.rendered / video.render_failed" %}
Fires for every finished render on your account: API, studio, embedded studio and scheduled episodes.

```json
{
  "id": "evt_9f2a…", "event": "video.rendered", "createdAt": "2026-09-25T01:12:08.000Z",
  "data": {
    "videoId": "vid-391",
    "external_id": "listing-AI",
    "externalUserId": null,
    "channelId": null, "showId": null, "seriesId": null,
    "title": "$AI just listed",
    "status": "rendered",
    "duration": 29.4,
    "version": 1,
    "url": "https://api.monkeygun.com/api/media/videos/vid-391/vid-391.mp4?k=cb66…",
    "renderUrl": "https://api.monkeygun.com/api/media/videos/vid-391/vid-391-v1.mp4?k=cb66…",
    "thumbnail": "https://api.monkeygun.com/api/media/videos/vid-391/vid-391-thumb.jpg?k=cb66…",
    "watchUrl": "https://monkeygun.com/w/vid-391?k=cb66…",
    "mediaKey": "cb66914c20d5ae776c90",
    "error": null,
    "warnings": []
  }
}
```

On `video.render_failed`, `status` is `error`, `error` has the reason, `renderUrl` is null, and the render charge has been refunded. `externalUserId` is set for videos made in an [embedded studio](../guides/embedded-studio.md) session.
{% endtab %}
{% tab title="video.created" %}
Fires when creation finishes (script, voice, visuals) before the render, and when an async job completes creation.

```json
{ "id": "evt_…", "event": "video.created", "createdAt": "…",
  "data": { "videoId": "vid-391", "external_id": "listing-AI", "channelId": null, "showId": null, "seriesId": null,
            "title": "$AI just listed", "status": "scripted", "duration": 29.4, "format": "9:16",
            "video": "/api/videos/vid-391/file/vid-391.mp4", "error": null, "jobId": "job-…" } }
```

Note this event carries the legacy relative `video` path and no media key; wait for `video.rendered` for playable links.
{% endtab %}
{% tab title="Series events" %}
`episode.ready` (a held episode awaits review), `episode.published` (autoposted or shared), `series.error` (a check or render failed). Same envelope; `data` has `channelId`, `showId`, `seriesId`, `videoId` and a `message`.
{% endtab %}
{% endtabs %}

## Verify

{% tabs %}
{% tab title="Node" %}
```ts
import { createHmac, timingSafeEqual } from "crypto";
export function verify(rawBody: string, header: string, secret: string) {
  const expected = "sha256=" + createHmac("sha256", secret).update(rawBody).digest("hex");
  const a = Buffer.from(header), b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}
```
{% endtab %}
{% tab title="Python" %}
```python
import hmac, hashlib
def verify(raw_body: bytes, header: str, secret: str) -> bool:
    expected = "sha256=" + hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(header, expected)
```
{% endtab %}
{% endtabs %}

Verify over the raw bytes, before JSON parsing.

## The reconciler

Because there is no retry, run a small loop beside the webhook. This is what tokenslop runs every 30 seconds:

```ts
for (const row of db.videosWhere({ status: "rendering", createdBefore: now - 15 })) {
  const v = await mg.get(`/videos/${row.id}`).catch(e => e);        // GET /v1/videos/{id}
  if (v.status === "rendered") markReady(row, v.renderUrl, v.duration);
  else if (v.status === "error") { markFailed(row, v.lastError); refund(row); }
  else if (v.httpStatus === 404 && now - row.createdAt > 600) { markFailed(row, "not found"); refund(row); }
}
for (const order of db.ordersWhere({ status: "paid", videoId: null, paidBefore: now - 600 })) { failAndRefund(order); }
```

Attach webhooks to your own records by `external_id` (set it on every `from-data` call). For embedded sessions attach by `externalUserId`.
