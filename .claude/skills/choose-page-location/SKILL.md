---
name: choose-page-location
description: Choose the best location for a new or reorganized page under `wiki/pages/`. Use before page creation or when deciding whether a topic needs a new subdirectory.
---

# Choose Page Location

Decide where a page belongs in the `wiki/pages/` folder hierarchy and return the recommended path.

## When to invoke

Use this skill before creating a new page, when reorganizing existing pages, or when one page has grown broad enough to split into a cluster.

## Inputs

- Topic name or page title
- Optional existing file path if reorganizing

## Steps

1. Survey the structure.
   - List all directories under `wiki/pages/`.
   - Read each directory's `_index.md` title and context.
2. Match the topic to the best-fit existing directory.
   - Exact or close semantic match → place the page there.
   - Clear subtopic of an existing directory → place it inside that directory.
   - No reasonable match → continue to step 3.
3. Recommend a new subdirectory only when:
   - The topic is broad enough to eventually hold 3 or more sibling pages, or
   - No existing directory is a plausible parent.
   - Use a lowercase kebab-case name derived from the topic.
4. Return the recommended target path and note whether the caller should create a new directory first.
5. Do not create files, directories, or indexes. The caller is responsible for those side effects.

## Rules

- This skill plans only. It does not create directories, pages, or indexes.
- Never recommend a directory for a single page unless it is a clear entry point for a future cluster.
- Max nesting depth is 3 levels: `wiki/pages/<topic>/<subtopic>/page.md`.
- A directory with only one child page is usually a smell. Collapse it into the parent unless growth is expected soon.
- Directory names must be lowercase kebab-case with no spaces or special characters.
- Page filenames must also be lowercase kebab-case with a `.md` extension.
