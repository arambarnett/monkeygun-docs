# For exchanges

What an integration looks like, what it takes on your side, and what you get, in one page. For the developer detail, start at the [quickstart](start-here/quickstart.md).

## What your users see

* **A feed of short videos cut from your own data.** Listings, movers, liquidations, whale moves, weekly recaps. Each one is 15 to 30 seconds, vertical, in your brand, with every number traced to the payload you sent, and a trade button one tap away.
* **"Make your own."** A studio inside your app where a user turns their portfolio, a trade, or a token they hold into a clip, with your CTA on the end card. They share it; their followers land on you.
* **Your marketing calendar on autopilot.** Daily and weekly shows that run on a schedule or on a trigger, delivered to your feed, your socials, or both.

This is running today at [tokenslop.fun](https://tokenslop.fun) on Robinhood Chain: house shows, user-paid promos, an embedded creator studio, and branded uploads, all on the same API you would use. Samples: [six rendered examples](examples/monkeygun-examples.md).

## What it takes on your side

| Piece | What you provide | Effort |
|---|---|---|
| Data | A JSON snapshot per event: token, pool, wallet or flow. [Schemas here](schemas/overview.md). Any feed you already have works | One endpoint or a cron job |
| Brand | Colors, fonts, logo, watermark, disclaimer text, CTA. Locked once on your channel | An afternoon |
| Trigger | Your system calls `POST /v1/videos/from-data` when something happens, or we run a schedule | A few lines |
| Playback | A webhook receives the finished file's URL; you show it in your feed or post it | Half a day |
| Creator studio (optional) | A backend route that mints a session token and an iframe on your page | One day |

A first listing video is under an hour of engineering. A feed with user creation is a one-to-two-week integration. There is no SDK to install; it is a REST API with public docs, an OpenAPI spec, and [runnable examples](examples/monkeygun-examples.md).

## What we need from you to start

1. Which data, and where it lives (an API, a warehouse export, or public on-chain data we pull ourselves).
2. Brand assets and any compliance language your legal team requires on screen.
3. The surface: a tab in your app, a web page, your social accounts, or all three.
4. Twenty to fifty assets to start with, and two show formats to run daily.

## How a pilot works

Four to six weeks, fixed fee. We stand up your channel, two data shows and the creator studio on your data, run it daily, and score it: exposed users against a comparison group on sessions, retention, shares, creation rate and trading activity. You get the readout and the videos; if the numbers hold, it continues on a platform fee plus usage. Pricing and packages are on the [packages page](packages.md).

## Compliance

Every figure on screen comes from the payload; the renderer draws the numerals itself, so a number that is not in your data cannot appear. Disclaimers and as-of timestamps are locked on the channel and appear on every episode. User uploads can be held for review before they reach a feed. Details in [Brand and style packs](concepts/brand-and-packs.md) and [Upload and brand pass](guides/upload-and-brand-pass.md).

## Talk to us

Aram Barnett, co-founder: [aram.barnett@gmail.com](mailto:aram.barnett@gmail.com). Send the data you have and the surface you want the videos on, and we will send back a sample cut from it within a day.
