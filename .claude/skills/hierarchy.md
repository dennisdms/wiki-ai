# hierarchy

Decides where a page belongs in the `wiki/pages/` folder hierarchy and, if needed, creates a new subdirectory.

## When to invoke

- Before creating a new page (called by `research`)
- When reorganizing existing pages
- When a single page grows too broad and should be split into a cluster

## Inputs

- Topic name or page title
- Optional: existing file path if reorganizing

## Steps

1. **Survey the structure** — list all directories under `wiki/pages/` and read each directory's `_index.md` title.
2. **Match the topic** — find the best-fit existing directory:
   - Exact or close semantic match → place the page there.
   - The topic is clearly a subtopic of an existing directory → place it inside that directory.
   - No reasonable match → go to step 3.
3. **Create a subdirectory** only when:
   - The topic is broad enough to eventually hold 3 or more sibling pages, OR
   - No existing directory is a plausible parent.
   - Name: lowercase kebab-case derived from the topic (e.g. "Game Mechanics" → `game-mechanics/`).
   - Immediately invoke the `index` skill so the new directory's structure is documented in `_index.md`.
4. **Confirm the target path** with the caller before writing any files.
5. **Refresh the parent directory index** — invoke the `index` skill on the parent directory after the page is placed so the folder structure stays accurate.

## Rules

- Never create a directory for a single page unless that page is a clear entry point for a future cluster.
- Max nesting depth is 3 levels: `wiki/pages/<topic>/<subtopic>/page.md`. Do not go deeper.
- A directory with only one child page is a smell — collapse it into the parent unless growth is expected soon.
- Directory names must be lowercase kebab-case (no spaces, no special characters).
- Page filenames must also be lowercase kebab-case with a `.md` extension.
