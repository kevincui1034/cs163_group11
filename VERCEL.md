# Deploy this project on Vercel

This repo’s web UI is a **Dash (Flask) app** under `appengine/`. Vercel runs it as a single Python serverless function via [`api/index.py`](api/index.py), which exposes the Flask WSGI object as `app` (required by Vercel).

## Prerequisites

- A [Vercel](https://vercel.com) account and the [Vercel CLI](https://vercel.com/docs/cli) (`npm i -g vercel`), **or** connect the GitHub repo in the Vercel dashboard.
- For production data from **Google Cloud Storage**: a bucket with `Pokemon.csv` and `gen9ou_full_data.json`, plus a **service account** JSON with read (and write, if you use save helpers) access to that bucket.

## Environment variables

Set these in the Vercel project (**Settings → Environment Variables**):

| Variable | Required | Description |
|----------|----------|-------------|
| `USE_GCS` | Recommended for Vercel | Set to `1` to load data from GCS instead of local files under `appengine/components/data/`. |
| `BUCKET_NAME` | If `USE_GCS=1` | GCS bucket name (e.g. `cs163-group11.appspot.com`). |
| `GCP_SERVICE_ACCOUNT_JSON` | If `USE_GCS=1` on Vercel | Paste the **full JSON** of the service account key (one line or multiline). Used to set up credentials when no `GOOGLE_APPLICATION_CREDENTIALS` file exists. **Treat as a secret.** |
| `GOOGLE_APPLICATION_CREDENTIALS` | Optional | If you mount a key file in the image/build, path to the JSON file; otherwise use `GCP_SERVICE_ACCOUNT_JSON`. |

For **local** development without GCS, omit these or set `USE_GCS=0` and run from `appengine/` with data files present.

## Deploy

From the repository root (where `vercel.json` and `requirements.txt` live):

```bash
vercel
```

Production:

```bash
vercel --prod
```

Or import the repo in the Vercel dashboard; the build will install [`requirements.txt`](requirements.txt), which includes [`appengine/requirements.txt`](appengine/requirements.txt).

## Local check (same entrypoint Vercel uses)

```bash
# From repo root, after: pip install -r requirements.txt
set USE_GCS=0
vercel dev
```

On Windows PowerShell: `$env:USE_GCS='0'` before `vercel dev`.

## Notes

- **`app.yaml` / `gunicorn`**: Used for Google App Engine only; Vercel does not use them.
- **Project root**: In Vercel → Settings → General → **Root Directory**, leave this empty (repo root). If it is set to `appengine`, the build will not see [`api/index.py`](api/index.py) and configuration can fail.
- **Bundle size / cold starts**: `scikit-learn` and related libs are heavy. [`.vercelignore`](.vercelignore) skips uploading `pokemon_analysis/` (not needed for the web app). If you still hit size or timeout limits, trim dependencies or pages.
- **Pokemon recommender page**: The full recommender (`/pokemon_recommender`) is not linked in the navbar in [`appengine/app.py`](appengine/app.py); it depends on large local model files that may not be present in deployment.
