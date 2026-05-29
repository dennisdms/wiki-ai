---
name: manage-sources
description: Maintain `wiki/sources/bibliography.md` as the wiki's source registry. Use when adding, finding, auditing, or removing source entries and when converting raw URLs into bibliography citations.
---

# Manage Sources

Maintain `wiki/sources/bibliography.md`, the only place raw URLs live in the wiki.

## When to invoke

Use this skill when the user provides a URL, asks whether a source already exists, wants to audit bibliography quality, or needs to remove a source entry.

Supported operations:
- `add <url>` — add a new source; called by `research-topic` when the user provides a URL.
- `find <url-or-title>` — check whether a source already exists and return its slug.
- `audit` — list all entries and flag problems such as duplicates, missing fields, or bad slugs.
- `remove <slug>` — remove an entry and report all pages that cite it.

## Rules

- The slug is lowercase kebab-case derived from the title, for example `game-feel`.
- Slugs must be unique within the file.
- Pages cite entries as `[[bibliography#slug]]`, never as raw URLs.
- `wiki/sources/bibliography.md` is the only file this skill ever writes.

## Steps — add

1. Search `wiki/sources/bibliography.md` for the URL string. If found, return the existing slug and do not create a duplicate entry.
2. Derive a slug from the title: lowercase, kebab-case, punctuation removed.
3. If the derived slug already exists for a different source, append a short disambiguator such as `game-feel-2`.
4. Require a one-sentence summary. If the user has not provided one, ask for it before writing. A blank summary is not allowed.
5. Set **Accessed** to today's date.
6. Append the new entry at the end of `wiki/sources/bibliography.md`.
7. Return the slug so the caller can embed `[[bibliography#slug]]` in the page body.

## Steps — find

1. Search for the URL or title string in `wiki/sources/bibliography.md`.
2. Return the slug of the matching entry, or report that no match was found.

## Steps — audit

1. Parse all H2 headings as slugs.
2. Flag each of the following:
   - Duplicate URLs under different slugs
   - Entries missing any required field
   - Blank summaries
   - Slugs that are not lowercase kebab-case
3. Output a grouped report with one section per issue type.

## Steps — remove

1. Remove the H2 block for the given slug from `wiki/sources/bibliography.md`.
2. Search all `.md` files in `wiki/pages/` and `wiki/reports/` for `[[bibliography#<slug>]]`.
3. List every file that contains a reference. Do not auto-edit those files.

## Requirements

Every bibliography entry must contain all four required fields:
- Title
- URL
- Accessed
- Summary

Summaries must be substantive and not just a restatement of the title.
