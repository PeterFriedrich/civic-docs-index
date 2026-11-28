"""Write a local HTML page of the `wanted` rows in docs/WANTED.md and open it in Firefox.

Route C (docs/ACQUISITION_TESTS.md) needs the owner's own browser to fetch each
attachment; clicking links in a page avoids the terminal's double-open.

    python tools/download_page.py [--wanted docs/WANTED.md] [--out output/download_page.html] [--no-open]
"""
import argparse
import html
import subprocess
from pathlib import Path

URL = "https://pub-edmonton.escribemeetings.com/filestream.ashx?DocumentId={}"


def wanted_rows(md: str) -> list[dict]:
    rows = []
    for line in md.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and cells[-1] == "wanted" and cells[0].isdigit():
            rows.append({"id": cells[0], "title": cells[1], "requester": cells[2].strip("`")})
    return rows


def render(rows: list[dict]) -> str:
    items = "\n".join(
        f'<li><a href="{URL.format(r["id"])}" target="_blank">{r["id"]}</a>'
        f' <span class="req">{html.escape(r["requester"])}</span>'
        f'<div class="title">{html.escape(r["title"])}</div></li>'
        for r in rows
    )
    return f"""<!doctype html>
<meta charset="utf-8">
<title>Wanted downloads ({len(rows)})</title>
<style>
  body {{ font: 15px/1.4 system-ui, sans-serif; max-width: 52rem; margin: 2rem auto; padding: 0 1rem; }}
  li {{ margin: 0 0 .9rem; }}
  a {{ font: 600 1.1rem monospace; color: #0645ad; }}
  a:visited {{ color: #999; text-decoration: line-through; }}
  .req {{ font-size: .85rem; color: #666; margin-left: .5rem; }}
  .title {{ font-size: .85rem; color: #333; }}
</style>
<h1>Wanted downloads: {len(rows)}</h1>
<p>Click each once, a few seconds apart. Clicked links grey out. Then tell the session you're done.</p>
<ol>
{items}
</ol>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wanted", default="docs/WANTED.md")
    ap.add_argument("--out", default="output/download_page.html")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    rows = wanted_rows(Path(args.wanted).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(rows), encoding="utf-8")
    print(f"{len(rows)} wanted rows -> {out}")
    if not args.no_open:
        subprocess.Popen(["firefox", out.resolve().as_uri()])


if __name__ == "__main__":
    main()
