---
name: create-index
description: Regenerate a directory `_index.md` from the actual contents of a wiki folder. Use after adding, removing, moving, or reorganizing pages, source files, assets, or subdirectories.
---

# Create Index

Document a directory's structure and contents by creating or regenerating its `_index.md`.

## When to invoke

Use this skill after creating a directory, adding or removing a page, source file, or asset, refreshing stale directory documentation, or whenever a wiki directory is missing its `_index.md`.

## Inputs

- Directory path to index, for example `wiki/pages/game-mechanics/`
- This skill also applies to top-level directories such as `wiki/sources/` and `wiki/assets/`

## Directory index template

Every directory index must follow this structure:

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

Examples for the non-page directories:

```markdown
- [[gamedeveloper.com]] — Source entries collected from Game Developer.
- `design-notes.pdf` — PDF asset used as source material for multiple pages.
- `combat-reference.png` — Image asset used as a visual reference.
```

Key points:
- `path:` is the directory path relative to the repo root, with a trailing slash.
- `## Contents` documents the folder's direct children, not the `_index.md` file itself.
- Every entry in `## Contents` needs a description.
- Files and directories share one list, sorted alphabetically by visible label.
- In `wiki/sources/`, website source files are listed as wiki-links such as `[[gamedeveloper.com]]`.
- In `wiki/assets/`, non-Markdown files are listed as inline code filenames such as `` `design-notes.pdf` ``.

## Steps

1. Read the existing `_index.md` if one exists.
   - Reuse any still-correct title or context when helpful, but rewrite the file as needed.
   - If no existing file exists, derive a title from the directory name and set `path:` from the directory argument.
2. Scan the directory for direct children:
   - Markdown files other than `_index.md`
   - Non-Markdown files when indexing `wiki/assets/`
   - Subdirectories that contain an `_index.md`
3. Collect descriptions:
   - For each Markdown page, use its frontmatter `description` field.
   - If that is absent, use the first non-heading sentence of its body.
   - If that is still absent, use its `title` frontmatter value.
   - For each subdirectory, use the first sentence of the context in that subdirectory's `_index.md`.
   - If that is absent, use the subdirectory's `title` frontmatter.
   - For website source files in `wiki/sources/`, prefer a short description derived from the file's title or opening context.
   - For non-Markdown asset files in `wiki/assets/`, describe the file type and apparent purpose from its filename. If that is unclear, use `Asset file.`
4. Build the contents list:
   - Format Markdown page entries as `- [[slug]] — Description.`
   - Format subdirectory entries as `- [[subdir/_index]] — Description.`
   - Format asset file entries as `- ` + inline-code filename + ` — Description.`
   - Sort alphabetically by visible label.
   - If no description can be found, write `— (no description yet)`.
5. Write the file so it documents the directory's current structure using the template above.

## Rules

- Every directory in the wiki must have an `_index.md`. This is a hard invariant.
- The `## Contents` section is fully regenerated on every run.
- Do not insert maintenance comments or hidden markers into `_index.md`.
- `path:` must reflect the actual directory and include a trailing slash.
- If the directory is empty, write an empty `## Contents` section.
- `_index.md` files themselves do not appear as entries. Use `[[subdir/_index]]` for subdirectories.
- Source files under `wiki/sources/` are normal Markdown entries and should be linked with wiki-links.
- Asset files under `wiki/assets/` are not Markdown pages and should be listed as plain filenames, not wiki-links.
- This skill only writes markdown files. It never creates, moves, or deletes non-markdown files.
- After regenerating an index, scan all direct subdirectories and flag any that are missing their own `_index.md`.
