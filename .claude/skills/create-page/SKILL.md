---
name: create-page
description: Create a blank wiki page with the required frontmatter at the correct path. Use for quick page creation after the target location has been decided.
---

# Create Page

Create a blank page file at the correct path with proper frontmatter. It is used directly for quick capture and by `research-topic` when a researched topic needs a new page.

## When to invoke

Use this skill when stubbing out a page before filling in content, when `research-topic` has resolved a target path, or when creating multiple related pages in one pass.

## Inputs

- Title (required) — natural-language page title
- Description (required) — one sentence describing what the page is about
- Tags (required)
- Path (optional) — explicit path such as `wiki/pages/topic/my-page.md`; if omitted, `choose-page-location` determines placement

## Steps

### 1. Resolve path

- If a path is provided, use it directly.
- If not, invoke the `choose-page-location` skill with the title to get the target path.
- Do not proceed until `choose-page-location` confirms the path.

### 2. Check for conflicts

- If a file already exists at the target path, stop and report it. Do not overwrite.
- To update an existing page, use `research-topic` instead.

### 3. Write the file

```markdown
---
title: Page Title
description: One sentence describing what this page is about.
tags: [tag-one, tag-two]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

- Set both `created` and `updated` to today's date.
- Leave the body empty. Content writing belongs to the caller.

### 4. Initialize derived structure

- Invoke `update-backlinks update <page-path>` so the page gets the standard backlinks section.
- Invoke `create-index` on the parent directory so its documented structure stays current.
- Invoke `manage-tags validate <page-path>` if the caller wants immediate tag validation.

## Rules

- Never overwrite an existing file. This skill creates only.
- `description` is required.
- Use `manage-tags` for tag validation and taxonomy cleanup.
- Use `choose-page-location` when no explicit path is provided.
- Use `update-backlinks` to add or refresh the backlinks section.
- This skill creates the initial page file, then invokes the follow-up skills that keep related structure in sync.
