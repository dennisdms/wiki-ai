# page

Creates a blank page file at the correct path with proper frontmatter. This is the file-creation primitive used directly by the user for quick page capture, and called by `research` for the actual write step.

## When to invoke

- When you want to stub out a page before filling in content
- Called by `research` after hierarchy resolves the target path
- When creating multiple related pages in one pass

## Inputs

- Title (required) — natural-language page title
- Description (required) — one sentence describing what this page is about
- Tags (required) — 1–5 lowercase kebab-case tags
- Path (optional) — explicit path (e.g. `wiki/pages/topic/my-page.md`); if omitted, `hierarchy` determines placement

## Steps

### 1. Resolve path

- If path is provided: use it directly.
- If not: invoke the `hierarchy` skill with the title to get the target path. Do not proceed until `hierarchy` confirms.

### 2. Derive filename

- Lowercase kebab-case from the title: `"Game Feel"` → `game-feel.md`
- No spaces, no special characters, `.md` extension

### 3. Check for conflicts

- If a file already exists at the target path: stop and report it. Do not overwrite.
- To update an existing page, use `research` instead.

### 4. Write the file

```markdown
---
title: Page Title
description: One sentence describing what this page is about.
tags: [tag-one, tag-two]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Backlinks

<!-- Auto-maintained by backlinks skill -->
<!-- No backlinks yet -->
```

- Set both `created` and `updated` to today's date.
- Leave the body empty between the frontmatter and `## Backlinks` — content is added after creation.

### 5. Refresh the parent directory index

- Invoke `index` on the parent directory so its documented structure stays current.

## Rules

- Never overwrite an existing file — this skill creates only; use `research` to update.
- `description` is required — do not create a page without one.
- Tags must follow wiki conventions: lowercase kebab-case, 1–5 per page.
- Filename must be lowercase kebab-case derived from the title.
- `## Backlinks` must be the last section — nothing follows it.
- This skill writes only the page file itself and triggers `index` on the parent directory.
