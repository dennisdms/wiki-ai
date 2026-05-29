# sources

Maintains `wiki/sources/bibliography.md` — the only place raw URLs live in the wiki.

## When to invoke

- `add <url>` — add a new source; called by `research` when the user provides a URL
- `find <url-or-title>` — check whether a source already exists; returns its slug
- `audit` — list all entries and flag problems (duplicates, missing fields, bad slugs)
- `remove <slug>` — remove an entry and report all pages that cite it

- The slug is lowercase kebab-case derived from the title (e.g. "Game Feel" → `game-feel`).
- Slugs must be unique within the file.
- Pages cite entries as `[[bibliography#slug]]` — never as raw URLs.


## Steps — add

1. Search `wiki/sources/bibliography.md` for the URL string. If found, return the existing slug — do not create a duplicate entry.
2. Derive a slug from the title: lowercase, kebab-case, strip punctuation.
3. If the derived slug already exists in the file (different source), append a short disambiguator: `game-feel-2`.
4. Require a one-sentence summary. If the user hasn't provided one, ask for it before writing. A blank summary is not allowed.
5. Set **Accessed** to today's date.
6. Append the new entry at the end of `wiki/sources/bibliography.md`.
7. Return the slug so the caller can embed `[[bibliography#slug]]` in page body.

## Steps — find

1. Search for the URL or title string in `wiki/sources/bibliography.md`.
2. Return the slug of the matching entry, or report that no match was found.

## Steps — audit

1. Parse all H2 headings as slugs.
2. Flag each of the following:
   - Duplicate URLs (same URL under different slugs)
   - Entries missing any of the four required fields
   - Blank summaries
   - Slugs that are not lowercase kebab-case
3. Output a grouped report: one section per issue type.

## Steps — remove

1. Remove the H2 block for the given slug from `wiki/sources/bibliography.md`.
2. Grep all `.md` files in `wiki/pages/` and `wiki/reports/` for `[[bibliography#<slug>]]`.
3. List every file that contains a reference — do not auto-edit those files. The user decides how to handle the orphaned links.

## Rules

- All wiki markdown is AI-maintained end to end; human edits are not protected state and may be overwritten.
- This skill may rewrite or reorder `wiki/sources/bibliography.md` as needed to keep entries consistent and deduplicated.
- `wiki/sources/bibliography.md` is the only file this skill ever writes to.
- Every entry must have all four fields: Title, URL, Accessed, Summary.
- Summaries are required and must be substantive — not just a restatement of the title.
- Never place raw URLs in page bodies; that is exactly what this skill exists to prevent.
