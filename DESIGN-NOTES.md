# Editorial redesign — local review, 9 September 2026

## Scope

- Shared type scale, restrained dark palette, warm accent, consistent spacing.
- Homepage: current-work introduction, three featured projects, six expandable projects, a compact CV timeline, short background, contact.
- Full 17-entry publication archive at `/publications/`.
- Full experience and education retained at `/cv/`, including print styles.
- Responsive navigation, keyboard focus states, skip links and reduced-motion support.
- Prism adapted into `assets/negative-prism.svg`: bone/copper palette, finer static ray paths and faint interface normals. Original symbol-lab asset is unchanged; no raster-generated figures.

## Build and preview

This is the static rewrite, not the legacy Jalpc npm build.

```sh
python3 scripts/build_site.py
python3 -m http.server 8765
```

Edit `content/site.json` for canonical content, `scripts/build_site.py` for templates, and `assets/site.css` for styles. Homepage selections are in the `home` object. Generated pages and a content-hashed CSS URL are rebuilt together.

The previous JSON source lagged behind the generated homepage. The current 17 publications and full experience/education were reconciled into JSON before rebuilding, preserving titles, links and metadata from that page.

## September 24 content update

- Removed the prism caption, preserving the illustration and its mobile visibility rule.
- Replaced the repeated selected-paper list with a compact experience and education timeline based on the pre-redesign CV. Full CV remains at `/cv/`; the homepage CV navigation now targets `#cv`.
- Added project summaries for holographic cloud storage, stochastic path probabilities, and molecular intermediates, using existing publication links. The full 17-entry publication archive is unchanged.
- Preserved `#publications`, `#experience`, and `#education` deep links at their relevant destinations.
- Updated source templates and canonical JSON, then regenerated all three pages. Visual and browser review artifacts are in the sibling `personal-site-cv-review` directory.

## Isolation

Worktree: `/home/node/.openclaw/workspace/work/personal-site-redesign`
Branch: `redesign/editorial-20260909`

The existing uncommitted design edits were copied into this isolated worktree first. The original project working tree remains unchanged, with a pre-edit backup at `/home/node/.openclaw/workspace/work/personal-site-before-20260909.zip`. This branch includes the reconciled content and redesign, not a deployment.

## Verification

- Deterministic Python build and `git diff --check`.
- All internal linked pages and assets exist.
- Chromium at 320, 390, 768 and 1440 pixels for homepage, CV and publications (12 combinations): no horizontal overflow, navigation clipping, missing anchors, broken images or runtime errors; fonts loaded.
- Expandable projects opens and includes all three remaining projects.
- Desktop and mobile homepage screenshots visually inspected.
- CV print PDF generated (not visually audited).
- Browser script, JSON results, screenshots and PDF are in the sibling `personal-site-review` directory, outside the website.

No push or production deployment performed.
