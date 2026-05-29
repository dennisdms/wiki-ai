# wiki-ai

An AI-powered research wiki template. One repo = one project. Claude Code does the research and maintains the wiki's Markdown end to end; run `python3 scripts/server/main.py` to browse the wiki in your browser. The browser UI is rooted at `wiki/`, not the repo root.

```sh
curl -fsSL https://raw.githubusercontent.com/dennisdms/wiki-ai/main/scripts/init.sh | sh -s -- "my-project"
```

## Run the server

From the repo root:

```sh
python3 scripts/server/main.py
```

Then open `http://localhost:8000` in your browser.

Use a different port if needed:

```sh
python3 scripts/server/main.py --port 8080
```

---

## Project Plan

### 1. Repo scaffold

- [x] Create folder structure: `wiki/pages/`, `wiki/sources/assets/`, `wiki/reports/`, `.claude/skills/`, `scripts/server/static/`, `scripts/server/templates/`
- [x] `wiki/_index.md` stub
- [x] `wiki/pages/_index.md` stub
- [x] `wiki/reports/_index.md` stub
- [x] `wiki/sources/bibliography.md`

---

### 2. Skills (`.claude/skills/`)

#### `research`
- [x] Accept a topic as input
- [x] Search `wiki/pages/` for an existing page before creating a new one
- [x] Create, update, or rewrite a page under `wiki/pages/` with frontmatter (`title`, `tags`, `created`, `updated`)
- [x] Append new external sources to `wiki/sources/bibliography.md` (deduplicate by URL)
- [x] Refresh the parent directory index so it includes the new page

#### `index`
- [x] Scan a directory and document its structure in `_index.md`
- [x] Regenerate wiki markdown as needed

---

### 3. Init script (`scripts/init.sh`)

- [x] Require project name as first argument; error if missing
- [x] Create target directory; error if it already exists
- [x] Fetch template files from raw GitHub (`curl -fsSL`)
  - `CLAUDE.md`, `.claude/skills/research`, `.claude/skills/sources`, `.claude/skills/index`, `.claude/skills/backlinks`, `.claude/skills/hierarchy`, `.claude/skills/page`, `.claude/skills/tags`, `scripts/server/main.py`, `scripts/server/static/style.css`, `scripts/server/static/graph.js`, `scripts/server/templates/base.html`, `scripts/server/templates/page.html`, `wiki/sources/_index.md`, `wiki/sources/assets/_index.md`
- [x] Scaffold stub files: `wiki/_index.md`, `wiki/pages/_index.md`, `wiki/reports/_index.md`, `wiki/sources/bibliography.md`
- [x] Run `git init` and make initial commit
- [x] Print next steps: open in Claude Code, run `python3 scripts/server/main.py`
- [x] Works on macOS and Linux — only requires `bash`, `curl`, `git`

---

### 4. Web server (`scripts/server/main.py`)

- [x] `http.server.BaseHTTPRequestHandler` — stdlib only, no dependencies
- [x] `GET /` — render `wiki/_index.md`
- [x] `GET /pages/<path>` — render a page or `_index.md` from `wiki/pages/`; 404 if not found
- [x] `GET /graph` — full-page D3 force-directed graph
- [x] `GET /api/graph` — JSON `{ nodes, links }` built by scanning `[[links]]` in markdown files under `wiki/`
- [x] `GET /static/<file>` — serve CSS/JS
- [x] Markdown rendering: frontmatter, `[[wiki-links]]` → `<a>`, headings, bold, italic, code, lists
- [x] Start on port 8000; print `http://localhost:8000`

---

### 5. Graph view (`scripts/server/static/graph.js`)

- [x] Fetch `/api/graph` and render a D3 force-directed graph filling the viewport
- [x] Click a node to navigate to it; zoom and pan
- [x] Node color by type: pages (blue), indexes (purple), reports (green)
