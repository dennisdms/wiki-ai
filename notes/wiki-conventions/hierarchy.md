---
title: Note Hierarchy
description: Rules for grouping notes into folders and deciding when to create a subdirectory.
tags: [wiki-conventions, organization]
created: 2026-05-28
updated: 2026-05-28
---

# Note Hierarchy

How notes are organized into folders under `notes/`.

## The rule

Notes are grouped by topic. A folder is created when a topic is broad enough to eventually hold three or more sibling notes. A single note never gets its own folder unless it is the clear entry point of a future cluster.

## Depth

Maximum three levels deep:

```
notes/
  <topic>/
    <subtopic>/
      note.md
```

Do not go deeper. If a subtopic keeps growing, consider whether the original topic boundary is drawn correctly.

## Naming

- Directories: lowercase kebab-case (`game-mechanics`, `world-building`)
- Note files: lowercase kebab-case with `.md` extension (`combat-system.md`)
- No spaces, no uppercase, no special characters in either

## Deciding where a note belongs

The `hierarchy` skill automates this decision. The logic is:

1. Is there an existing directory that closely matches the topic? Place the note there.
2. Is the topic clearly a subtopic of an existing directory? Place it inside that directory.
3. Neither? Create a new directory, then immediately document its structure in `_index.md` via the `index` skill.

## Smell check

- A folder with one note → collapse it into the parent unless growth is expected.
- A note covering three or more distinct subtopics → consider splitting it and promoting to a directory.
- Tags that duplicate the folder name → remove the redundant tag (see [[tags]]).

## Backlinks

<!-- Auto-maintained by backlinks skill -->
<!-- No backlinks yet -->
