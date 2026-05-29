---
name: research-topic
description: Research a topic, create or update a wiki page, and keep sources, indexes, backlinks, and tags in sync. Use when the user asks to research, summarize, rewrite, or expand a page.
---

# Research Topic

Research a topic, create, update, or rewrite a page, and keep all connected files in sync.

## When to invoke

Use this skill when the user asks to research a topic for the wiki, expand an existing page, or create a new page from a topic plus optional source material.

The user may also provide a source:
- A URL → add it to sources first, then reference the slug in the page.
- An asset path → a file already in `wiki/sources/assets/` to draw from.

## Inputs

- Topic or question (required)
- Optional URL: a source link the user wants stored and cited
- Optional asset path: a path to a file inside `wiki/sources/assets/`

## Steps

### 1. Resolve source material

**If the user provides a URL:**
- Invoke `manage-sources add <url>` before writing anything.
- Get back the slug (for example `game-feel`).
- Use `[[bibliography#game-feel]]` to cite it in the page body.

**If the user provides an asset path:**
- Confirm the file exists at `wiki/sources/assets/<filename>`.
- If not found, stop and tell the user.
- Use `[[assets/filename]]` to reference it in the page body.

**If neither:**
- Proceed with general knowledge and existing wiki pages as sources.

### 2. Check for an existing page

- Search `wiki/pages/` for `.md` files whose `title` frontmatter or filename closely matches the topic.
- If a match is found, update or rewrite it rather than creating a new file. Then continue with the write/update flow.

### 3. Determine placement

- Invoke the `choose-page-location` skill with the topic name to get the target directory and filename.
- Do not write any files until `choose-page-location` confirms the path.

### 4. Write the page

Required frontmatter:

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
- Write factual, dense prose about the topic. Do not meta-comment on the page itself.
- Use `[[other-page-slug]]` to link to related pages in `wiki/pages/`.
- Cite sources as `[[bibliography#slug]]` and never inline raw URLs.
- Reference assets as `[[assets/filename]]`.
- End the file with an empty `## Backlinks` section so the `update-backlinks` skill can populate it.

### 5. Link related pages

- Search `wiki/pages/` for pages that should reference the new or updated page but do not yet.
- Insert `[[new-page-slug]]` where it is naturally relevant.
- Update the `updated` date in any page you modify.

### 6. Refresh directory indexes

- Invoke `create-index` on the page's parent directory so its documented structure includes the page.
- If a new directory was created, also invoke `create-index` on its parent.

### 7. Update backlinks

- Invoke `update-backlinks update <new-page-path>` to populate its `## Backlinks` section.
- Invoke `update-backlinks update <path>` for every page modified while adding related links.

### 8. Validate tags

- Invoke `manage-tags validate <new-page-path>`.

## Rules

- One page per invocation. If the topic is too broad, narrow it or ask the user to split it.
- Reuse and rewrite existing pages when that keeps the wiki cleaner than creating duplicates.
- Never inline raw URLs in page bodies. Always route them through `manage-sources`.
- The `description` frontmatter field is required because directory indexes depend on it.
