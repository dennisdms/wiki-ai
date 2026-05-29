# research

Research a topic, create, update, or rewrite a page, and keep all connected files in sync.

## When to invoke

The user invokes this skill with a topic to research. They may also provide a source:
- A URL → add to sources first, then reference the slug in the page
- An asset path → a file already in `sources/assets/` (PDF, image, etc.) to draw from

## Inputs

- Topic or question (required)
- Optional URL: a source link the user wants stored and cited
- Optional asset path: a path to a file inside `sources/assets/`

## Steps

### 1. Resolve source material

**If the user provides a URL:**
- Invoke `sources add <url>` before writing anything.
- Get back the slug (e.g. `game-feel`).
- Use `[[bibliography#game-feel]]` to cite it in the page body.

**If the user provides an asset path:**
- Confirm the file exists at `sources/assets/<filename>`.
- If not found, stop and tell the user.
- Use `[[assets/filename]]` to reference it in the page body.

**If neither:**
- Proceed with general knowledge and existing wiki pages as sources.

### 2. Check for an existing page

- Grep `pages/` for `.md` files whose `title` frontmatter or filename closely matches the topic.
- If a match is found: update or rewrite it rather than creating a new file. Jump to step 4.

### 3. Determine placement

- Invoke the `hierarchy` skill with the topic name to get the target directory and filename.
- Do not write any files until `hierarchy` confirms the path.

### 4. Write the page

Frontmatter required fields:

```yaml
---
title: Topic Title
description: One sentence stating what this page is about.
tags: [tag-one, tag-two]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Body guidelines:
- Factual, dense prose. Write about the topic — don't meta-comment on the page itself.
- Use `[[other-page-slug]]` to link to related pages in `pages/`.
- Cite sources as `[[bibliography#slug]]` (never inline raw URLs).
- Reference assets as `[[assets/filename]]`.
- End the file with an empty `## Backlinks` section (the `backlinks` skill will populate it).

### 5. Link related pages

- Search `pages/` for pages that should reference the new page but don't yet.
- Insert `[[new-page-slug]]` into their body where it is naturally relevant.
- Update the `updated` date in their frontmatter.

### 6. Refresh directory indexes

- Invoke `index` on the page's parent directory so its documented structure includes the page.
- If a new directory was created, also invoke `index` on its parent.

### 7. Update backlinks

- Invoke `backlinks update <new-page-path>` to populate its `## Backlinks` section.
- Invoke `backlinks update <path>` for every page modified in step 5.

### 8. Validate tags

- Invoke `tags validate <new-page-path>`.

## Rules

- Pages may be rewritten or structurally reorganized when needed to keep them accurate, coherent, and well-linked.
- One page per invocation. If the topic is too broad, narrow it or ask the user to split it.
- Never inline raw URLs in page bodies — always route through `sources`.
- The `description` frontmatter field is required — it feeds the directory index entry for this page.
