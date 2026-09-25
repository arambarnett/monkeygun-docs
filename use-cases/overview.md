# Use cases beyond data

The same API cuts from a URL, a PDF, a folder of footage, a stock ticker or a weather forecast. Here is what to send for each, and what you need set up.

Financial and on-chain data is where the show kits are, but the engine is source-agnostic. Every video starts from a **source pack**: verbatim facts, stills, footage and brand pulled from whatever you gave it. What changes per use case is only the first call.

| You have | First call | Then | Guide |
|---|---|---|---|
| A JSON snapshot | `from-data` with `data` | done | [Data to video](../guides/data-to-video.md) |
| A web page or PDF | `POST /v1/sources { url }` or `from-data { sourceUrl }` | create, render | [URL to video](../use-cases/url-to-video.md) |
| Footage, photos, audio | `POST /v1/library/upload`, `index_footage` | create with `libraryAssetIds` | [Footage to video](../use-cases/footage-to-video.md) |
| A ticker, a city, a currency pair | `market_data` | create with the returned `sourcePackId` | [Other data feeds](../use-cases/other-data.md) |
| Pasted notes or a script | `POST /v1/sources { text }` or `from-data { script }` | create, render | [Authored scripts](../guides/authored-scripts.md) |
| A Google Drive folder | `import_drive` | as footage | [Footage to video](../use-cases/footage-to-video.md) |

## What you need set up, by use case

<details>
<summary>Any use case</summary>

An API key, a webhook endpoint or a poller, and a place to store `renderUrl`. That is the whole integration for one-off videos.

</details>
<details>
<summary>Running shows</summary>

A channel and at least one show with defaults and a brand lock. Either your own scheduler calling `from-data`, or a series that listens. See [Channels, shows and kits](../concepts/channels-shows-kits.md).

</details>
<details>
<summary>Your users making videos</summary>

A backend route that mints embed tokens, a page that iframes the studio, and a webhook handler that attributes by `externalUserId`. See [Embedded studio](../guides/embedded-studio.md).

</details>
<details>
<summary>Footage</summary>

Storage on your side is optional; upload by URL and Monkeygun keeps the file in your library. Budget 20 credits per minute of footage for indexing, once.

</details>
<details>
<summary>Publishing</summary>

Nothing, if you host the file. Connect Buffer in Settings → Publishing to autopost, or use `publish` with `destination: "share-link"` for a hosted page.

</details>
