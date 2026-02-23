# LondonPlumberAI

Landing page for LondonPlumberAI – AI receptionist for plumbers in London.

Single-page HTML/CSS/JS (no frameworks). Includes hero, ROI calculator, how-it-works, pricing, and contact form. Dark professional theme, mobile responsive.

## Push to GitHub

If the repo is not yet on GitHub:

1. Create a new repository on [GitHub](https://github.com/new) (e.g. `london-plumber-ai`). Do not add a README or .gitignore.
2. In this folder run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/london-plumber-ai.git
git push -u origin main
```

Or with GitHub CLI: `gh repo create london-plumber-ai --source=. --push`.

## Deploy

- **Vercel:** Import this repo at [vercel.com](https://vercel.com). Framework: Other. Publish as static files.
- **Netlify:** Import at [netlify.com](https://netlify.com). Build command: leave empty. Publish directory: `.`. Contact form uses Netlify Forms (add `data-netlify="true"` form); submissions appear in Netlify dashboard.

Deployed at: _[Add your Vercel or Netlify URL after deployment]_

## Local

Open `index.html` in a browser or run a static server, e.g. `npx serve .`
