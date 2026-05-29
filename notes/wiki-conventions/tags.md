---
title: Tags
description: How to use and maintain the tag taxonomy across content notes.
tags: [wiki-conventions]
created: 2026-05-28
updated: 2026-05-28
---

# Tags

Tags are cross-cutting categories in note frontmatter. They complement the folder hierarchy by grouping notes that belong together conceptually but live in different directories.

## Format

```yaml
---
tags: [game-mechanics, combat, systems-design]
---
```

- Always lowercase kebab-case: `game-mechanics`, not `Game Mechanics` or `gameMechanics`
- A YAML list, even for a single tag: `tags: [single-tag]`
- 1–5 tags per note. More than 5 is a smell.

## What makes a good tag

Good tags are **stable** and **reusable** — they describe a category that will apply to many notes over time. Bad tags are one-off descriptors that only fit one note.

| Good | Bad |
|---|---|
| `combat` | `combat-system-first-pass` |
| `npcs` | `npc-merchant-dialogue` |
| `world-building` | `notes-from-session-3` |

## When to reuse vs. create

Before adding a new tag, run `/tags audit` to see what's already in use. Prefer an existing tag over a near-synonym. If you do introduce a new tag, the `tags` skill will ask for confirmation.

## Tags and folder hierarchy

Never tag a note with its own directory name. If a note lives in `notes/game-mechanics/`, the tag `game-mechanics` is redundant — the folder already expresses that membership. Tags are for cross-cutting concerns that the hierarchy can't express.

## Maintaining tags

The `tags` skill handles:

- **Validate** — check a note's tags against the existing taxonomy after each edit
- **Audit** — list all tags with frequency counts; surface singletons for review
- **Rename** — rename a tag across every note at once
- **Merge** — consolidate two overlapping tags into one canonical form

## Backlinks

<!-- Auto-maintained by backlinks skill -->
<!-- No backlinks yet -->
