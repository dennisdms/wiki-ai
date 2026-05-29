---
name: update-backlinks
description: Rebuild or inspect the `## Backlinks` section for wiki pages based on `[[wiki-links]]`. Use after creating, updating, moving, or auditing pages across `wiki/pages/` and `wiki/reports/`.
---

# Update Backlinks

Maintain the `## Backlinks` section at the bottom of every page under `wiki/pages/`.

## When to invoke

Use this skill after creating or updating a page, after renaming or moving a page, or as a standalone backlink audit and repair pass across the wiki.

## How backlinks work

Every page that contains `[[other-page]]` creates a backlink in `other-page.md`. The `## Backlinks` section at the bottom of each page lists every page that links to it. This section is structural, and the web server strips it before rendering HTML, so it should never contain narrative content.

## Inputs

- `update <page-path>` — rebuild backlinks for one specific page
- `update-all` — rebuild backlinks for every page in `wiki/pages/`
- `scan <page-path>` — report what a page links to and what links to it without writing anything

## Steps — update single page

1. Determine the slug of the target page from its filename without `.md`.
2. Search all `.md` files under `wiki/pages/` and `wiki/reports/` for `[[<slug>]]` occurrences.
3. Collect matching files as backlink sources, deduplicated and excluding the page itself.
4. Open the target page.
   - If a `## Backlinks` section exists, replace everything from that heading to the end of the file.
   - If not, append the section at the end of the file.
5. Write the section as:

```markdown
## Backlinks

<!-- Auto-maintained by update-backlinks skill -->
- [[source-page-one]]
- [[source-page-two]]
```

If no backlinks exist, write:

```markdown
## Backlinks

<!-- Auto-maintained by update-backlinks skill -->
<!-- No backlinks yet -->
```

## Steps — update-all

1. Build a full link map by extracting all `[[slug]]` references from `.md` files under `wiki/pages/` and `wiki/reports/`.
2. Invert the map so each slug points to the files that reference it.
3. For every `.md` file in `wiki/pages/`, apply the single-page update logic using the inverted map.
4. Report a summary: number updated, already up to date, and with no backlinks.

## Steps — scan

1. Extract all `[[slug]]` references from the target page. These are its outbound links.
2. Search all `.md` files for `[[<target-slug>]]`. These are its inbound links.
3. Print both lists without modifying files.

## Rules

- `## Backlinks` must always be the last section in the file.
- Backlinks from `wiki/reports/` count and must be included.
- `_index.md` files may have backlinks and should be treated like any other page.
- Sort backlink entries alphabetically by slug.
- This section is auto-maintained and may be overwritten on the next run.
