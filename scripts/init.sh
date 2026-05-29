#!/usr/bin/env bash
set -eu

if [ "${1-}" = "" ]; then
  echo "usage: $0 <project-name>" >&2
  exit 1
fi

PROJECT_NAME=$1
TARGET_DIR=$PROJECT_NAME
RAW_BASE="https://raw.githubusercontent.com/dennisdms/wiki-ai/main"

if [ -e "$TARGET_DIR" ]; then
  echo "error: target already exists: $TARGET_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR/.claude/skills" \
  "$TARGET_DIR/notes" \
  "$TARGET_DIR/reports" \
  "$TARGET_DIR/sources/assets" \
  "$TARGET_DIR/scripts/static" \
  "$TARGET_DIR/scripts/templates"

fetch() {
  remote_path=$1
  local_path=$2
  curl -fsSL "$RAW_BASE/$remote_path" -o "$TARGET_DIR/$local_path"
}

fetch "CLAUDE.md" "CLAUDE.md"
fetch "README.md" "README.md"
fetch ".claude/_index.md" ".claude/_index.md"
fetch ".claude/skills/_index.md" ".claude/skills/_index.md"
fetch ".claude/skills/research.md" ".claude/skills/research.md"
fetch ".claude/skills/index.md" ".claude/skills/index.md"
fetch "scripts/main.py" "scripts/main.py"
fetch "scripts/_index.md" "scripts/_index.md"
fetch "scripts/static/style.css" "scripts/static/style.css"
fetch "scripts/static/graph.js" "scripts/static/graph.js"
fetch "scripts/static/_index.md" "scripts/static/_index.md"
fetch "scripts/templates/base.html" "scripts/templates/base.html"
fetch "scripts/templates/note.html" "scripts/templates/note.html"
fetch "scripts/templates/_index.md" "scripts/templates/_index.md"
fetch "sources/_index.md" "sources/_index.md"
fetch "sources/assets/_index.md" "sources/assets/_index.md"

cat > "$TARGET_DIR/_index.md" <<EOF
---
title: $PROJECT_NAME
---

# $PROJECT_NAME

Project home for this wiki.

## Contents

- [[notes/_index]] — Research notes organized by topic.
- [[reports/_index]] — Generated reports synthesized from research notes.
- [[sources/_index]] — External sources: bibliography and raw assets.
EOF

cat > "$TARGET_DIR/notes/_index.md" <<'EOF'
---
title: Notes
path: notes/
---

# Notes

Research notes organized by topic.

## Contents

EOF

cat > "$TARGET_DIR/reports/_index.md" <<'EOF'
---
title: Reports
path: reports/
---

# Reports

Generated reports synthesized from research notes.

## Contents

EOF

cat > "$TARGET_DIR/sources/bibliography.md" <<'EOF'
---
title: Bibliography
---

# Bibliography

All external sources used in this wiki. Notes link here via `[[bibliography#slug]]` — never inline raw URLs in notes.

<!-- Entry format:
## slug
- **Title:** Page or document title
- **URL:** https://example.com
- **Accessed:** YYYY-MM-DD
- **Summary:** One-sentence description of the source.
-->
EOF

cd "$TARGET_DIR"
git init >/dev/null 2>&1
git add .
git commit -m "Initial wiki-ai scaffold" >/dev/null 2>&1 || true

printf '\nCreated %s\n\n' "$PROJECT_NAME"
printf 'Next steps:\n'
printf '  1. Open the folder in Claude Code.\n'
printf '  2. Run: python scripts/main.py\n'
