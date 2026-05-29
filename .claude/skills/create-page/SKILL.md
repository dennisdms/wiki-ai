---
name: create-page
description: Create a blank wiki page with the required frontmatter and backlinks stub at the correct path. Use for quick page creation after the target location has been decided.
---

# Create Page

Create a blank page file at the correct path with proper frontmatter. This is the file-creation primitive used directly by the user for quick capture and by `research-topic` for the actual write step.

## When to invoke

Use this skill when stubbing out a page before filling in content, when `research-topic` has resolved a target path, or when creating multiple related pages in one pass.

## Inputs

- Title (required) — natural-language page title
- Description (required) — one sentence describing what the page is about
- Tags (required) — 1 to 5 lowercase kebab-case tags
- Path (optional) — explicit path such as `wiki/pages/topic/my-page.md`; if omitted, `choose-page-location` determines placement

## Steps

### 1. Resolve path

- If a path is provided, use it directly.
- If not, invoke the `choose-page-location` skill with the title to get the target path.
- Do not proceed until `choose-page-location` confirms the path.

### 2. Derive filename

- Convert the title to lowercase kebab-case, for example `Game Feel` → `game-feel.md`.
- Use no spaces or special characters.

### 3. Check for conflicts

- If a file already exists at the target path, stop and report it. Do not overwrite.
- To update an existing page, use `research-topic` instead.

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

<!-- Auto-maintained by update-backlinks skill -->
<!-- No backlinks yet -->
```

- Set both `created` and `updated` to today's date.
- Leave the body empty between the frontmatter and `## Backlinks`.

### 5. Refresh the parent directory index

- Invoke `create-index` on the parent directory so its documented structure stays current.

## Rules

- Never overwrite an existing file. This skill creates only.
- `description` is required.
- Tags must follow wiki conventions: lowercase kebab-case, 1 to 5 per page.
- The filename must be lowercase kebab-case derived from the title.
- `## Backlinks` must be the last section in the file.
- This skill writes only the page file itself and triggers `create-index` on the parent directory.
