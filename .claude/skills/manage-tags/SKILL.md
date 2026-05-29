---
name: manage-tags
description: Keep page tags consistent across `wiki/pages/`. Use after page edits, for taxonomy audits, or when renaming and merging tags across the wiki.
---

# Manage Tags

Maintain tag consistency across all pages in `wiki/pages/`.

## When to invoke

Use this skill after creating or updating a page, for a standalone tag audit, or when renaming or merging tags across the wiki.

## Inputs

- `validate <page-path>` — check tags on a specific page against the existing taxonomy
- `audit` — list all tags in use, grouped by frequency
- `rename <old-tag> <new-tag>` — rename a tag across all pages
- `merge <tag-a> <tag-b> <canonical>` — consolidate two tags into one canonical form

## Tag rules

- Tags are lowercase kebab-case, for example `game-mechanics`, `world-building`, or `npcs`.
- Each page should have 1 to 5 tags.
- Tags represent stable cross-cutting categories, not one-off descriptors.
- Prefer reusing an existing tag over inventing a new one.
- Never use a tag that duplicates the folder the page already lives in.

## Steps — validate

1. Read the page's `tags` frontmatter field.
2. Collect all tags currently in use by searching for `tags:` frontmatter lines in markdown files under `wiki/pages/`.
3. For each tag on the page:
   - Exact match to an existing tag → OK.
   - Close match to an existing tag → suggest the canonical form.
   - Brand new tag → confirm with the user before accepting it into the taxonomy.
4. Report any count violations such as zero tags or more than five tags.

## Steps — audit

1. Search all `.md` files under `wiki/pages/` for `tags:` frontmatter lines.
2. Parse each tag list and build a frequency map.
3. Output a sorted table of tag → count, grouped alphabetically.
4. Flag tags used only once as candidates for consolidation or removal.

## Steps — rename / merge

1. Find all pages whose frontmatter contains the old tag or tags.
2. Update the `tags` list in each page's frontmatter.
3. Report a summary showing which files changed and how the values changed.
