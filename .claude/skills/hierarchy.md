# hierarchy

Decides where a note belongs in the `notes/` folder hierarchy and, if needed, creates a new subdirectory.

## When to invoke

- Before creating a new note (called by `research`)
- When reorganizing existing notes
- When a single note grows too broad and should be split into a cluster

## Inputs

- Topic name or note title
- Optional: existing file path if reorganizing

## Steps

1. **Survey the structure** — list all directories under `notes/` and read each directory's `_index.md` title.
2. **Match the topic** — find the best-fit existing directory:
   - Exact or close semantic match → place the note there.
   - The topic is clearly a subtopic of an existing directory → place it inside that directory.
   - No reasonable match → go to step 3.
3. **Create a subdirectory** only when:
   - The topic is broad enough to eventually hold 3 or more sibling notes, OR
   - No existing directory is a plausible parent.
   - Name: lowercase kebab-case derived from the topic (e.g. "Game Mechanics" → `game-mechanics/`).
   - Immediately invoke the `index` skill to create `_index.md` in the new directory.
4. **Confirm the target path** with the caller before writing any files.
5. **Update the parent `_index.md`** — invoke the `index` skill on the parent directory after the note is placed.

## Rules

- Never create a directory for a single note unless that note is a clear entry point for a future cluster.
- Max nesting depth is 3 levels: `notes/<topic>/<subtopic>/note.md`. Do not go deeper.
- A directory with only one child note is a smell — collapse it into the parent unless growth is expected soon.
- Directory names must be lowercase kebab-case (no spaces, no special characters).
- Note filenames must also be lowercase kebab-case with a `.md` extension.
