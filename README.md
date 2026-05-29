# wiki-ai

An AI-powered research wiki template. One repo = one project. Claude Code does the research; a Python web UI lets you browse and explore the link graph.

```sh
curl -fsSL https://raw.githubusercontent.com/dennisdms/wiki-ai/main/scripts/init.sh | sh -s -- "my-project"
```

---

## Project Plan

### 1. Repo scaffold

- [ ] Create folder structure: `content/`, `sources/assets/`, `reports/`, `.claude/skills/`, `.claude/agents/`, `scripts/static/`, `scripts/templates/`
- [ ] Root `_index.md` stub (title from project name, empty topic list)
- [ ] `content/_index.md` stub
- [ ] `reports/_index.md` stub
- [ ] `sources/bibliography.md` with entry-format comment block at top
- [ ] `.claude/settings.json` with default skill permissions

---

### 2. Skills (`.claude/skills/`)

#### `research`
- [ ] Accept a topic as input
- [ ] Search `content/` for an existing note on the topic before creating a new one
- [ ] Create or update a note under `content/` with correct frontmatter (`title`, `tags`, `created`, `updated`)
- [ ] Append new external sources to `sources/bibliography.md` (deduplicate by URL)
- [ ] After saving, scan related notes and insert `[[new-note]]` links where relevant
- [ ] Add `## Backlinks` section to the new note listing all notes that link to it
- [ ] Update the parent `_index.md` to include the new note
- [ ] If a topic is broad, create a subdirectory with its own `_index.md` and split into focused notes

#### `report`
- [ ] Accept a topic or question as input
- [ ] Read all relevant notes from `content/` and entries from `sources/bibliography.md`
- [ ] Write a synthesized report to `reports/<slug>.md` with frontmatter
- [ ] Include a `## Sources` section listing every note, bibliography entry, and asset used
- [ ] Update `reports/_index.md` to include the new report
- [ ] Regenerate, never patch existing reports

#### `lint`
- [ ] Find broken `[[links]]` — no matching `.md` file or `bibliography#slug` anchor
- [ ] Find notes missing `## Backlinks` section
- [ ] Find notes with missing or malformed frontmatter (`title`, `created`, `updated`)
- [ ] Find duplicate URLs in `sources/bibliography.md`
- [ ] Find `[[assets/x]]` links pointing to files that don't exist in `sources/assets/`
- [ ] Find directories missing an `_index.md`
- [ ] Output a grouped error report; exit non-zero if any errors found

#### `cleanup`
- [ ] Run lint and collect all issues
- [ ] Show a diff of every proposed change and ask for confirmation before writing
- [ ] Regenerate `_index.md` link-list sections (preserve hand-written narrative at top)
- [ ] Add missing `## Backlinks` sections to notes
- [ ] Set missing `updated` dates to today
- [ ] Normalize filenames to lowercase kebab-case (update all links that referenced the old name)
- [ ] Remove duplicate bibliography entries (keep first occurrence)

---

### 3. Init script (`scripts/init.sh`)

- [ ] Require project name as first positional argument; error if missing
- [ ] Accept optional `--remote <url>` flag
- [ ] Create target directory, error if it already exists
- [ ] Fetch template files from raw GitHub (`curl -fsSL`); fail fast on any error
  - Files to copy: `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/*`, `scripts/main.py`, `scripts/sync.py`, `scripts/requirements.txt`, `scripts/Dockerfile`, `scripts/docker-compose.yml`, `scripts/static/graph.js`, `scripts/static/style.css`, `scripts/templates/base.html`, `scripts/templates/note.html`, `scripts/templates/graph.html`
- [ ] Scaffold stub files: `_index.md`, `content/_index.md`, `reports/_index.md`, `sources/bibliography.md`
- [ ] Create empty directories with `.gitkeep`: `sources/assets/`, `.claude/agents/`
- [ ] Run `git init` and make initial commit
- [ ] If `--remote` provided: set remote origin and push
- [ ] Print next steps (open in Claude Code, run Docker, set remote)
- [ ] Works on macOS and Linux with only `bash`, `curl`, `git` — no Python required

---

### 4. Git sync script (`scripts/sync.py`)

