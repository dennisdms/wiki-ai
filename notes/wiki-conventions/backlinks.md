---
title: Backlinks
description: How the ## Backlinks section works and why it must stay as the final section.
tags: [wiki-conventions, navigation]
created: 2026-05-28
updated: 2026-05-28
---

# Backlinks

Backlinks make the wiki navigable from any direction, not just top-down through the hierarchy. Every note that is referenced by another note records that reference at the bottom of the file.

## How they work

When note A contains `[[note-b]]`, the `backlinks` skill adds `[[note-a]]` to note B's `## Backlinks` section. This happens automatically after any note is created or updated.

## The section

The `## Backlinks` section is always the last section in a note:

```markdown
## Backlinks

<!-- Auto-maintained by backlinks skill -->
- [[note-a]]
- [[note-c]]
```

If a note has no inbound links:

```markdown
## Backlinks

<!-- Auto-maintained by backlinks skill -->
<!-- No backlinks yet -->
```

## What counts as a backlink

- Links from any note in `notes/`
- Links from any report in `reports/`
- Links from `_index.md` files count but are lower priority

Links from `sources/bibliography.md` do not create backlinks — bibliography entries are referenced by notes, not the other way around.

## What to avoid

- Never hand-edit the `## Backlinks` section. It will be overwritten on the next run.
- Never put anything after `## Backlinks` — it must be the final section.
- Do not reference a note by a different slug than its filename; the skill matches on filename.

## Keeping backlinks current

The `backlinks` skill is invoked automatically by `research` and `cleanup`. For a manual repair pass across the whole wiki: `/backlinks update-all`. To inspect a single note without writing: `/backlinks scan notes/my-note.md`.

## Backlinks

<!-- Auto-maintained by backlinks skill -->
<!-- No backlinks yet -->
