# Connect your data

Paste a link to data you already have and get a show that runs on its own. We read the source once and show you what we found: the first rows, the latest items and the key numbers. Then we suggest shows for it. After you start one, the series re-reads the source on its schedule and makes an episode **only when the data changed**. A quiet check costs 1 credit and makes nothing.

In the app: **Autopilot → Connect your data**, pick the source type, paste the link, check the preview, then click **Suggest shows**.

## Source types

### Google Sheets

1. In the sheet, click **Share**. Under **General access**, choose **Anyone with the link**, role **Viewer**.
2. Open the tab you want and copy the URL from the address bar. It looks like `https://docs.google.com/spreadsheets/d/<id>/edit#gid=<gid>`.
3. Paste it. We read the tab as CSV from `https://docs.google.com/spreadsheets/d/<id>/export?format=csv&gid=<gid>`. A link without `gid` reads the first tab. "Publish to web" links (`/d/e/…/pubhtml`) work too.

Put the column names in the first row and the data below them. If the newest rows are at the bottom, as in a log, we detect that and use the last rows. You can switch this under **Newest rows are at**. Every row is checked for changes, so a new row at the bottom starts a new episode.

**"That sheet is not public yet"** means Google sent its sign-in page instead of the data. Repeat step 1, then click **check again**.

### CSV link

Paste any public URL that downloads a `.csv` file, with column names in the first line. If the link opens a web page instead of downloading a file, use the file's direct download link or pick **Web page**.

### JSON API

1. Paste a `GET` endpoint that returns JSON. We find the list of rows in the response and the fields in each row.
2. If the API needs a key, fill in **API key header**, for example `X-API-Key` with your key, or `Authorization` with `Bearer sk_…`.

The key is stored on our server with the show and sent only to that API. It is never sent back to your browser and never written to our logs. It is not forwarded if the API redirects to a different host. Put keys in the header, not in the URL. A key in a URL is masked when we display it, but it is still part of the link we call.

### RSS or Atom feed

Paste the feed link. It usually ends in `/feed`, `/rss`, `.xml` or `.atom`. An episode is made when new items appear.

### Web page

Paste any public page, such as prices, a leaderboard or listings. Each run we read the page's title, figures and main text, and make an episode when they change. Pages that need a login or build their content with JavaScript may not read. Use the page's feed or API instead if it has one.

### Dune

1. On Dune, open your query and copy its URL, for example `https://dune.com/queries/1234567`. The query id on its own also works.
2. Create an API key: **dune.com → Settings → API → Create new API key**.
3. Pick **Dune query**, then paste the link and the key.

We read the query's latest saved result from `https://api.dune.com/api/v1/query/<id>/results?limit=100` with your key in the `X-Dune-API-Key` header. We don't execute the query. To keep the show fresh, schedule the query on Dune; each new result counts as new data. Reads use your Dune plan's API credits. The key follows the same rules as a JSON API key.

## The API

The same flow works with an API key under `/v1`:

```bash
# 1. Preview: read the source once, get a sourceId (the key stays on our server)
curl -X POST https://api.monkeygun.com/v1/sources/preview -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{ "kind": "dune", "url": "https://dune.com/queries/1234567", "apiKey": "'"$DUNE_API_KEY"'" }'
# → { "sourceId": "src_…", "preview": { "title", "fields", "sample", "rowCount", "stats", "keySaved": true, … } }

# 2. Show ideas for it
curl -X POST https://api.monkeygun.com/v1/autopilot/suggest -H "Authorization: Bearer $MK_KEY" -H "Content-Type: application/json" \
  -d '{ "sourceId": "src_…" }'

# 3. Start: the same body as in Scheduled shows, with "source": { "sourceId": "src_…" }
```

| Field | Values |
|---|---|
| `kind` | `sheets`, `csv`, `json`, `rss`, `page`, `dune` or `pricecharting` |
| `url` | The link. For `dune`, a query URL or id |
| `header` | `json` only, optional: `{ "name": "X-API-Key", "value": "…" }` |
| `apiKey` | `dune` only: your Dune API key |
| `take` | `sheets` and `csv`, optional: `first` or `last` for where the newest rows are. Detected when left out |

A `sourceId` belongs to your account and expires after two hours. `start` uses it up. A source we can't read answers `422` with `error`, a `code` (`sheet_not_public`, `unauthorized`, `not_found`, `blocked`, `no_rows`, …) and often a `fix`. Links to private or internal network addresses are refused (`blocked`). Each preview reads at most 5 MB within 20 seconds.