- [ ] Parse `--interval <seconds>` (default 900) and `--dry-run` flags
- [ ] Loop every `--interval` seconds:
  - Check `git status --porcelain`
  - If changes: `git add -A` → `git commit -m "auto-sync: <ISO timestamp>"` → `git push --force`
  - Always after: `git pull --rebase`
- [ ] Log every action with an ISO timestamp to stdout
- [ ] Handle errors gracefully (failed push/pull logged, loop continues)

---

### 5. Web server (`scripts/main.py`)

#### Setup
- [ ] FastAPI app reading `WIKI_ROOT` env var (default: parent of `scripts/`)
- [ ] Jinja2 template loading from `scripts/templates/`
- [ ] Static file mount at `/static` from `scripts/static/`

#### Routes
- [ ] `GET /` — render root `_index.md`
- [ ] `GET /content/{path:path}` — render note or `_index.md`; 404 if not found
- [ ] `GET /reports/{slug}` — render a report
- [ ] `GET /sources/assets/{filename}` — serve raw file from `sources/assets/`; 404 if not found
- [ ] `GET /graph` — full-page graph view (renders `graph.html`)
- [ ] `GET /api/graph` — return JSON `{ nodes: [...], links: [...] }` by scanning all `.md` files for `[[links]]`

#### Markdown rendering (shared helper)
- [ ] Parse YAML frontmatter and pass to template context
- [ ] Convert `[[Note Title]]` → `<a href="/content/note-title">Note Title</a>`
- [ ] Convert `[[bibliography#slug]]` → `<a href="/sources/bibliography#slug">slug</a>`
- [ ] Convert `[[assets/file.ext]]` → `<a href="/sources/assets/file.ext">file.ext</a>`
- [ ] Strip `## Backlinks` section before rendering (structural, not for display)
- [ ] Render remaining Markdown to HTML (`python-markdown` with `fenced_code` and `tables` extensions)

---

### 6. Graph view (`scripts/static/graph.js`)

- [ ] Fetch `GET /api/graph` on page load
- [ ] Render D3 force-directed graph in an SVG that fills the viewport
- [ ] Node size scales with inbound link count (min size enforced so isolated nodes are visible)
- [ ] Node color by type: `content` (blue), `_index` (purple), `reports` (green), `bibliography` (amber), `assets` (grey)
- [ ] Node label on hover
- [ ] Click node → navigate to its URL
- [ ] Zoom and pan via D3 zoom behavior
- [ ] Highlight a node and its direct neighbors on hover; dim the rest

---

### 7. HTML templates (`scripts/templates/`)

- [ ] `base.html` — shared layout: top nav (Home, Graph), content area, responsive CSS link
- [ ] `note.html` — extends base; renders frontmatter title + tags as header, then note body
- [ ] `graph.html` — extends base; full-viewport SVG + loads `graph.js`

---

### 8. Styles (`scripts/static/style.css`)

- [ ] Dark background, readable sans-serif body, monospace code blocks
- [ ] Wiki links visually distinct from external links
- [ ] Responsive: readable on mobile, graph view degrades gracefully
- [ ] Minimal — no framework, no utility classes

---

### 9. Docker (`scripts/Dockerfile` + `scripts/docker-compose.yml`)

#### Dockerfile
- [ ] `FROM python:3.12-slim`
- [ ] Copy `scripts/` to `/app`, install `requirements.txt`
- [ ] `CMD` starts both `sync.py` (background) and `uvicorn main:app`

#### docker-compose.yml
- [ ] `wiki` service: build from `scripts/Dockerfile`, mount repo root to `/wiki-data`, expose port 8000, set `WIKI_ROOT=/wiki-data`
- [ ] `claude-remote` service: `ghcr.io/anthropics/claude-code:latest`, run `claude --remote-control`, mount repo root, set working dir to `/wiki-data`

#### Validation
- [ ] `docker compose up` from repo root starts both services
- [ ] Browser at `http://localhost:8000` shows the wiki home page
- [ ] Graph view loads and renders nodes

---

### 10. requirements.txt

- [ ] `fastapi`
- [ ] `uvicorn[standard]`
- [ ] `jinja2`
- [ ] `markdown`
- [ ] `pyyaml`
