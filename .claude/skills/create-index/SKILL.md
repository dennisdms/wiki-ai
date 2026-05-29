---
name: create-index
description: Regenerate a directory `_index.md` from the actual markdown contents of a wiki folder. Use after adding, removing, moving, or reorganizing pages or subdirectories.
---

# Create Index

Document a directory's structure and contents by creating or regenerating its `_index.md`.

## When to invoke

Use this skill after creating a directory, adding or removing a page, refreshing stale directory documentation, or whenever a wiki directory is missing its `_index.md`.

## Inputs

- Directory path to index, for example `wiki/pages/game-mechanics/`

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

Key points:
- `path:` is the directory path relative to the repo root, with a trailing slash.
- `## Contents` documents the folder's direct children, not the `_index.md` file itself.
- Every entry in `## Contents` needs a description.
- Files and directories share one list, sorted alphabetically by slug.

## Steps

1. Read the existing `_index.md` if one exists.
   - Reuse any still-correct title or context when helpful, but rewrite the file as needed.
   - If no existing file exists, derive a title from the directory name and set `path:` from the directory argument.
2. Scan the directory for:
   - `.md` files other than `_index.md`
   - Subdirectories that contain an `_index.md`
3. Collect descriptions:
   - For each page, use its frontmatter `description` field.
   - If that is absent, use the first non-heading sentence of its body.
   - If that is still absent, use its `title` frontmatter value.
   - For each subdirectory, use the first sentence of the context in that subdirectory's `_index.md`.
   - If that is absent, use the subdirectory's `title` frontmatter.
4. Build the contents list:
   - Format page entries as `- [[slug]] — Description.`
   - Format subdirectory entries as `- [[subdir/_index]] — Description.`
   - Sort alphabetically by slug.
   - If no description can be found, write `— (no description yet)`.
5. Write the file so it documents the directory's current structure using the template above.

## Rules

- Every directory in the wiki must have an `_index.md`. This is a hard invariant.
- The `## Contents` section is fully regenerated on every run.
- Do not insert maintenance comments or hidden markers into `_index.md`.
- `path:` must reflect the actual directory and include a trailing slash.
- If the directory is empty, write an empty `## Contents` section.
- `_index.md` files themselves do not appear as entries. Use `[[subdir/_index]]` for subdirectories.
- This skill only writes markdown files. It never creates, moves, or deletes non-markdown files.
- After regenerating an index, scan all direct subdirectories and flag any that are missing their own `_index.md`.
