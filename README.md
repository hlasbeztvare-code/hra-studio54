# Studio 54 — Přežij after

Existing game with a layered comic intro. See [STUDIO54_DESIGN_LOCK.md](STUDIO54_DESIGN_LOCK.md) for the visual and copy constraints.

Requires Node.js and npm. For browser checks, install Google Chrome.

```sh
npm ci
npm run dev
```

Preview: http://localhost:5454. The development server rebuilds on each page load and serves artwork/posters from `deploy/`. A clean checkout can build without a pre-existing ignored `dist/` directory.

```sh
npm run build
npm run check:intro
npm run preview:intro
```

The browser check requires the preview server to be running. The check creates `shots/check-intro-*.png` with test fixtures. `npm run preview:intro` creates `shots/intro-1920x1080.png`, `shots/intro-1440x900.png` and a mobile screenshot using the original live leaderboard and statistics read through GET requests. The personal record remains device-local. Preview requests never write to the shared APIs.

The redesign awaits visual approval; deployment and additional gameplay work are separate steps.
