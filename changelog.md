# Changelog

What changed in the API and the engine.

## 2026-09-27 — Card on file and pay-as-you-go
- **Free credits change.** New accounts now get 50 credits, enough to plan and see a price. The daily free credits are off. Saving a card adds 500 credits for the first videos.
- **Save a card, get 500 credits.** Settings → Credits → Add card opens Stripe's hosted page. The first card on an account adds 500 bonus credits.
- **Pay-as-you-go.** With a card on file, a call that runs short charges a $10 pack (or your chosen pack) and continues instead of answering `402`. Capped at $50 per account per day; on/off in Settings → Credits. Applies to API and MCP calls too.
- **New 402 reason.** `payment_failed (card_declined | authentication_required | daily_cap)` when pay-as-you-go could not top up. Nothing is made or charged. See [Errors](errors.md).

## 2026-09-27 — Captions, web copies, voices and languages, publishing
- **Post captions.** Designed videos now come with a `caption`: post text the designer wrote for that video. Its figures come from your data through the same slots as the voiceover, so the model cannot type a number. It is on video responses and on `video.rendered`, and scheduled shows without a money link post it (plus the source link). For a one-off `publish`, pass it as `caption`.
- **Web copies.** Every render also makes a 720p copy of about 2–3 MB with fast start, for feeds and autoplay. It is `webUrl` on videos, jobs and `video.rendered`, which also carries `posterUrl`. Videos rendered before this date have `webUrl: null`.
- **Voices and languages on designed videos.** `voiceId` and `language` work on `from-data` (designed path) and `/videos/token`. 13 languages: English, Spanish, Portuguese (Brazil), French, German, Italian, Turkish, Indonesian, Japanese, Korean, Chinese (Simplified), Hindi, Arabic. See [Voices, languages and captions](guides/voices-languages-captions.md).
- **Calmer narration.** The default pace is slower, and a line that runs long is no longer sped up to fit its scene. The next line starts later instead, and lines that cannot fit are rewritten before recording.
- **Publishing.** `publish` takes `captions`, a map of post text per Buffer service (`instagram`, `tiktok`, `twitter`, `youtube`, `linkedin`, …) that falls back to `caption`. `instagramStory: true` also posts the video as an Instagram Story after a live Reel (`storyPostIds` in the result). Live Buffer posts (`autopost: true`) now go out immediately instead of waiting for a queue slot. See [Publishing](guides/publishing.md).
- **Token videos on any chain.** `POST /v1/videos/token` accepts EVM (`0x…`) and Solana addresses. `chain` is a DexScreener chain id (`base`, `solana`, `ethereum`, `bsc`, `robinhood`, …). `source: "dexscreener"` reads facts from DexScreener, with hourly candles from GeckoTerminal. Robinhood Chain tokens listed on tokenslop still default to tokenslop's data.

## 2026-09-26 — Designed videos, Autopilot
- **Designed videos.** `from-data` with data, a page or a brief is now designed by the model from scratch: layout, motion, charts and voiceover, written as code and recorded frame by frame. Every figure on screen and in the voiceover comes from your data. Pass `engine: "director"` for the template engine. Shows, footage, clips and presenters use the template engine automatically.
- `style` picks one of 11 looks: `trading-terminal`, `tabloid`, `nature-doc`, `hype-trailer`, `arcade`, `breaking-news`, `swiss-poster`, `comic`, `vaporwave`, `luxury-minimal`, `chaos-meme`. Omit it for a varied pick. `mode: "story"` leads with a plot instead of the numbers.
- A designed video costs 480 credits up to 30 seconds, plus 240 per extra 30 seconds.
- `POST /v1/videos/token`: a token address in, a designed, voiced and checked 9:16 short out. It answers `202` with a job, then fires the usual webhooks.
- **Autopilot.** Scheduled shows that are designed, rendered, optionally reviewed by AI, and posted with no human. The routes are under `/v1/autopilot` with your API key: `suggest`, `starters`, `voices`, `start`, `GET /autopilot`, `PATCH /autopilot/{seriesId}`, `pause`, `resume` and episode `approve`. See [Scheduled shows](guides/scheduled-shows.md#autopilot).

## 2026-09-25 — Developer docs, OpenAPI 3.1.0, 500 signup credits
- These docs replace the in-app docs page.
- OpenAPI now includes `/embed/token`, `/library/upload`, `/jobs/{id}`, `/webhooks/{id}/deliveries`, and `Video`, `Job`, `Media`, `WebhookEvent` and `VideoStatus` schemas.
- Internal tools removed from the public catalog.
- New accounts start with 500 credits.

## 2026-09-24 — Authored-script quality
- `scene.chart`: real line and bar charts drawn from your series.
- `scene.asset.url`: a public image or mp4 fetched into the video at create time.
- `scene.sfx`: bundled sound names, `none`, or a library sound per scene.
- `scene.transition`: `wipe`, `cut` or `dissolve` per scene.
- `motion: "slam"` for hero numbers. Count-ups use tabular fixed-width digits (no more reflow).
- Authored scripts keep `stats`, `motion` and `frame` (previously dropped).
- Image-to-video seeds small or off-aspect stills on a full-frame canvas; token logos under 300 px now make clips.
- Keyed absolute media links (`url`, `renderUrl`, `thumbnail`, `watchUrl`, `mediaKey`, `public`) on every video response and on jobs.
- `public: true` per call. `musicAssetId` and `music.generate` per call on `from-data`.

## 2026-09-14 — Plans, proofs, profiles
- `plan` and `proof` tools; the studio shows a plan card for anything over 200 credits.
- Account profile: brand kit, voices, audiences, CTAs remembered between sessions; `learn_brand` from a site.
- Music-video workflow: whole-track runtime, lyric-driven imagery, no narration.
