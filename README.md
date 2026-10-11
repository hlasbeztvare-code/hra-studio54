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
npm run check:responsive
npm run preview:intro
```

The browser check requires the preview server to be running. The check creates `shots/check-intro-*.png` with test fixtures. `npm run preview:intro` creates `shots/intro-1920x1080.png`, `shots/intro-1440x900.png` and a mobile screenshot using the original live leaderboard and statistics read through GET requests. The personal record remains device-local. Preview requests never write to the shared APIs.

The redesign was deployed with user approval on October 10, 2026: https://hra.l-code-dynamics.com. Live checks passed in both desktop sizes; see the design contract for the deployment record. Additional gameplay work remains a separate task.

The responsive intro keeps the complete artwork, START and touch controls near the top on phones. Bubbles, TOP 10 and the original posters follow in a vertically scrollable layout. Tablets and short landscape screens use a two-column layout; the approved desktop composition remains at 1440×900 and 1920×1080. Dialogs remain anchored to the viewport after scrolling. `check:responsive` verifies 15 screen sizes from 320×568 to 1920×1080, horizontal content bounds, long personal records, reachable controls, dialogs, rotation and a short keyboard viewport. All test API writes are intercepted.
