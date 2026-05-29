# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> This file is intentionally high-level. Implementation details, conventions, and the project todo list live in `README.md`.

## Philosophy

**Minimalism.** Every addition to this template must justify its existence. Prefer fewer files, fewer abstractions, fewer moving parts. When in doubt, leave it out. A wiki that's simple to understand and fork beats one that's feature-complete but heavy.

**Anyone can run it.** Setup must require nothing beyond a terminal, Python, and a browser. No Docker, no build tools, no developer background. If a non-technical person would give up at a setup step, that step shouldn't exist.

## What this is

wiki-ai is a template for an AI-powered single-project research wiki. Each repo instance is one research project (e.g. "designing a game"). Claude Code is the primary interface — users invoke skills to research and navigate interlinked Markdown pages. A stdlib Python web server with a D3.js graph view lets anyone browse the wiki with `python3 scripts/server/main.py` — no install step, no dependencies. The browser UI is rooted at `wiki/`.

Users start a new wiki with a single command — no forking:
```sh
curl -fsSL https://raw.githubusercontent.com/dennisdms/wiki-ai/main/scripts/init.sh | sh -s -- "my-project"
```

## Folder structure

```
wiki/
  _index.md        # Wiki home served at /
  sources/
    bibliography.md  # All external URLs — pages link here, never inline raw URLs
    assets/          # Source materials (PDFs, images, etc.)
  pages/             # Research pages, recursively organized with _index.md per folder
  reports/           # Generated reports
.claude/
  skills/
    <skill>/
      SKILL.md       # research-topic, manage-sources, create-index, choose-page-location, create-page, update-backlinks, manage-tags, create-skill
scripts/
  init.sh            # Project bootstrap script
  server/            # stdlib Python server, static/, templates/
```

## Branching strategy

This repo serves two distinct purposes depending on the active branch. Read the branch name before doing any work — the mode changes what you are responsible for.

### `main` — template development

On `main` you are **building wiki-ai itself**: the skills, the init script, the web server, and the docs. Work here is software development. The `.md` files in the repo root plus the stub wiki files under `wiki/` are part of the template, not a live wiki. Do not add research pages or bibliography entries on this branch.

### `wiki_*` — live wiki instances

Any branch named `wiki_<topic>` (e.g. `wiki_front-end-for-wiki-ai`, `wiki_game-design`) is a **full wiki in use**, as if a real user had run the init script and started researching. These branches exist in this repo for development convenience — they let you dog-food the tool — but the AI's role on them is identical to what a real user's AI would do: research, write pages, maintain indexes, and follow all wiki skills.

**On a `wiki_*` branch:**
- All wiki skills apply in full (`research-topic`, `create-index`).
- The wiki content under `wiki/` (`pages`, `reports`, `sources`) is real research, not placeholder scaffolding.

## Key invariants

- `[[wiki-links]]` connect pages to each other and to `wiki/sources/bibliography.md` entries.
- `_index.md` files are recursive: every directory in `wiki/` has one to document that folder's structure, maintained by the `create-index` skill.
- `wiki/sources/bibliography.md` is the only place raw URLs live.
- `scripts/server/main.py` serves `wiki/` as the site root.

## Skills

| Skill | Purpose |
|---|---|
| `research-topic` | Research a topic, save a page, update sources, and refresh the relevant folder indexes |
| `manage-sources` | Maintain `wiki/sources/bibliography.md` for external URLs and source metadata |
| `create-index` | Document a directory's structure in `_index.md` |
| `choose-page-location` | Choose where new pages belong inside `wiki/pages/` |
| `create-page` | Create a blank page with the required frontmatter and backlinks stub |
| `update-backlinks` | Rebuild the `## Backlinks` section for pages |
| `manage-tags` | Keep page tags consistent across the wiki |
| `create-skill` | Create or refine Claude Code skills with clear scope, naming, and discovery guidance |
