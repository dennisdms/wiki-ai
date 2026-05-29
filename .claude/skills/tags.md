# tags

Maintains tag consistency across all notes in `notes/`.

## When to invoke

- After creating or updating a note — validate its tags (called by `research`)
- Standalone audit of the full tag taxonomy
- When renaming or merging tags across the wiki

## Inputs

- `validate <note-path>` — check tags on a specific note against existing taxonomy
- `audit` — list all tags in use, grouped by frequency
- `rename <old-tag> <new-tag>` — rename a tag across all notes
- `merge <tag-a> <tag-b> <canonical>` — consolidate two tags into one canonical form

## Tag rules

- Tags are lowercase kebab-case: `game-mechanics`, `world-building`, `npcs`.
- Each note should have 1–5 tags. Fewer than 1 or more than 5 is a smell.
- Tags represent stable cross-cutting categories — not one-off descriptors or note-specific details.
- Prefer reusing an existing tag over inventing a new one.
- Never use a tag that duplicates the folder the note already lives in (e.g. a note in `game-mechanics/` should not carry the tag `game-mechanics`).

## Steps — validate

1. Read the note's `tags` frontmatter field.
2. Collect all tags currently in use: grep for `^tags:` in all `.md` files under `notes/`.
3. For each tag on the note:
   - Matches an existing tag exactly → OK.
   - Close to an existing tag (typo, pluralization, spacing) → suggest the canonical form.
   - Brand new tag → confirm with the user before accepting it into the taxonomy.
4. Report any count violations (0 tags, or > 5 tags).

## Steps — audit

1. Grep all `.md` files under `notes/` for `^tags:` frontmatter lines.
2. Parse each tag list and build a frequency map.
3. Output a sorted table: tag → count, grouped alphabetically.
4. Flag tags used only once (candidates for consolidation or removal).

## Steps — rename / merge

1. Find all notes whose frontmatter contains the old tag(s).
2. Update the `tags` list in each note's frontmatter.
3. Report a summary: which files changed, old value → new value.
