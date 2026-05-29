# research

Research a topic, create or update a note, and keep all connected files in sync.

## When to invoke

The user invokes this skill with a topic to research. They may also provide a source:
- A URL → add to bibliography first, then reference the slug in the note
- An asset path → a file already in `sources/assets/` (PDF, image, etc.) to draw from

## Inputs

- Topic or question (required)
- Optional URL: a source link the user wants stored and cited
- Optional asset path: a path to a file inside `sources/assets/`

## Steps

### 1. Resolve source material

**If the user provides a URL:**
- Invoke `bibliography add <url>` before writing anything.
- Get back the slug (e.g. `game-feel`).
- Use `[[bibliography#game-feel]]` to cite it in the note body.

**If the user provides an asset path:**
- Confirm the file exists at `sources/assets/<filename>`.
- If not found, stop and tell the user — never create or move asset files.
- Use `[[assets/filename]]` to reference it in the note body.

**If neither:**
- Proceed with general knowledge and existing wiki notes as sources.

### 2. Check for an existing note

- Grep `notes/` for `.md` files whose `title` frontmatter or filename closely matches the topic.
- If a match is found: update it rather than creating a new file. Jump to step 4.

### 3. Determine placement

- Invoke the `hierarchy` skill with the topic name to get the target directory and filename.
- Do not write any files until `hierarchy` confirms the path.

### 4. Write the note

Frontmatter required fields:

```yaml
---
title: Topic Title
description: One sentence stating what this note is about.
tags: [tag-one, tag-two]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Body guidelines:
- Factual, dense prose. Write about the topic — don't meta-comment on the note itself.
- Use `[[other-note-slug]]` to link to related notes in `notes/`.
- Cite sources as `[[bibliography#slug]]` (never inline raw URLs).
- Reference assets as `[[assets/filename]]`.
- End the file with an empty `## Backlinks` section (the `backlinks` skill will populate it).

### 5. Link related notes

- Search `notes/` for notes that should reference the new note but don't yet.
- Insert `[[new-note-slug]]` into their body where it is naturally relevant.
- Update the `updated` date in their frontmatter.

### 6. Update indexes

- Invoke `index` on the note's parent directory.
- If a new directory was created, also invoke `index` on its parent.

### 7. Update backlinks

- Invoke `backlinks update <new-note-path>` to populate its `## Backlinks` section.
- Invoke `backlinks update <path>` for every note modified in step 5.

### 8. Validate tags

- Invoke `tags validate <new-note-path>`.

## Rules

- One note per invocation. If the topic is too broad, narrow it or ask the user to split it.
- Never inline raw URLs in note bodies — always route through `bibliography`.
- Never create, move, rename, or delete files in `sources/assets/` — that directory is user-managed.
- The `description` frontmatter field is required — it feeds the `_index.md` entry for this note.
- Non-`.md` files in the wiki are never touched.
