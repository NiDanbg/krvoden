# Karel Voden — krvoden.com

Statically generated author site (no client-side router, real HTML per page/language).

## Local development

```
pip install -r requirements.txt
python scripts/build.py      # generates dist/
python -m http.server 8040 --directory dist
```

## Editing content

```
python admin_server.py        # http://localhost:8050/admin
```

Edits go straight to `data.js` / `synopsis/` / `books/` / `news/` / `images/`. Use the admin panel's
**Build** tab to regenerate `dist/` for local preview, and **Publish** to push straight to GitHub.

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the site with
`scripts/build.py` and publishes `dist/` via GitHub Pages (Pages source: **GitHub Actions**).
