---
name: manage-sources
description: Maintain `wiki/sources/*.md` as the wiki's source registry, with one Markdown file per website. Use when adding, finding, auditing, or removing source entries and when converting raw URLs into source citations.
---

# Manage Sources

Maintain `wiki/sources/*.md`, where each website gets its own Markdown file and raw URLs live only inside those files.

## When to invoke

Use this skill when the user provides a URL, asks whether a source already exists, wants to audit source quality, or needs to remove a source entry.

Supported operations:
- `add <url>` — add a new source entry; called by `research-topic` when the user provides a URL.
- `find <url-or-title>` — check whether a source already exists and return its source reference.
- `audit` — list all entries and flag problems such as duplicates, missing fields, or bad slugs.
- `remove <website#slug>` — remove a source entry and report all pages that cite it.

## Rules

- Store source entries under `wiki/sources/` in one file per website, named `<website>.md`.
- The website filename is the URL hostname in lowercase, with the leading `www.` removed. Example: `https://www.gamedeveloper.com/...` becomes `wiki/sources/gamedeveloper.com.md`.
- Each file may contain multiple source entries from that website.
- Each entry slug is lowercase kebab-case derived from the source title, for example `game-feel`.
- Slugs must be unique within their website file.
- Pages cite entries as `[[sources/<website>#<slug>]]`, never as raw URLs.
- Raw URLs may appear only in `wiki/sources/*.md`.
- This skill only writes files under `wiki/sources/`.

## Steps — add

1. Search all `wiki/sources/*.md` files for the URL string. If found, return the existing source reference and do not create a duplicate entry.
2. Derive the website filename from the URL hostname: lowercase, strip leading `www.`, keep dots.
3. Create `wiki/sources/<website>.md` if it does not exist yet.
4. Derive an entry slug from the title: lowercase, kebab-case, punctuation removed.
5. If that slug already exists in the website file for a different source, append a short disambiguator such as `game-feel-2`.
6. Require a one-sentence summary. If the user has not provided one, ask for it before writing. A blank summary is not allowed.
7. Set **Accessed** to today's date.
8. Append the new H2 entry block to `wiki/sources/<website>.md`.
9. Return the source reference so the caller can embed `[[sources/<website>#<slug>]]` in the page body.

## Steps — find

1. Search all `wiki/sources/*.md` files for the URL or title string.
2. Return the matching source reference in `sources/<website>#<slug>` form, or report that no match was found.

## Steps — audit

1. Parse every `wiki/sources/*.md` file.
2. Flag each of the following:
   - Duplicate URLs across different files or slugs
   - Entries missing any required field
   - Blank summaries
   - Slugs that are not lowercase kebab-case
   - Files whose name does not match their website hostname convention
3. Output a grouped report with one section per issue type.

## Steps — remove

1. Remove the H2 block for the given `website#slug` from `wiki/sources/<website>.md`.
2. Search all `.md` files in `wiki/pages/` and `wiki/reports/` for `[[sources/<website>#<slug>]]`.
3. List every file that contains a reference. Do not auto-edit those files.
4. If the website file has no remaining source entries after removal, delete the file.

## Requirements

Every source entry must contain all four required fields:
- Title
- URL
- Accessed
- Summary

Summaries must be substantive and not just a restatement of the title.
