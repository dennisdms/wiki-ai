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

Core template work is in place. The checklist below marks shipped pieces as complete and leaves the remaining hardening work unchecked.

### 1. Repo scaffold

- [x] Create the core folder structure: `wiki/pages/`, `wiki/reports/`, `wiki/sources/assets/`, `.claude/skills/<skill>/SKILL.md`, `scripts/server/static/`, `scripts/server/templates/`
- [x] Ship wiki entrypoints and recursive indexes: `wiki/_index.md`, `wiki/pages/_index.md`, `wiki/reports/_index.md`, `wiki/sources/_index.md`, `wiki/sources/assets/_index.md`
- [x] Provide bibliography storage at `wiki/sources/bibliography.md`
- [x] Include template docs/config: `README.md`, `CLAUDE.md`, `.claude/settings.json`
- [x] Document the script tree with `scripts/_index.md`, `scripts/server/_index.md`, `scripts/server/static/_index.md`, `scripts/server/templates/_index.md`

---

### 2. Skills (`.claude/skills/`)

#### `research-topic`
- [x] Accept a topic plus optional URL or asset input
- [x] Reuse an existing page when there is already a close match in `wiki/pages/`
- [x] Create or rewrite a page with required frontmatter: `title`, `description`, `tags`, `created`, `updated`
- [x] Keep related pages, parent indexes, backlinks, and tags in sync after page updates

#### `manage-sources`
- [x] Add and deduplicate bibliography entries by URL
- [x] Support finding, auditing, and removing bibliography entries by slug or URL/title
- [x] Enforce `wiki/sources/bibliography.md` as the only place raw URLs live

#### `create-index`
- [x] Regenerate any directory `_index.md` from the directory's actual markdown contents
- [x] Include page and subdirectory descriptions in `## Contents`
- [x] Enforce the invariant that every wiki directory has an `_index.md`

#### `choose-page-location`
- [x] Choose the best target directory for a new page under `wiki/pages/`
- [x] Create a new subdirectory only when the topic warrants a cluster
- [x] Refresh parent indexes after structure changes

#### `create-page`
- [x] Create a blank page at the correct path with required frontmatter and an empty backlinks section
- [x] Refuse to overwrite an existing file

#### `update-backlinks`
- [x] Rebuild `## Backlinks` for a single page or the entire wiki
- [x] Include backlinks from both `wiki/pages/` and `wiki/reports/`
- [x] Keep backlinks sorted and always last in the file

#### `manage-tags`
- [x] Validate per-page tags against the current taxonomy
- [x] Audit tag usage across `wiki/pages/`
- [x] Support tag rename and merge operations across the wiki

#### `create-skill`
- [x] Turn a user request or prompt into a focused Claude Code skill
- [x] Guide naming, scope, structure, and discovery wording
- [x] Validate frontmatter, examples, and supporting-file layout before finishing

---

### 3. Init script (`scripts/init.sh`)

- [x] Require a project name as the first argument; error if missing
- [x] Create the target directory; error if it already exists
- [x] Fetch template files from raw GitHub with `curl -fsSL`
  - `README.md`, `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/research-topic/SKILL.md`, `.claude/skills/manage-sources/SKILL.md`, `.claude/skills/create-index/SKILL.md`, `.claude/skills/update-backlinks/SKILL.md`, `.claude/skills/choose-page-location/SKILL.md`, `.claude/skills/create-page/SKILL.md`, `.claude/skills/manage-tags/SKILL.md`, `.claude/skills/create-skill/SKILL.md`, `scripts/_index.md`, `scripts/server/_index.md`, `scripts/server/main.py`, `scripts/server/static/style.css`, `scripts/server/static/graph.js`, `scripts/server/static/_index.md`, `scripts/server/templates/base.html`, `scripts/server/templates/page.html`, `scripts/server/templates/_index.md`, `wiki/sources/_index.md`, `wiki/sources/assets/_index.md`
- [x] Scaffold stub files: `wiki/_index.md`, `wiki/pages/_index.md`, `wiki/reports/_index.md`, `wiki/sources/bibliography.md`
- [x] Run `git init` and make an initial commit
- [x] Print next steps: open in Claude Code and run `python3 scripts/server/main.py`
- [x] Work on macOS and Linux with only `bash`, `curl`, and `git`

---

### 4. Web server (`scripts/server/main.py`)

- [x] Use the Python standard library only (`http.server`, no framework or install step)
- [x] Render any markdown page under `wiki/`, including `/`, `/pages/...`, `/reports/...`, and `/sources/...`
- [x] Serve `/graph` and `/api/graph` for the wiki graph view
- [x] Serve static assets from `/static/...`
- [x] Convert frontmatter-aware markdown to HTML with `[[wiki-links]]`, markdown links, headings, emphasis, code, blockquotes, and ordered/unordered lists
- [x] Strip the `## Backlinks` section from rendered HTML while preserving it in source markdown
- [x] Surface page metadata such as path, dates, and tags in the UI
- [x] Start on port 8000 by default and print `http://localhost:<port>`

---

### 5. Browser UI (`scripts/server/templates/`, `scripts/server/static/`)

- [x] Provide a shared base template with wiki navigation (`Home`, `Pages`, `Reports`, `Graph`)
- [x] Provide a readable dark-mode stylesheet for markdown pages and metadata
- [x] Lazy-load D3 from a CDN for the graph page
- [x] Render a full-viewport force-directed graph from `/api/graph`
- [x] Support click-to-navigate, zoom, pan, drag, labels, tooltips, and resize-aware graph layout
- [x] Color nodes by type: page, index, report, or other

---

### 6. Remaining work

- [ ] Serve and render `[[assets/filename]]` links from `wiki/sources/assets/` so asset references used by the skills work in the browser UI
- [ ] Add an automated smoke test for `scripts/init.sh` that scaffolds a fresh project and verifies the expected files are created
- [ ] Add automated tests for `scripts/server/main.py` covering markdown rendering, wiki-link resolution, and `/api/graph`
- [ ] Add a simple validation workflow or script to keep the template files and README plan in sync
