# Runnable examples

Six complete integrations as dependency-free Node scripts, each run against production. Clone, add your key, run one.

Repository: [github.com/arambarnett/monkeygun-examples](https://github.com/arambarnett/monkeygun-examples)

```bash
git clone https://github.com/arambarnett/monkeygun-examples && cd monkeygun-examples
cp .env.example .env      # your key from Monkeygun → Settings → Developer
set -a && source .env && set +a
node examples/01-exchange-listing.mjs
```

Every script prints the keyed `renderUrl` (plays without a session), a share page and a poster. The client is 40 lines: `api()` for REST calls, `tool()` for the catalog, `waitForVideo()` and `waitForJob()` for polling. Replace polling with a [webhook](../guides/webhooks-and-polling.md) in production.

## 01 · Exchange listing

A token just listed. Post its [TokenSnapshot](../schemas/token-snapshot.md) with the logo and your CTA; one call, then poll or listen for `video.rendered`. Pass the listing id as `external_id` so the webhook maps back to your record.

[![Bitcoin is live](https://api.monkeygun.com/api/media/videos/vid-422/vid-422-thumb.jpg?k=5eed15a54d475d0eb30e)](https://monkeygun.com/w/vid-422?k=5eed15a54d475d0eb30e)

[Watch the sample](https://monkeygun.com/w/vid-422?k=5eed15a54d475d0eb30e) · [source](https://github.com/arambarnett/monkeygun-examples/blob/main/examples/01-exchange-listing.mjs) · 60 credits

## 02 · Yield protocol: Rate Split

A [PoolSnapshot](../schemas/pool-snapshot.md) with an authored script: the words are exact, a real bar chart shows the APY split between borrowers and rewards, the disclaimer carries the as-of date, and `async: true` returns a job to poll. No director, no invented copy.

[![Rate split](https://api.monkeygun.com/api/media/videos/vid-421/vid-421-thumb.jpg?k=44d584944fda17b69a38)](https://monkeygun.com/w/vid-421?k=44d584944fda17b69a38)

[Watch the sample](https://monkeygun.com/w/vid-421?k=44d584944fda17b69a38) · [source](https://github.com/arambarnett/monkeygun-examples/blob/main/examples/02-yield-rate-split.mjs) · 60 credits

## 03 · Portfolio recap and the embedded studio

Two things an exchange does for its users. First, "your week" from a [WalletSnapshot](../schemas/wallet-snapshot.md), made server-side and tagged to the user. Then an embed token so the same user opens the studio inside your app and makes their own; rendered-video webhooks carry `externalUserId` so attribution never depends on the browser.

[![Your week](https://api.monkeygun.com/api/media/videos/vid-423/vid-423-thumb.jpg?k=d69a6e2083d2f8de2f79)](https://monkeygun.com/w/vid-423?k=d69a6e2083d2f8de2f79)

[Watch the sample](https://monkeygun.com/w/vid-423?k=d69a6e2083d2f8de2f79) · [source](https://github.com/arambarnett/monkeygun-examples/blob/main/examples/03-portfolio-recap.mjs) · 60 credits

## 04 · Your existing footage, indexed and cut

Upload what you already have by URL (a file, or a post on X, YouTube, TikTok or Instagram), index it once so the engine knows every scene and every spoken line, scan it for highlights if it has no speech, then cut a video from it with `images: "library"`. A campaign is one indexing plus one call per angle.

[![Cut from your own footage](https://api.monkeygun.com/api/media/videos/vid-425/vid-425-thumb.jpg?k=815e407ba99a2ad20c58)](https://monkeygun.com/w/vid-425?k=815e407ba99a2ad20c58)

[Watch the sample](https://monkeygun.com/w/vid-425?k=815e407ba99a2ad20c58) · [source](https://github.com/arambarnett/monkeygun-examples/blob/main/examples/04-footage-campaign.mjs) · 20 credits per minute to index, 5 per minute for highlights, then the video

## 05 · Weekly stocks brief

No data of your own: the built-in `market_data` feed reads Yahoo Finance for tickers and indices (CoinGecko for coins, Frankfurter for FX, Open-Meteo for weather) and returns a source pack. The script may only use the pack's facts.

[![AMD up 23% in a week](https://api.monkeygun.com/api/media/videos/vid-424/vid-424-thumb.jpg?k=e203ca6d3e163cf1fb64)](https://monkeygun.com/w/vid-424?k=e203ca6d3e163cf1fb64)

[Watch the sample](https://monkeygun.com/w/vid-424?k=e203ca6d3e163cf1fb64) · [source](https://github.com/arambarnett/monkeygun-examples/blob/main/examples/05-stocks-weekly.mjs) · 60 credits, images generated add 25 each

## 06 · URL to video

Any page in, a video out that can only say what the page says. The sample reads the Wikipedia page for Ken Sugimori, the artist who designed the original Pokémon, and cuts a collector's portrait from its facts and images.

[![Ken Sugimori](https://api.monkeygun.com/api/media/videos/vid-426/vid-426-thumb.jpg?k=3d45860c08fe23ce4566)](https://monkeygun.com/w/vid-426?k=3d45860c08fe23ce4566)

[Watch the sample](https://monkeygun.com/w/vid-426?k=3d45860c08fe23ce4566) · [source](https://github.com/arambarnett/monkeygun-examples/blob/main/examples/06-url-to-video.mjs) · 60 credits

## Live integrations

* [tokenslop.fun](tokenslop.md), an exchange-style feed built entirely on this API.
* [nansen-shows](nansen-shows.md), seven authored shows from Nansen smart-money data.
