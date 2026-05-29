---
name: research-topic
description: Research a topic, create or update a wiki page, and keep sources, indexes, backlinks, and tags in sync. Use when the user asks to research, summarize, rewrite, or expand a page.
---

# Research Topic

Research a topic, create, update, or rewrite a page, and keep all connected files in sync.

## When to invoke

Use this skill when the user asks to research a topic for the wiki, expand an existing page, or create a new page from a topic plus optional source material.

The user may also provide an explicit source:
- A URL → add it to sources first, then reference the returned source entry in the page.
- An asset path → a file already in `wiki/assets/` to draw from.

Unless the user provides an explicit source, do web research before writing.

## Inputs

- Topic or question (required)
- Optional URL: a source link the user wants stored and cited
- Optional asset path: a path to a file inside `wiki/assets/`

## Steps

### 1. Resolve source material

**If the user provides a URL:**
- Invoke `manage-sources add <url>` before writing anything.
- Get back the source reference (for example `sources/gamedeveloper.com#game-feel`).
- Use `[[sources/gamedeveloper.com#game-feel]]` to cite it in the page body.

**If the user provides an asset path:**
- Confirm the file exists at `wiki/assets/<filename>`.
- If not found, stop and tell the user.
- Use `[[assets/filename]]` to reference it in the page body.

**If neither:**
- Do web research before writing.
- Match the breadth of research to the scope of the request:
  - Simple questions: use 1–3 relevant sources.
  - Standard research requests: use 5–10 relevant sources.
  - Deep-dive questions: use 10–15 relevant sources.
- Add each external URL you rely on through `manage-sources` before citing it in the page.
- Synthesize the answer from the gathered sources.
- Do not rely on your own memory, prior knowledge, or model weights as the basis for factual claims.
- Use existing wiki pages as supporting context, but not as a substitute for web research.

### 2. Check for an existing page

- Search `wiki/pages/` for `.md` files whose `title` frontmatter or filename closely matches the topic.
- If a match is found, update or rewrite it rather than creating a new file. Then continue with the write/update flow.

### 3. Determine placement for a new page

- If you are creating a new page, invoke `choose-page-location` with the topic name to get the target path.
- Do not create files or directories until the target path is confirmed.

### 4. Create the page if needed

- If a matching page already exists, skip page creation and update that file.
- If no matching page exists, invoke `create-page` with the resolved title, description, tags, and path.
- Use `create-page` to create the initial blank page with the required frontmatter.

### 5. Write or rewrite the content

- For a newly created page, fill in the blank page created by `create-page`.
- For an existing page, update or rewrite the content while keeping required metadata valid.
- Set `updated` to today's date on every page you modify.

Body guidelines:
- Write factual, dense prose about the topic. Do not meta-comment on the page itself.
- Synthesize the page's claims from the gathered sources rather than from your own memory or model knowledge.
- Use `[[other-page-slug]]` to link to related pages in `wiki/pages/`.
- Cite sources as `[[sources/<website>#<slug>]]` and never inline raw URLs.
- Reference assets as `[[assets/filename]]`.

### 6. Link related pages

- Search `wiki/pages/` for pages that should reference the new or updated page but do not yet.
- Insert `[[new-page-slug]]` where it is naturally relevant.
- Update the `updated` date in any page you modify.

### 7. Refresh affected indexes

- Invoke `create-index` on any directory whose direct contents changed.
- If you created a new directory, also refresh its parent directory index.

### 8. Update backlinks

- Invoke `update-backlinks update <page-path>` for the page you created or updated.
- Invoke `update-backlinks update <path>` for every page modified while adding related links.

### 9. Validate tags

- Invoke `manage-tags validate <page-path>` for the page you created or updated.

## Rules

- One page per invocation. If the topic is too broad, narrow it or ask the user to split it.
- Reuse and rewrite existing pages when that keeps the wiki cleaner than creating duplicates.
- Do not rely on your own memory, prior knowledge, or model weights for factual content; synthesize from sources.
- Never inline raw URLs in page bodies. Always route them through `manage-sources`.
- When creating a new page, use `create-page` rather than duplicating its file template here.
- Keep page metadata valid so `create-index`, `manage-tags`, and `update-backlinks` can operate correctly.
