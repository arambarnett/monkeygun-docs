# Media and keys

Where the file lives, which URL to use, and how to make it public.

Files live in a private bucket. There are three ways a request is allowed to read one:

1. **The media key.** Every video has a `mediaKey`. Append `?k=<mediaKey>` to any media path, or use the `url`, `renderUrl`, `thumbnail` and `watchUrl` fields, which already carry it.
2. **`public: true`.** Set it per call on `from-data` or `create_video`, or as a show default. The bare paths then play for anyone.
3. **A signed-in session** on the owning account (the studio and the embedded studio).

Without one of these, a media path answers `401`.

## Which URL to use

| Field | Path | Use it for |
|---|---|---|
| `renderUrl` | `/api/media/videos/{id}/{id}-v{N}.mp4?k=…` | Playback and caching. Immutable per version, served with a long cache lifetime, honours Range requests |
| `url` | `/api/media/videos/{id}/{id}.mp4?k=…` | "Latest cut". Mutable, revalidates. Changes after an edit and re-render |
| `thumbnail` | `/api/media/videos/{id}/{id}-thumb.jpg?k=…` | Poster frame. Add `&t=<seconds>` to get a frame at a moment (generated once, then cached) |
| `watchUrl` | `https://monkeygun.com/w/{id}?k=…` | A hosted share page with Open Graph tags for iMessage, X, Slack, Discord |
| `video` | `/api/videos/{id}/file/{id}.mp4` | Legacy relative path from the render box. No key, no Range support. Avoid |

{% hint style="success" %}
Serve `renderUrl` through your own CDN or edge (tokenslop proxies it under `tokenslop.fun/m/…`) when your viewers are far from the render region. The per-version file never changes, so any cache can keep it for a year.
{% endhint %}

## When is the file readable?

`video.rendered` fires when the render finishes. The bucket copy is usually readable at that moment, but on a busy box it can lag by a few seconds. If you gate a feed on playability, `HEAD` the `renderUrl` and expect `200` or `206` before you show it.

## Downloading and re-hosting

You may download and re-host the MP4. The share page and the `watchUrl` are optional. Nothing in the file references Monkeygun unless you keep the default watermark; set `brand.watermark` to your own text, an empty string to remove it, or `brand.logo` to a library image.
