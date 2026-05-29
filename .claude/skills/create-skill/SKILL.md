---
name: create-skill
description: Create or update a project skill in `.claude/skills/<name>/SKILL.md` with correct naming, YAML frontmatter, discovery wording, and optional supporting files. Use when making or refining repo-local skills.
---

# Create Skill

Create or update a Claude Code skill for this repo, choosing the right scope, naming, structure, and discovery wording so the skill is easy to find and works reliably.

## When to invoke

Use this skill when:
- The user wants to create a new skill.
- The user wants to rewrite, rename, or improve an existing skill.
- The user has a prompt or workflow that should become a reusable skill.
- A skill is not being discovered and needs troubleshooting.
- The user wants help deciding whether a skill should be personal or project-local.

## Inputs

- The capability the skill should provide
- When the skill should be used
- Any required tools, files, scripts, or dependencies
- Whether the skill is for personal use or should live in the project and be shared
- Any example prompts, existing instructions, or workflows to convert

## Steps

### 1. Determine scope

Start by making the skill narrow and concrete.

Ask or infer:
- What specific capability should this skill provide?
- When should Claude use it?
- What files, tools, or resources does it need?
- Is it a personal workflow or a shared project skill?

Keep one skill focused on one job.

Good scopes:
- `pdf-form-filling`
- `excel-analysis`
- `api-review`

Too broad:
- `document-tools`
- `data-workflows`
- `project-helper`

If the requested scope is too broad, narrow it before writing files.

### 2. Choose the right location

Pick the location that matches the user's intent.

- Personal skill: `~/.claude/skills/`
  - Use for individual workflows, experiments, or private preferences.
- Project skill: `.claude/skills/`
  - Use for team workflows, repo-specific expertise, or anything that should be committed.

If the user does not specify, prefer project-local when the skill is specific to the current repository. Prefer personal when it is a reusable workflow that is not tied to this repo.

### 3. Choose a valid name

The skill name must be:
- Lowercase
- Hyphen-separated
- Focused and descriptive
- No more than 64 characters

Good:
- `pdf-processor`
- `git-commit-helper`
- `api-designer`

Bad:
- `PDF_Processor`
- `Git Commits`
- `my-super-general-helper-skill-for-everything`

When using the directory-based skill format, the directory name must match the frontmatter `name` exactly.

### 4. Create the structure

Use the smallest structure that fits the job.

Single-file skill:

```text
.claude/skills/skill-name/
└── SKILL.md
```

Multi-file skill:

```text
.claude/skills/skill-name/
├── SKILL.md
├── reference.md
├── examples.md
├── scripts/
│   └── helper.py
└── templates/
    └── template.txt
```

Only add supporting files when they materially improve clarity, reuse, or validation.

### 5. Write the frontmatter

Every `SKILL.md` must begin with valid YAML frontmatter.

```yaml
---
name: skill-name
description: Brief description of what this does and when to use it.
---
```

Required fields:
- `name`
  - lowercase letters, numbers, and hyphens only
  - must match the containing directory name
  - max 64 characters
- `description`
  - max 1024 characters
  - must state what the skill does and when to use it
  - should include trigger words users are likely to say

Optional fields:
- `allowed-tools`
  - use for read-only or restricted workflows
  - example: `allowed-tools: Read, Grep, Glob`

Frontmatter rules:
- Opening `---` must be the first line.
- Closing `---` must appear before the body.
- Use valid YAML with spaces, never tabs.

### 6. Write a strong description

The description is the main discovery signal. Make it specific.

Use this formula:
- what it does
- when to use it
- trigger words, file types, or operations the user will mention

Good examples:

```yaml
description: Extract text and tables from PDF files, fill forms, and merge documents. Use when working with PDFs, forms, or document extraction.
```

```yaml
description: Analyze Excel spreadsheets, create pivot tables, and generate charts. Use when working with Excel files, spreadsheets, or .xlsx data analysis.
```

Bad examples:

```yaml
description: Helps with documents
```

```yaml
description: For data analysis
```

Include concrete triggers such as:
- file extensions like `.pdf`, `.xlsx`, `.json`
- verbs like `analyze`, `extract`, `generate`, `transform`
- contextual phrases like `Use when...` or `For...`

### 7. Structure the body clearly

Write the body for Claude, not for humans browsing documentation.

Use clear sections like:

```markdown
# Skill Name
Brief overview of what this skill does.

## Quick start
A minimal example that shows immediate use.

## Instructions
1. First action
2. Second action
3. Handle edge cases

## Examples
Concrete prompts, commands, or file examples.

## Best practices
- Conventions to follow
- Pitfalls to avoid
- When to use vs. not use

## Requirements
Any dependencies or setup steps
```

The instructions should be step-by-step, concrete, and operational.

### 8. Add supporting files only when useful

Use extra files for progressive disclosure.

- `reference.md` for detailed options, APIs, or edge cases
- `examples.md` for extended examples
- `scripts/` for helper scripts
- `templates/` for reusable file templates

Reference them directly from `SKILL.md` with relative paths.

### 9. Validate before finishing

Check all of the following:
- `SKILL.md` exists in the intended location.
- The directory name matches the frontmatter `name`.
- YAML frontmatter opens and closes correctly.
- `name` follows the naming rules.
- `description` is specific and under 1024 characters.
