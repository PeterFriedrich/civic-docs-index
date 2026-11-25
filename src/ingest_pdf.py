"""Ingest one acquired PDF into the private data repo: check, keep, extract, record.

    python -m src.ingest_pdf FILE --id DOCUMENT_ID [--title T] [--route C] [--obtained YYYY-MM-DD]
                             [--root data/raw/private]

Writes, under --root:
  pdfs/<id>.pdf     a copy of the file (gitignored in the private repo; kept for re-extraction)
  text/<id>.txt     extracted text, one "=== page N ===" block per page (not written for a scan)
  manifest.csv      one row per document

The id is passed in because the browser saves under the attachment title, so it
cannot be read from the file name. A file that fails src/check_pdf is refused
and nothing is written. A scanned file still gets its manifest row (scanned=1),
so it is flagged, not dropped. Re-ingesting an id with the same sha256 is a
no-op; with a different sha256 it is refused.

Exit codes: 0 ingested or already present; 1 refused (2 is argparse's).
"""
import argparse
import csv
import datetime
import json
import shutil
import sys
from pathlib import Path

from pypdf import PdfReader

from src.check_pdf import check

FIELDS = ["document_id", "title", "sha256", "bytes", "pages", "text_bytes", "scanned", "route", "obtained", "ingested"]


def _read_manifest(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ingest(file: Path, doc_id: str, root: Path, title: str, route: str, obtained: str, today: str) -> dict:
    result = check(file)
    if result["status"] == "fail":
        return {"document_id": doc_id, "status": "refused", "reason": result["failures"]}

    manifest = root / "manifest.csv"
    rows = _read_manifest(manifest)
    prior = [r for r in rows if r["document_id"] == doc_id]
    if prior:
        if prior[0]["sha256"] == result["sha256"]:
            return {"document_id": doc_id, "status": "already ingested"}
        return {
            "document_id": doc_id,
            "status": "refused",
            "reason": [f"sha256 differs from the manifest ({prior[0]['sha256'][:12]} vs {result['sha256'][:12]})"],
        }

    scanned = result["status"] != "ok"
    (root / "pdfs").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(file, root / "pdfs" / f"{doc_id}.pdf")
    if not scanned:
        pages = [p.extract_text() or "" for p in PdfReader(file).pages]
        (root / "text").mkdir(parents=True, exist_ok=True)
        (root / "text" / f"{doc_id}.txt").write_text(
            "".join(f"=== page {i} ===\n{t.rstrip()}\n\n" for i, t in enumerate(pages, 1)), encoding="utf-8"
        )

    row = {
        "document_id": doc_id,
        "title": title,
        "sha256": result["sha256"],
        "bytes": result["bytes"],
        "pages": result["pages"],
        "text_bytes": result["text_bytes"],
        "scanned": int(scanned),
        "route": route,
        "obtained": obtained,
        "ingested": today,
    }
    new = not manifest.exists()
    with manifest.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    return {"document_id": doc_id, "status": "ingested", "scanned": bool(scanned), "pages": result["pages"]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", type=Path)
    ap.add_argument("--id", required=True, help="eSCRIBE DocumentId")
    ap.add_argument("--title", help="attachment title (default: the file name without .pdf)")
    ap.add_argument("--route", default="C", help="acquisition route, docs/ACQUISITION_TESTS.md")
    today = datetime.date.today().isoformat()
    ap.add_argument("--obtained", default=today, help="date the file was downloaded")
    ap.add_argument("--root", type=Path, default=Path("data/raw/private"))
    args = ap.parse_args(argv)
    if not args.id.isdigit():
        ap.error(f"--id must be a numeric DocumentId, got {args.id!r}")
    out = ingest(args.file, args.id, args.root, args.title or args.file.stem, args.route, args.obtained, today)
    print(json.dumps(out))
    return 1 if out["status"] == "refused" else 0


if __name__ == "__main__":
    sys.exit(main())
