# backlinks

Maintains the `## Backlinks` section at the bottom of every page under `wiki/pages/`.

## When to invoke

- After creating or updating a page (called by `research`)
- After renaming or moving a page (called by `cleanup`)
- As a standalone audit/repair pass across the whole wiki

## How backlinks work

Every page that contains `[[other-page]]` creates a backlink in `other-page.md`. The `## Backlinks` section at the bottom of each page lists every page that links to it. This section is structural — the web server strips it before rendering HTML — so it should never contain narrative content.

## Inputs

- `update <page-path>` — rebuild backlinks for one specific page
- `update-all` — rebuild backlinks for every page in `wiki/pages/`
- `scan <page-path>` — report what this page links to and what links to it, without writing anything

## Steps — update single page

1. Determine the slug of the target page: filename without `.md`.
2. Search all `.md` files under `wiki/pages/` and `wiki/reports/` for `[[<slug>]]` occurrences.
3. Collect the set of matching files as backlink sources (deduplicate, exclude the page itself).
4. Open the target page:
   - If a `## Backlinks` section exists: replace everything from that heading to the end of file.
   - If not: append the section at the end of the file.
5. Write the section:

```markdown
## Backlinks

<!-- Auto-maintained by backlinks skill -->
- [[source-page-one]]
- [[source-page-two]]
```

If no backlinks exist:

```markdown
## Backlinks

<!-- Auto-maintained by backlinks skill -->
<!-- No backlinks yet -->
```

## Steps — update-all

1. Build a full link map: for every `.md` file under `wiki/pages/` and `wiki/reports/`, extract all `[[slug]]` references.
2. Invert the map: for each slug, collect all files that reference it.
3. For every `.md` file in `wiki/pages/`, apply the single-page update logic using the inverted map.
4. Report a summary: N pages updated, N already up-to-date, N with no backlinks.

## Steps — scan

1. Extract all `[[slug]]` references from the target page → these are its outbound links.
2. Search all `.md` files for `[[<target-slug>]]` → these are its inbound links.
3. Print both lists without modifying any files.

## Rules

- `## Backlinks` must always be the last section in the file — nothing may follow it.
- All wiki markdown is AI-maintained end to end; human edits are not protected state and may be overwritten.
- This section will be overwritten on the next run.
- Backlinks from `wiki/reports/` count and must be included.
- `_index.md` files may have backlinks; treat them like any other page.
- Sort backlink entries alphabetically by slug.
