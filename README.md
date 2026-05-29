# wiki-ai

An AI-powered research wiki template. One repo = one project. Claude Code does the research; run `python scripts/main.py` to browse the wiki in your browser.

```sh
curl -fsSL https://raw.githubusercontent.com/dennisdms/wiki-ai/main/scripts/init.sh | sh -s -- "my-project"
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
- [ ] Accept a topic as input
- [ ] Search `notes/` for an existing note before creating a new one
- [ ] Create or update a note under `notes/` with frontmatter (`title`, `tags`, `created`, `updated`)
- [ ] Append new external sources to `sources/bibliography.md` (deduplicate by URL)
- [ ] Update the parent `_index.md` to include the new note

#### `index`
- [ ] Scan a directory and regenerate its `_index.md` link list
- [ ] Preserve any hand-written narrative above the link list

---

### 3. Init script (`scripts/init.sh`)

- [ ] Require project name as first argument; error if missing
- [ ] Create target directory; error if it already exists
- [ ] Fetch template files from raw GitHub (`curl -fsSL`)
  - `CLAUDE.md`, `.claude/skills/research`, `.claude/skills/index`, `scripts/main.py`, `scripts/static/style.css`, `scripts/static/graph.js`, `scripts/templates/base.html`, `scripts/templates/note.html`
- [ ] Scaffold stub files: `_index.md`, `notes/_index.md`, `reports/_index.md`, `sources/bibliography.md`
- [ ] Run `git init` and make initial commit
- [ ] Print next steps: open in Claude Code, run `python scripts/main.py`
- [ ] Works on macOS and Linux — only requires `bash`, `curl`, `git`

---

### 4. Web server (`scripts/main.py`)

- [ ] `http.server.BaseHTTPRequestHandler` — stdlib only, no dependencies
- [ ] `GET /` — render root `_index.md`
- [ ] `GET /notes/<path>` — render note or `_index.md`; 404 if not found
- [ ] `GET /graph` — full-page D3 force-directed graph
- [ ] `GET /api/graph` — JSON `{ nodes, links }` built by scanning `[[links]]` in all `.md` files
- [ ] `GET /static/<file>` — serve CSS/JS
- [ ] Markdown rendering: frontmatter, `[[wiki-links]]` → `<a>`, headings, bold, italic, code, lists
- [ ] Start on port 8000; print `http://localhost:8000`

---

### 5. Graph view (`scripts/static/graph.js`)

- [ ] Fetch `/api/graph` and render a D3 force-directed graph filling the viewport
- [ ] Click a node to navigate to it; zoom and pan
- [ ] Node color by type: notes (blue), indexes (purple), reports (green)
