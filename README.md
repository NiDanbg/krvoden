# Karel Voden — krvoden.com

Statically generated author site (no client-side router, real HTML per page/language).

## Local development

```
pip install -r requirements.txt
python scripts/build.py      # generates dist/
python -m http.server 8040 --directory dist
```

## Editing content

Content is edited with a local admin panel that is kept only on the author's computer, outside this repository.

## Deployment

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the site with
`scripts/build.py` and publishes `dist/` via GitHub Pages (Pages source: **GitHub Actions**).
