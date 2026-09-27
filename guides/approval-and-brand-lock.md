# Approval and brand lock

For agencies, campaigns and regulated businesses: every episode of a show carries the same identity and legal line, nothing a banned word slips through, and named people sign off before anything goes out.

A show has two settings for this:

- **Brand lock**: logo, colors, fonts, a required disclaimer, a required end-card CTA and banned words. The render enforces it.
- **Approvers**: email addresses. Each new episode is emailed to them with a private approval link. They don't need a Monkeygun account.

Set both in **Show → Settings → Brand & approval**, in the Autopilot **Channels** step, or with the API (below).

## Brand lock

| Field | What the render does |
|---|---|
| `disclaimer` | Burned into every frame of every episode as a strip along the bottom edge, for the full runtime. Up to 600 characters. |
| `cta` | Must be on the end card. If the episode doesn't already show it, an end card with the CTA is burned into the last seconds. |
| `bannedWords` | Words or phrases that may never appear in the title, narration, scene text, on-screen data, captions or the post caption. |
| `logo`, `accent`, `ground`, `ink`, `displayFont`, `bodyFont` | Your logo, colors and fonts. They override the video's own brand on scripted episodes and are handed to the designer on authored ones. |

### The disclaimer can't be removed

The locked text comes from the show every time an episode renders. It never comes from the video, so later edits can't change it. That covers `update_video`, a Studio edit, a revision or a chat instruction.

After the strip is burned in, a check runs. The render fails if any of these is true:

- the strip is missing
- the strip's text doesn't match the locked text exactly
- the strip doesn't start at 0s or doesn't cover the whole runtime
- the strip isn't inside the composition
- the strip lost its locked styling
- a script, style or scene in the composition refers to the strip, which could hide or move it

Chat can set a lock but can't loosen one. It can't change or remove a locked disclaimer, drop banned words, change approvers, or turn off "approval required". Only a person with edit rights can do those, in the show settings or with the REST call below.

### Banned words

Matching is by whole word or phrase, is case-insensitive and works in any language. `cure` doesn't match "secure", and `risk free` matches "Risk  free". The words are also given to the writer so scripts avoid them in the first place.

If one gets through anyway, the render stops before it starts, with a message like this:

```
Banned word "guaranteed" found — the show's brand lock does not allow it. voiceover: "Returns are guaranteed…". Edit the script (or ask chat to rewrite those lines) and render again.
```

Your own locked disclaimer and CTA never count against your banned words.

## Approvers

1. An episode renders, and the show's policy holds it: `hold`, `approval`, or `review` when the AI reviewer holds it.
2. Every approver gets an email from notify@monkeygun.com. It links to `https://monkeygun.com/w/{videoId}/approve?t=…`.
3. The page plays the video and shows the post caption. It has two buttons: **Approve** and **Request changes**, which takes a note.
4. What happens next depends on the button:
   - **Approve**: the episode publishes to its series' destinations (your Buffer channels, YouTube through Buffer, a share link). If the episode has no series destination, it's marked approved and ready to download.
   - **Request changes**: the note is filed on the episode and the owner is notified and emailed. In chat, `get_video` shows the note as `approverChangeRequests`, and the episode card has a **Revise with the note** button. When the revised cut renders, it goes back to the approvers automatically, with new links.
5. The app shows who approved, when, and every note. You'll see it on the episode card ("Awaiting approval by …", "Approved by … at …") and under **Approval history**.

### Policies

| `policy` | What happens to a finished episode |
|---|---|
| `hold` | Held. The owner can approve in the app. Approvers, if any, are emailed. |
| `approval` | Held until a named approver approves. The owner can't approve around them unless the owner is on the list. Nothing posts to Buffer or YouTube before that, and this overrides a series' own policy. Requires at least one approver. |
| `review` | An AI reviewer checks the episode, then posts it. If the reviewer holds it, the approvers are emailed. |
| `digest`, `autopost` | Approvers aren't involved. |

### The approval link

- The link is signed with HMAC-SHA256 using `APPROVAL_SIGNING_SECRET`. The signature covers the video, the approver's email, the approval round and the expiry, so a link can't be guessed or altered.
- It's valid for one episode and one approver, and expires after **7 days**.
- A link acts only on the cut it was sent for. If the episode is re-rendered or sent again, older links stop working with a clear message.
- Once someone decides, later clicks on the same round just show who decided.

## API

Set the lock, approvers and policy on a show. Chat's `update_show` can't set approvers, so use this call:

```bash
curl -X PATCH https://api.monkeygun.com/api/channels/$CHANNEL/shows/$SHOW \
  -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{
    "brandLock": {
      "disclaimer": "Paid for by Friends of Jane Doe.",
      "cta": "Vote Nov 3 — janedoe.org",
      "bannedWords": ["guaranteed", "risk free"],
      "accent": "#1f4fd8", "ground": "#0b1020", "ink": "#ffffff"
    },
    "approvers": ["counsel@janedoe.org", "cm@janedoe.org"],
    "policy": "approval"
  }'
```

Autopilot takes the same fields when you start a show:

```bash
curl -X POST https://api.monkeygun.com/v1/autopilot/start -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{ "source": {…}, "show": {…}, "policy": "approval",
        "brandLock": { "disclaimer": "Not financial advice." },
        "approvers": ["compliance@yourfirm.com"] }'
```

| Route | Who can call it | What it does |
|---|---|---|
| `POST /api/approvals/{videoId}/request` | Owner or editor | Sends the current cut to every approver, or sends it again. This opens a new round, so older links stop working. |
| `GET /api/approvals/{videoId}` | Anyone who can see the video | Returns the approval state, the audit trail (`approval.log`), change requests and the show's rule. |
| `GET /w/{videoId}/approve?t=…` | Public (the token is the credential) | The approver's page. |
| `POST /api/approvals/decide` | Public (the token is the credential) | Records the decision. Body: `{ "t": "…", "action": "approve" \| "changes", "note": "…" }` |

## Configuration

| Env var | Purpose |
|---|---|
| `APPROVAL_SIGNING_SECRET` | Signs approval links. **Required in production**: without it, no approval email is sent and the error is logged. Use a long random value, for example `openssl rand -hex 32`. Rotating it invalidates every open approval link. In local development, a fixed development secret is used when it's unset. |
| `RESEND_API_KEY` | Already used for the digest. Approval emails go out through the same Resend account. Without it in local development, the approval link is printed to the API log instead. |
| `WEB_URL` | The base URL used in approval links. Default: `https://monkeygun.com`. |
