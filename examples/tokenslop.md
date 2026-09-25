# tokenslop.fun

A live exchange-style feed on Robinhood Chain built entirely on this API: house shows, user-paid promos, an embedded creator studio and branded uploads.

[tokenslop.fun](https://tokenslop.fun) is the reference integration. It runs on one Monkeygun account and one channel with eleven shows. Everything below is how it works in production today.

## The four flows

<details>
<summary>House show episode from a snapshot</summary>

1. A scheduler on tokenslop's side decides an episode should exist (nightly, or a mover).
2. `POST /v1/videos/from-data` with `channelId: "tokenslop"`, `showId` (for example `trenches-report`), `data` (a movers list with `iconUrl` per token), `imageUrl`, `images: "none"` or `"source"`, `cta: "Trade them on tokenslop.fun"`, `external_id: "smr-<unix>"`.
3. Insert a feed row with the returned `videoId`, marked as house content.
4. On `video.rendered`, store `renderUrl` (key stripped, proxied under `tokenslop.fun/m/…`; the show default `public: true` makes that possible). A 30-second reconciler covers missed webhooks.

</details>
<details>
<summary>User-paid promo</summary>

1. The user signs a message with their wallet and picks a tier (Quick Promo, Hero Clip, AI Video, Cinematic, or a show like Roast My Bag).
2. tokenslop debits its own "slop credits" (Monkeygun cost × 1.5) and creates an order.
3. `from-data` in the background with the token's [TokenSnapshot](../schemas/token-snapshot.md), the tier's `showId`, `external_id: <orderId>`, and tier extras (`images: "generate"` for Hero, `aiVideo: { provider: "minimax" }` for AI Video, `aiVideo: { provider: "seedance-pro", withAudio: true }` for Cinematic).
4. The webhook attaches the video to the order by `external_id`; `video.render_failed` refunds. Orders with no video after ten minutes are failed and refunded by a sweep.
5. The paid Smart Money report uses the authored-script pipeline instead of the director: the same payload as the house shows, the order id as `external_id`, the buyer as the creator. It sells for $3.00 on a $2.00 cost (60 credits plus a 5-second clip and a generated bed).

</details>
<details>
<summary>Creator studio</summary>

1. Wallet signs; tokenslop's backend calls `POST /v1/embed/token { externalUserId: <wallet>, origin, channelId: "tokenslop", ttlSeconds: 3600 }`.
2. The page iframes the returned `url`.
3. On the iframe's `video.rendered` postMessage, the page calls a signed claim endpoint that reads `get_video` and inserts the feed row under the wallet.
4. The webhook also inserts any rendered video whose `externalUserId` is a wallet, so attribution never depends on the browser.

</details>
<details>
<summary>Upload and brand pass</summary>

1. `POST /v1/library/upload { url }` with a public mp4 or a social permalink.
2. `POST /v1/tools/brand_footage { assetId, channelId: "tokenslop", cta }` for 5 credits.
3. Feed row with `review = 1` until the creator has three cleared videos; an admin queue clears it.

</details>

## What tokenslop built around the API

| Piece | Why | Docs |
|---|---|---|
| Reconciler every 30 s | Webhooks are one attempt | [Webhooks and polling](../guides/webhooks-and-polling.md) |
| Stuck-order sweep | A create can die mid-flight; refund after 10 minutes | same |
| `public: true` as a show default + HEAD probe before feeding | Feed players need keyless URLs and the bucket copy can lag a few seconds | [Media and keys](../concepts/media-and-keys.md) |
| Explicit `images` on every call | Show defaults add cost after a quote | [Credits and quotes](../concepts/credits-and-quotes.md) |
| Authored scripts for the Nansen shows | Exact stats on screen, real charts, no director timeout | [Authored scripts](../guides/authored-scripts.md) |

## Show defaults in use

Nine of the eleven shows share `images: "auto"`, `cta: "Trade it on tokenslop.fun"` and `public: true`. Roast My Bag adds a music bed and a sound-design note ("record scratch on the first punchline, crowd ooh on the second, airhorn on the last"). Trenches Report adds a locked frame with the show title and a badge.

<figure><img src="https://api.monkeygun.com/api/media/videos/vid-306/vid-306-thumb.jpg" alt="tokenslop feed video"><figcaption><p>tokenslop.fun feed.</p></figcaption></figure>
