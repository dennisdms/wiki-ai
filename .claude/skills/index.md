# index

Documents a directory's structure and contents by creating or regenerating its `_index.md`.

## When to invoke

- After creating a new directory (called by `hierarchy`)
- After adding or removing a page from a directory (called by `research`, `cleanup`)
- Directly to refresh stale or missing directory documentation
- When any directory is discovered to be missing an `_index.md` — every directory in the wiki must have one

## Inputs

- Directory path to index (e.g. `wiki/pages/game-mechanics/`)

## Directory index template

Every directory index must follow this exact structure:

```markdown
---
title: Topic Title
path: wiki/pages/topic/
---

# Topic Title

One or two sentences of context. What unifies these pages?
What questions does this cluster address?

## Contents

- [[page-slug]] — One sentence describing what this page covers.
- [[another-page]] — One sentence describing what this page covers.
- [[subtopic/_index]] — One sentence describing what this subdirectory contains.
```

Key points:
- `path:` in frontmatter is the directory path relative to the repo root, trailing slash included.
- `## Contents` documents the folder's direct children, not the `_index.md` file itself.
- Every entry in `## Contents` has a description — no bare links, no missing descriptions.
- Files and directories are mixed in one list, sorted alphabetically by slug.

## Steps

1. **Read existing `_index.md`** if one exists:
   - Reuse any still-correct title or context if it helps, but rewrite the file as needed.
   - If no existing file, derive a title from the directory name (kebab-case → Title Case) and set `path:` from the directory argument.
2. **Scan the directory** for:
   - `.md` files (exclude `_index.md` itself) — these are pages.
   - Subdirectories that contain an `_index.md` — these are sub-topic clusters.
3. **Collect descriptions**:
   - For each page: use its frontmatter `description` field. If absent, use the first non-heading sentence of its body. If still absent, use its `title` frontmatter value.
   - For each subdirectory: use the first sentence of the context in the subdirectory's `_index.md` (the text between the `# Heading` and `## Contents`). If absent, use the subdirectory's `title` frontmatter.
4. **Build the contents list**:
   - Format each line: `- [[slug]] — Description.`
   - For subdirectories: `- [[subdir/_index]] — Description.`
   - Sort alphabetically by slug.
   - Every entry must have a description — if none can be found, write `— (no description yet)` as a placeholder.
5. **Write the file** so it documents the directory's current structure using the template above.

## Rules

- All wiki markdown is AI-maintained end to end; human edits are not protected state and may be overwritten.
- This skill may regenerate the whole file whenever needed.
- **Every directory in the wiki must have an `_index.md`.** This is a hard invariant. If you encounter a directory without one while running this skill, create it before proceeding.
- The `## Contents` section is fully regenerated on every run.
- Do not insert maintenance comments or other hidden markers into `_index.md`; they are implementation artifacts and should not appear in the reader-facing UI.
- `path:` must reflect the actual directory, with a trailing slash.
- If the directory is empty, write an empty `## Contents` section.
- `_index.md` files themselves do not appear as entries — use `[[subdir/_index]]` for subdirectories.
- This skill only writes `.md` files — it never creates, moves, or deletes non-markdown files.
- After regenerating an index, scan all direct subdirectories and flag any that are missing their own `_index.md`.
