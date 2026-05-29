# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> This file is intentionally high-level. Implementation details, conventions, and the project todo list live in `README.md`.

## Philosophy

**Minimalism.** Every addition to this template must justify its existence. Prefer fewer files, fewer abstractions, fewer moving parts. When in doubt, leave it out. A wiki that's simple to understand and fork beats one that's feature-complete but heavy.

**Anyone can run it.** Setup must require nothing beyond a terminal, Python, and a browser. No Docker, no build tools, no developer background. If a non-technical person would give up at a setup step, that step shouldn't exist.

## What this is

wiki-ai is a template for an AI-powered single-project research wiki. Each repo instance is one research project (e.g. "designing a game"). Claude Code is the primary interface — users invoke skills to research and navigate interlinked Markdown notes. A stdlib Python web server with a D3.js graph view lets anyone browse the wiki with `python scripts/main.py` — no install step, no dependencies.

Users start a new wiki with a single command — no forking:
```sh
curl -fsSL https://raw.githubusercontent.com/dennisdms/wiki-ai/main/scripts/init.sh | sh -s -- "my-project"
```

## Folder structure

```
_index.md          # Project home (auto-maintained)
sources/
  bibliography.md  # All external URLs — notes link here, never inline raw URLs
  assets/          # User-pasted source materials (PDFs, images, etc.)
notes/             # Research notes, recursively organized with _index.md per folder
reports/           # Generated reports — never hand-edited
.claude/
  skills/          # research, index
scripts/           # stdlib Python server, static/, templates/
```

## Branching strategy

This repo serves two distinct purposes depending on the active branch. Read the branch name before doing any work — the mode changes what you are responsible for.

### `main` — template development

On `main` you are **building wiki-ai itself**: the skills, the init script, the web server, and the docs. Work here is software development. The `.md` files (CLAUDE.md, README.md, stub indexes) are part of the template, not a live wiki. Do not add research notes or bibliography entries on this branch.

### `wiki_*` — live wiki instances

Any branch named `wiki_<topic>` (e.g. `wiki_front-end-for-wiki-ai`, `wiki_game-design`) is a **full wiki in use**, as if a real user had run the init script and started researching. These branches exist in this repo for development convenience — they let you dog-food the tool — but the AI's role on them is identical to what a real user's AI would do: research, write notes, maintain indexes, and follow all wiki skills. Treat the template code on these branches as read-only background infrastructure.

**On a `wiki_*` branch:**
- All wiki skills apply in full (`research`, `index`).
- The AI file scope rule applies: only `.md` files are touched.
- Do not edit `scripts/`, `CLAUDE.md`, or any other template infrastructure — changes to the template belong on `main`.
- The wiki content (notes, reports, bibliography) on these branches is real research, not placeholder scaffolding.

## AI file scope

**Claude Code may only read and write `.md` files anywhere in the wiki.** All other files — Python scripts, HTML templates, CSS, JavaScript, Dockerfiles, YAML configs, shell scripts, `.gitkeep`, binaries, assets — are off-limits. Do not create, edit, move, rename, or delete them under any circumstances.

Claude Code has full responsibility for every `.md` file in the wiki: notes, indexes, reports, bibliography, and this file. Non-markdown files are managed by the user or by external tooling.

The one exception is `sources/assets/` — even the `.md` files there (if any) are user-managed. Do not touch anything inside `sources/assets/`.

## Key invariants

- `[[wiki-links]]` connect notes to each other and to `sources/bibliography.md` entries.
- `_index.md` files are recursive: every directory has one, maintained by the `index` skill.
- `sources/bibliography.md` is the only place raw URLs live.
- `sources/assets/` is user-managed — AI never touches it.
- All Python (server) lives in `scripts/` — AI never touches these files.

## Skills

| Skill | Purpose |
|---|---|
| `research` | Research a topic, save a note, update bibliography and parent `_index.md` |
| `index` | Create or regenerate `_index.md` for a directory |
