"""Judge one acquired file: is it the PDF it claims to be, and what is in it.

Every acquisition route's output goes through this one check so routes are
compared on the same terms (docs/ACQUISITION_TESTS.md). Prints one JSON line.

    python -m src.check_pdf FILE [--expect EXPECT.json]

EXPECT.json maps a 1-based page number to strings that page's text must
contain, e.g. {"6": ["254.9"]}. Known answers are document text, so they live
in the private data repo, not here.

Exit codes: 0 ok or scanned (recorded, not a failure); 1 failed (2 is argparse's).
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def check(path: Path, expect: dict[str, list[str]] | None = None) -> dict:
    data = path.read_bytes()
    out = {
        "file": str(path),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "status": "fail",
        "failures": [],
    }
    if not data.startswith(b"%PDF-"):
        what = "a Cloudflare challenge page" if b"Verifying your browser" in data else repr(data[:20])
        out["failures"].append(f"not a PDF: starts with {what}")
        return out
    try:
        texts = [_squash(p.extract_text() or "") for p in PdfReader(path).pages]
    except Exception as e:  # pypdf raises several unrelated types on a damaged file
        out["failures"].append(f"unreadable PDF: {type(e).__name__}: {e}")
        return out
    out["pages"] = len(texts)
    out["text_bytes_per_page"] = [len(t.encode()) for t in texts]
    out["text_bytes"] = sum(out["text_bytes_per_page"])
    scanned = not any(t.strip() for t in texts)

    for page, wanted in (expect or {}).items():
        i = int(page) - 1
        here = texts[i] if 0 <= i < len(texts) else ""
        for w in wanted:
            if w not in here:
                elsewhere = [n + 1 for n, t in enumerate(texts) if w in t]
                out["failures"].append(
                    f"p.{page}: {w!r} not found" + (f" (found on p.{elsewhere})" if elsewhere else "")
                )
    if not out["failures"]:
        out["status"] = "scanned, no text layer" if scanned else "ok"
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", type=Path)
    ap.add_argument("--expect", type=Path, help="JSON: page number -> strings that page must contain")
    args = ap.parse_args(argv)
    expect = json.loads(args.expect.read_text()) if args.expect else None
    result = check(args.file, expect)
    print(json.dumps(result))
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
