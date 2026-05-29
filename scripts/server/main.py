from __future__ import annotations

import argparse
import html
import json
import mimetypes
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlparse

SERVER_DIR = Path(__file__).resolve().parent
ROOT = SERVER_DIR.parent.parent
WIKI_ROOT = ROOT / "wiki"
STATIC_DIR = SERVER_DIR / "static"
TEMPLATES_DIR = SERVER_DIR / "templates"
ROOT_SEGMENTS = {"pages", "reports", "sources"}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`[^`]+`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
UNORDERED_LIST_ITEM_RE = re.compile(r"^[-*]\s+(.*)$")
ORDERED_LIST_ITEM_RE = re.compile(r"^\d+\.\s+(.*)$")
BLOCKQUOTE_RE = re.compile(r"^>\s?(.*)$")
HTML_COMMENT_LINE_RE = re.compile(r"^\s*<!--.*?-->\s*$")
TEMPLATE_RE = re.compile(r"{{\s*([a-z_]+)\s*}}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    metadata: dict[str, object] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if inner:
                metadata[key] = [
                    item.strip().strip("\"'")
                    for item in inner.split(",")
                    if item.strip()
                ]
            else:
                metadata[key] = []
        else:
            metadata[key] = value.strip("\"'")

    return metadata, text[match.end() :]


def strip_backlinks(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == "## Backlinks":
            return "\n".join(lines[:index]).rstrip() + "\n"
    return text


def visible_wikilink_source(text: str) -> str:
    lines = strip_backlinks(text).splitlines()
    kept: list[str] = []
    in_code_block = False

    for line in lines:
        stripped = line.rstrip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or HTML_COMMENT_LINE_RE.match(stripped):
            continue
        kept.append(INLINE_CODE_RE.sub("", line))

    return "\n".join(kept)


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").strip().title() or slug


def normalize_relative(path: Path) -> str:
    return path.as_posix().lstrip("./")


def path_to_url(relative_path: Path) -> str:
    posix = normalize_relative(relative_path)
    if posix == "_index.md":
        return "/"
    if relative_path.name == "_index.md":
        parent = relative_path.parent.as_posix()
        return f"/{parent}/" if parent else "/"
    return "/" + relative_path.with_suffix("").as_posix()


def slugify_text(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def parse_wikilink(value: str) -> tuple[str, str | None]:
    if "|" not in value:
        return value.strip(), None
    target, label = value.split("|", 1)
    return target.strip(), label.strip() or None


def url_label(target: str) -> str:
    base, _, fragment = target.partition("#")
    base = base.rstrip("/")
    if fragment and (not base or base == "bibliography"):
        return fragment
    if not base:
        return target
    final_segment = base.split("/")[-1]
    if final_segment == "_index" and "/" in base:
        final_segment = base.split("/")[-2]
    return final_segment or fragment or target


def safe_relative(path: Path, base: Path) -> Path | None:
    try:
        return path.resolve().relative_to(base.resolve())
    except ValueError:
        return None


def repo_candidates_for_target(target: str, current_relative: Path) -> list[Path]:
    link_target, _ = parse_wikilink(target)
    link_target = link_target.split("#", 1)[0].strip()
    if not link_target:
        return []

    if link_target == "bibliography":
        return [Path("sources/bibliography.md")]

    if link_target.startswith("assets/"):
        return []

    raw = PurePosixPath(link_target)
    roots = raw.parts[0:1]
    starts_at_root = bool(roots) and roots[0] in ROOT_SEGMENTS

    bases: list[Path]
    if starts_at_root:
        bases = [Path(*raw.parts)]
    else:
        bases = [current_relative.parent / Path(*raw.parts)]
        if len(raw.parts) == 1:
            bases.extend(
                [
                    Path("pages") / raw.parts[0],
                    Path("reports") / raw.parts[0],
                    Path("sources") / raw.parts[0],
                    Path(".claude") / raw.parts[0],
                ]
            )

    candidates: list[Path] = []
    seen: set[str] = set()
    for base in bases:
        options = []
        if base.suffix:
            options.append(base)
        else:
            options.extend([base.with_suffix(".md"), base / "_index.md"])
            if base.name == "_index":
                options.insert(0, base.with_suffix(".md"))
        for option in options:
            key = normalize_relative(option)
            if key not in seen:
                seen.add(key)
                candidates.append(option)
    return candidates


def resolve_link_path(target: str, current_relative: Path) -> Path | None:
    for candidate in repo_candidates_for_target(target, current_relative):
        absolute = WIKI_ROOT / candidate
        relative = safe_relative(absolute, WIKI_ROOT)
        if relative is not None and absolute.exists() and absolute.is_file():
            return relative
    return None


def render_inline(text: str, current_relative: Path) -> str:
    parts: list[str] = []
    cursor = 0
    for match in WIKILINK_RE.finditer(text):
        parts.append(html.escape(text[cursor : match.start()]))
        raw_target = match.group(1).strip()
        target, alias = parse_wikilink(raw_target)
        resolved = resolve_link_path(target, current_relative)
        label = html.escape(alias or url_label(target))
        if resolved is None:
            parts.append(f'<span class="broken-link">[[{label}]]</span>')
        else:
            href = html.escape(path_to_url(resolved))
            if "#" in target:
                href = f"{href}#{html.escape(target.split('#', 1)[1])}"
            parts.append(f'<a href="{href}" class="wiki-link">{label}</a>')
        cursor = match.end()
    parts.append(html.escape(text[cursor:]))
    rendered = "".join(parts)
    rendered = re.sub(
        r"`([^`]+)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", rendered
    )
    rendered = MARKDOWN_LINK_RE.sub(
        lambda m: (
            f'<a href="{html.escape(m.group(2).strip())}">{html.escape(m.group(1).strip())}</a>'
        ),
        rendered,
    )
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", rendered)
    return rendered


def markdown_to_html(text: str, current_relative: Path) -> str:
    lines = strip_backlinks(text).strip("\n").splitlines()
    if not lines:
        return ""

    blocks: list[str] = []
    paragraph: list[str] = []
    blockquote: list[str] = []
    list_items: list[str] = []
    list_kind: str | None = None
    code_lines: list[str] = []
    in_code_block = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            content = " ".join(line.strip() for line in paragraph)
            blocks.append(f"<p>{render_inline(content, current_relative)}</p>")
            paragraph = []

    def flush_blockquote() -> None:
        nonlocal blockquote
        if blockquote:
            content = " ".join(line.strip() for line in blockquote)
            blocks.append(
                f"<blockquote><p>{render_inline(content, current_relative)}</p></blockquote>"
            )
            blockquote = []

    def flush_list() -> None:
        nonlocal list_items, list_kind
        if list_items and list_kind:
            items = "".join(f"<li>{item}</li>" for item in list_items)
            blocks.append(f"<{list_kind}>{items}</{list_kind}>")
            list_items = []
            list_kind = None

    def flush_code() -> None:
        nonlocal code_lines
        code = "\n".join(code_lines)
        blocks.append(f"<pre><code>{html.escape(code)}</code></pre>")
        code_lines = []

    def flush_open_blocks() -> None:
        flush_paragraph()
        flush_blockquote()
        flush_list()

    for line in lines:
        stripped = line.rstrip()

        if stripped.startswith("```"):
            flush_open_blocks()
            if in_code_block:
                flush_code()
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not stripped:
            flush_open_blocks()
            continue

        if HTML_COMMENT_LINE_RE.match(stripped):
            flush_open_blocks()
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            flush_open_blocks()
            level = len(heading_match.group(1))
            raw_heading = heading_match.group(2).strip()
            content = render_inline(raw_heading, current_relative)
            heading_id = slugify_text(re.sub(r"`([^`]+)`", r"\1", raw_heading))
            blocks.append(f'<h{level} id="{heading_id}">{content}</h{level}>')
            continue

        blockquote_match = BLOCKQUOTE_RE.match(stripped)
        if blockquote_match:
            flush_paragraph()
            flush_list()
            blockquote.append(blockquote_match.group(1))
            continue

        ordered_match = ORDERED_LIST_ITEM_RE.match(stripped)
        if ordered_match:
            flush_paragraph()
            flush_blockquote()
            if list_kind not in (None, "ol"):
                flush_list()
            list_kind = "ol"
            list_items.append(
                render_inline(ordered_match.group(1).strip(), current_relative)
            )
            continue

        unordered_match = UNORDERED_LIST_ITEM_RE.match(stripped)
        if unordered_match:
            flush_paragraph()
            flush_blockquote()
            if list_kind not in (None, "ul"):
                flush_list()
            list_kind = "ul"
            list_items.append(
                render_inline(unordered_match.group(1).strip(), current_relative)
            )
            continue

        paragraph.append(stripped)

    flush_open_blocks()
    if in_code_block:
        flush_code()

    return "\n".join(blocks)


def render_template(name: str, context: dict[str, str]) -> str:
    template = read_text(TEMPLATES_DIR / name)
    return TEMPLATE_RE.sub(lambda match: context.get(match.group(1), ""), template)


def page_meta_html(relative_path: Path, metadata: dict[str, object]) -> str:
    parts = [
        f'<li><span class="meta-key">Path</span><span class="meta-value">{html.escape(relative_path.as_posix())}</span></li>'
    ]
    for key in ("created", "updated"):
        value = metadata.get(key)
        if isinstance(value, str) and value:
            parts.append(
                f'<li><span class="meta-key">{html.escape(key.title())}</span><span class="meta-value">{html.escape(value)}</span></li>'
            )
    tags = metadata.get("tags")
    if isinstance(tags, list) and tags:
        tag_html = "".join(
            f'<span class="tag">{html.escape(tag)}</span>' for tag in tags
        )
        parts.append(
            f'<li><span class="meta-key">Tags</span><span class="meta-value tag-list">{tag_html}</span></li>'
        )
    return f'<ul class="page-meta">{"".join(parts)}</ul>'


def render_markdown_page(relative_path: Path) -> bytes:
    absolute_path = WIKI_ROOT / relative_path
    raw = read_text(absolute_path)
    metadata, body = parse_frontmatter(raw)
    title = str(metadata.get("title") or slug_to_title(relative_path.stem))
    description = str(metadata.get("description") or "")
    page_html = render_template(
        "page.html",
        {
            "meta": page_meta_html(relative_path, metadata),
            "content": markdown_to_html(body, relative_path),
        },
    )
    page = render_template(
        "base.html",
        {
            "title": html.escape(title),
            "description": html.escape(description),
            "body_class": "page-view",
            "content": page_html,
            "scripts": "",
        },
    )
    return page.encode("utf-8")


def resolve_request_to_markdown(request_path: str) -> Path | None:
    raw_path = unquote(urlparse(request_path).path)
    if raw_path == "/":
        candidate = WIKI_ROOT / "_index.md"
        return Path("_index.md") if candidate.exists() else None

    clean = raw_path.lstrip("/")
    if not clean:
        return None

    relative = Path(clean)
    options: list[Path]
    if relative.suffix:
        options = [relative]
    else:
        options = [relative.with_suffix(".md"), relative / "_index.md"]
        if relative.name == "_index":
            options.insert(0, relative.with_suffix(".md"))

    for option in options:
        absolute = WIKI_ROOT / option
        rel = safe_relative(absolute, WIKI_ROOT)
        if (
            rel is not None
            and absolute.exists()
            and absolute.is_file()
            and absolute.suffix == ".md"
        ):
            return rel
    return None


def detect_node_type(relative_path: Path) -> str:
    if relative_path.name == "_index.md":
        return "index"
    if relative_path.parts and relative_path.parts[0] == "reports":
        return "report"
    if relative_path.parts and relative_path.parts[0] == "pages":
        return "page"
    return "other"


def extract_links(relative_path: Path) -> list[str]:
    _, body = parse_frontmatter(read_text(WIKI_ROOT / relative_path))
    return [
        match.group(1).strip()
        for match in WIKILINK_RE.finditer(visible_wikilink_source(body))
    ]


def build_graph() -> dict[str, object]:
    markdown_files = sorted(
        path
        for path in WIKI_ROOT.rglob("*.md")
        if safe_relative(path, WIKI_ROOT) is not None
    )
    nodes: list[dict[str, object]] = []
    links: list[dict[str, object]] = []
    node_index: dict[str, Path] = {}

    for path in markdown_files:
        relative = path.relative_to(WIKI_ROOT)
        metadata, _ = parse_frontmatter(read_text(path))
        node_id = relative.as_posix()
        node_index[node_id] = relative
        nodes.append(
            {
                "id": node_id,
                "label": str(metadata.get("title") or slug_to_title(relative.stem)),
                "type": detect_node_type(relative),
                "url": path_to_url(relative),
            }
        )

    seen_edges: set[tuple[str, str]] = set()
    for node_id, relative in node_index.items():
        for target in extract_links(relative):
            resolved = resolve_link_path(target, relative)
            if resolved is None:
                continue
            edge = (node_id, resolved.as_posix())
            if edge in seen_edges:
                continue
            seen_edges.add(edge)
            links.append({"source": edge[0], "target": edge[1]})

    return {"nodes": nodes, "links": links}


class WikiHandler(BaseHTTPRequestHandler):
    server_version = "wiki-ai/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        route = parsed.path

        if route == "/api/graph":
            self.send_json(build_graph())
            return

        if route == "/graph":
            self.send_html(self.render_graph_page())
            return

        if route.startswith("/static/"):
            self.serve_static(route.removeprefix("/static/"))
            return

        relative_markdown = resolve_request_to_markdown(route)
        if relative_markdown is None:
            self.send_error(404, "Page not found")
            return

        self.send_html(render_markdown_page(relative_markdown))

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_html(self, content: bytes | str) -> None:
        body = content.encode("utf-8") if isinstance(content, str) else content
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: object) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_static(self, relative_name: str) -> None:
        target = STATIC_DIR / relative_name
        if not target.exists() or not target.is_file():
            self.send_error(404, "Static file not found")
            return

        if safe_relative(target, STATIC_DIR) is None:
            self.send_error(403, "Forbidden")
            return

        content = target.read_bytes()
        content_type, _ = mimetypes.guess_type(target.name)
        self.send_response(200)
        self.send_header(
            "Content-Type", f"{content_type or 'application/octet-stream'}"
        )
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def render_graph_page(self) -> bytes:
        content = """
<section class=\"graph-shell\">
  <div class=\"graph-toolbar\">
    <h1>Graph</h1>
    <p>Browse the wiki as a force-directed graph.</p>
  </div>
  <div id=\"graph\" class=\"graph-canvas\"></div>
</section>
""".strip()
        page = render_template(
            "base.html",
            {
                "title": "Graph",
                "description": "Force-directed graph of wiki links.",
                "body_class": "graph-page",
                "content": content,
                "scripts": '<script src="/static/graph.js"></script>',
            },
        )
        return page.encode("utf-8")


def serve(port: int) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), WikiHandler)
    print(f"http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve the wiki-ai browser UI.")
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to listen on (default: 8000)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    serve(parse_args().port)
