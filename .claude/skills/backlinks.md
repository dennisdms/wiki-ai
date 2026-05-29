# backlinks

Maintains the `## Backlinks` section at the bottom of every note under `notes/`.

## When to invoke

- After creating or updating a note (called by `research`)
- After renaming or moving a note (called by `cleanup`)
- As a standalone audit/repair pass across the whole wiki

## How backlinks work

Every note that contains `[[other-note]]` creates a backlink in `other-note.md`. The `## Backlinks` section at the bottom of each note lists every note that links to it. This section is structural — the web server strips it before rendering HTML — so it should never contain narrative content.

## Inputs

- `update <note-path>` — rebuild backlinks for one specific note
- `update-all` — rebuild backlinks for every note in `notes/`
- `scan <note-path>` — report what this note links to and what links to it, without writing anything

## Steps — update single note

1. Determine the slug of the target note: filename without `.md`.
2. Search all `.md` files under `notes/` and `reports/` for `[[<slug>]]` occurrences.
3. Collect the set of matching files as backlink sources (deduplicate, exclude the note itself).
4. Open the target note:
   - If a `## Backlinks` section exists: replace everything from that heading to the end of file.
   - If not: append the section at the end of the file.
5. Write the section:

```markdown
## Backlinks

<!-- Auto-maintained by backlinks skill -->
- [[source-note-one]]
- [[source-note-two]]
```

If no backlinks exist:

```markdown
## Backlinks

<!-- Auto-maintained by backlinks skill -->
<!-- No backlinks yet -->
```

## Steps — update-all

1. Build a full link map: for every `.md` file under `notes/` and `reports/`, extract all `[[slug]]` references.
2. Invert the map: for each slug, collect all files that reference it.
3. For every `.md` file in `notes/`, apply the single-note update logic using the inverted map.
4. Report a summary: N notes updated, N already up-to-date, N with no backlinks.

## Steps — scan

1. Extract all `[[slug]]` references from the target note → these are its outbound links.
2. Search all `.md` files for `[[<target-slug>]]` → these are its inbound links.
3. Print both lists without modifying any files.

## Rules

- `## Backlinks` must always be the last section in the file — nothing may follow it.
- All wiki markdown is AI-maintained end to end; human edits are not protected state and may be overwritten.
- This section will be overwritten on the next run.
- Backlinks from `reports/` count and must be included.
- `_index.md` files may have backlinks; treat them like any other note.
- Sort backlink entries alphabetically by slug.
