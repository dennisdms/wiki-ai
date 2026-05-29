#!/usr/bin/env bash
set -eu

if [ "${1-}" = "" ]; then
  echo "usage: $0 <project-name>" >&2
  exit 1
fi

PROJECT_NAME=$1
TARGET_DIR=$PROJECT_NAME
RAW_BASE="${WIKI_AI_RAW_BASE:-https://raw.githubusercontent.com/dennisdms/wiki-ai/main}"

if [ -e "$TARGET_DIR" ]; then
  echo "error: target already exists: $TARGET_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR/.claude/skills" \
  "$TARGET_DIR/pages" \
  "$TARGET_DIR/reports" \
  "$TARGET_DIR/sources/assets" \
  "$TARGET_DIR/scripts/server/static" \
  "$TARGET_DIR/scripts/server/templates"

fetch() {
  remote_path=$1
  local_path=$2
  curl -fsSL "$RAW_BASE/$remote_path" -o "$TARGET_DIR/$local_path"
}

fetch "CLAUDE.md" "CLAUDE.md"
fetch "README.md" "README.md"
fetch ".claude/skills/research.md" ".claude/skills/research.md"
fetch ".claude/skills/sources.md" ".claude/skills/sources.md"
fetch ".claude/skills/index.md" ".claude/skills/index.md"
fetch ".claude/skills/backlinks.md" ".claude/skills/backlinks.md"
fetch ".claude/skills/hierarchy.md" ".claude/skills/hierarchy.md"
fetch ".claude/skills/page.md" ".claude/skills/page.md"
fetch ".claude/skills/tags.md" ".claude/skills/tags.md"
fetch "scripts/_index.md" "scripts/_index.md"
fetch "scripts/server/_index.md" "scripts/server/_index.md"
fetch "scripts/server/main.py" "scripts/server/main.py"
fetch "scripts/server/static/style.css" "scripts/server/static/style.css"
fetch "scripts/server/static/graph.js" "scripts/server/static/graph.js"
fetch "scripts/server/static/_index.md" "scripts/server/static/_index.md"
fetch "scripts/server/templates/base.html" "scripts/server/templates/base.html"
fetch "scripts/server/templates/page.html" "scripts/server/templates/page.html"
fetch "scripts/server/templates/_index.md" "scripts/server/templates/_index.md"
fetch "sources/_index.md" "sources/_index.md"
fetch "sources/assets/_index.md" "sources/assets/_index.md"

cat > "$TARGET_DIR/_index.md" <<EOF
---
title: $PROJECT_NAME
---

# $PROJECT_NAME

Project home for this wiki.

## Contents

- [[pages/_index]] — Research pages organized by topic.
- [[reports/_index]] — Generated reports synthesized from research pages.
- [[sources/_index]] — External sources: bibliography and raw assets.
EOF

cat > "$TARGET_DIR/pages/_index.md" <<'EOF'
---
title: Pages
path: pages/
---

# Pages

Research pages organized by topic.

## Contents

EOF

cat > "$TARGET_DIR/reports/_index.md" <<'EOF'
---
title: Reports
path: reports/
---

# Reports

Generated reports synthesized from research pages.

## Contents

EOF

cat > "$TARGET_DIR/sources/bibliography.md" <<'EOF'
---
title: Bibliography
---

# Bibliography

All external sources used in this wiki. Pages link here via `[[bibliography#slug]]` — never inline raw URLs in pages.
EOF

cd "$TARGET_DIR"
git init >/dev/null 2>&1
git add .
git commit -m "Initial wiki-ai scaffold" >/dev/null 2>&1 || true

printf '\nCreated %s\n\n' "$PROJECT_NAME"
printf 'Next steps:\n'
printf '  1. Open the folder in Claude Code.\n'
printf '  2. Run: python3 scripts/server/main.py\n'
