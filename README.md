# wiki-ai

An AI-powered research wiki template. One repo = one project. Claude Code does the research and maintains the wiki's Markdown end to end; run `python scripts/main.py` to browse the wiki in your browser.

```sh
curl -fsSL https://raw.githubusercontent.com/dennisdms/wiki-ai/main/scripts/init.sh | sh -s -- "my-project"
```

## Run the server

From the repo root:

```sh
python3 scripts/main.py
```

Then open `http://localhost:8000` in your browser.

Use a different port if needed:

```sh
python3 scripts/main.py --port 8080
```

---

## Project Plan

### 1. Repo scaffold

- [x] Create folder structure: `notes/`, `sources/assets/`, `reports/`, `.claude/skills/`, `scripts/static/`, `scripts/templates/`
- [x] Root `_index.md` stub
- [x] `notes/_index.md` stub
- [x] `reports/_index.md` stub
- [x] `sources/bibliography.md` with entry-format comment at top

---

### 2. Skills (`.claude/skills/`)

#### `research`
- [x] Accept a topic as input
- [x] Search `notes/` for an existing note before creating a new one
- [x] Create, update, or rewrite a note under `notes/` with frontmatter (`title`, `tags`, `created`, `updated`)
- [x] Append new external sources to `sources/bibliography.md` (deduplicate by URL)
- [x] Refresh the parent directory index so it includes the new note

#### `index`
- [x] Scan a directory and document its structure in `_index.md`
- [x] Regenerate wiki markdown as needed

---

### 3. Init script (`scripts/init.sh`)

- [x] Require project name as first argument; error if missing
- [x] Create target directory; error if it already exists
- [x] Fetch template files from raw GitHub (`curl -fsSL`)
  - `CLAUDE.md`, `.claude/skills/research`, `.claude/skills/index`, `scripts/main.py`, `scripts/static/style.css`, `scripts/static/graph.js`, `scripts/templates/base.html`, `scripts/templates/note.html`
- [x] Scaffold stub files: `_index.md`, `notes/_index.md`, `reports/_index.md`, `sources/bibliography.md`
- [x] Run `git init` and make initial commit
- [x] Print next steps: open in Claude Code, run `python scripts/main.py`
- [x] Works on macOS and Linux — only requires `bash`, `curl`, `git`

---

### 4. Web server (`scripts/main.py`)

- [x] `http.server.BaseHTTPRequestHandler` — stdlib only, no dependencies
- [x] `GET /` — render root `_index.md`
- [x] `GET /notes/<path>` — render note or `_index.md`; 404 if not found
- [x] `GET /graph` — full-page D3 force-directed graph
- [x] `GET /api/graph` — JSON `{ nodes, links }` built by scanning `[[links]]` in all `.md` files
- [x] `GET /static/<file>` — serve CSS/JS
- [x] Markdown rendering: frontmatter, `[[wiki-links]]` → `<a>`, headings, bold, italic, code, lists
- [x] Start on port 8000; print `http://localhost:8000`

---

### 5. Graph view (`scripts/static/graph.js`)

- [x] Fetch `/api/graph` and render a D3 force-directed graph filling the viewport
- [x] Click a node to navigate to it; zoom and pan
- [x] Node color by type: notes (blue), indexes (purple), reports (green)
