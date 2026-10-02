# Windward Recruiting: website

The complete static website for Windward Recruiting, built on Brand Book Edition 02. The finished site is in `dist/`. It needs no framework, database or build step to run.

## Put it live with GitHub Pages
1. Create a new repository on GitHub and upload everything in this folder, including the hidden `.github` folder and `.gitignore`.
2. In the repository, open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Push to the `main` branch (or run the workflow from the **Actions** tab). The site publishes in about a minute.
4. **Custom domain (recommended):** in **Settings → Pages → Custom domain**, enter `windwardrecruiting.com`, then point the domain's DNS to GitHub Pages as GitHub describes there. Tick **Enforce HTTPS** once it is available.

The deploy workflow adjusts every link for the address GitHub gives the site (for example `username.github.io/windward-website/`), and leaves them unchanged on a custom domain. To test that locally: `python3 tools/base_path.py /windward-website`.

## What is included
- **58 pages:** Home, About (team and the Sanford Rose Associates® network), For employers (practice areas, how a search works, search request), For candidates, Jobs (25 roles, each with a full page), Insights (22 articles), Contact (book a 30-minute call first), Search, Privacy, Site map and 404.
- **79 redirects** from old addresses (WordPress pages, `/opportunities/`, `/expertise/`, `/network/`) to the new pages, as HTML pages plus `_redirects` (Netlify) and `.htaccess` (Apache).
- **Design:** Geist for headlines and Switzer for reading text, film-graded photography, smooth scrolling for mouse wheels and fade-in and fade-out on scroll. All fonts and images are self-hosted.
- **Search engines:** `sitemap.xml`, `robots.txt`, structured data (EmploymentAgency, JobPosting, BlogPosting), social share image and favicons.

## Forms (set up before going live)
GitHub Pages cannot receive form submissions by itself.
- Open `dist/assets/app.js` (and `src/app.js`) and set `FORM_ENDPOINT` to a form service URL, for example Formspree or Basin.
- Until then, a submitted form opens the visitor's email app addressed to `FORM_EMAIL`. Uploaded files cannot be attached automatically in that case.

## Booking calendar
The Contact page embeds the Calendly link set as `CAL` in `src/common.py`. If the link changes, update it there and rebuild.

## Updating the site
- **Rebuild everything:** `python3 src/build.py` regenerates all pages in `dist/` from `src/` and `data/`. Commit and push, and the workflow republishes.
- **Jobs:** edit `data/jobs.json`. The current roles are a snapshot from 2 October 2026.
- **Articles:** edit `data/articles.json`.
- **New photos:** `python3 grade.py original.jpg dist/assets/img/name.jpg colour 2400` applies the Windward film grade (use `mono` for black and white).
- **Preview locally:** `python3 -m http.server --directory dist` and open http://localhost:8000.

## Folder map
| Path | What it is |
| --- | --- |
| `dist/` | The live website. This is what gets published. |
| `src/` | Page templates, styles, scripts and the logo and icon generator. |
| `data/` | Jobs and articles content. |
| `grade.py` | The Windward film grade for new photographs. |
| `.github/workflows/pages.yml` | Publishes `dist/` to GitHub Pages on every push. |
