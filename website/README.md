# website · the team website (optional)

Two pages, published with GitHub Pages and rebuilt automatically on every change to `main`:

| Page | Built from | Edit this to change it |
|---|---|---|
| **Flowchart** (`index.html`) | [`flowchart.yaml`](flowchart.yaml) | `flowchart.yaml` (boxes, text, order, support subsystems) |
| **Variables & budget** (`variables.html`) | `params/variables.yaml` + `hs3gpr/budget.py` | `params/variables.yaml` |

The geometry picture and the SNR panels on the flowchart page are static HTML in `index.html`.

## Turn it on (once, about 2 minutes)

1. **Settings → Pages → Build and deployment → Source:** choose **GitHub Actions**.
2. **Settings → Secrets and variables → Actions → Variables tab → New repository variable:**
   name `PAGES_ENABLED`, value `true`.
3. **Actions → Website → Run workflow.** When it finishes, the site's address appears in the run summary
   (usually `https://<owner>.github.io/<repo>/`). Paste it into the repo's **About** box (gear icon → Website).

Notes:
- GitHub Pages is free for public repositories. For a private repository you need GitHub Pro, Team or
  Enterprise (students can get Pro through the GitHub Student Developer Pack). The site itself is public
  either way, so don't put anything confidential in it.
- Until you do step 2, the *Website* workflow skips itself, so you won't see failed runs.

## Change the flowchart

Open [`flowchart.yaml`](flowchart.yaml) on GitHub → pencil icon → edit text → commit. The site updates in
about a minute. The comments at the top of the file explain every field. Steps renumber themselves when
you add or remove one; step numbers you typed inside sentences ("step 19") do not.

If the file has a mistake (a typo in `kind`, a `uses` name that doesn't exist), the **Checks** workflow fails
on the pull request and says which line.

## Preview on your computer

```bash
python tools/build_site.py
python -m http.server -d _site 8000     # open http://localhost:8000
```
(Opening `index.html` directly from disk won't work; browsers block loading the data files that way.)
