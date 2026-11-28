"""Ingest one acquired PDF into the private data repo: check, keep, extract, record.

    python -m src.ingest_pdf FILE --id DOCUMENT_ID [--title T] [--route C] [--obtained YYYY-MM-DD]
                             [--root data/raw/private]
    python -m src.ingest_pdf --recheck [--root data/raw/private]

Writes, under --root:
  pdfs/<id>.pdf     a copy of the file (gitignored in the private repo; kept for re-extraction)
  text/<id>.txt     extracted text, one "=== page N ===" block per page (not written for a scan)
  manifest.csv      one row per document

The id is passed in because the browser saves under the attachment title, so it
cannot be read from the file name. A file that fails src/check_pdf is refused
and nothing is written. A scanned file still gets its manifest row (scanned=1),
so it is flagged, not dropped. Re-ingesting an id with the same sha256 is a
no-op; with a different sha256 it is refused. Text that came out one word per
line (word_per_line=1) is kept but flagged: phrase search fails on it, and the
fix is a re-extraction from the kept PDF. A manifest whose header is not FIELDS
is refused rather than appended to with misaligned columns.

--recheck re-runs the check and extraction on every kept pdfs/<id>.pdf after a
change to either: it rewrites the derived columns (pages, text_bytes, scanned,
word_per_line) and text/<id>.txt, deleting the text of a row that is now a scan.
Title, route and dates stay. A row with no kept PDF, or whose PDF no longer
matches its sha256, is reported and left as it is. One JSON line per changed or
skipped row.

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

FIELDS = ["document_id", "title", "sha256", "bytes", "pages", "text_bytes", "scanned", "word_per_line", "route", "obtained", "ingested"]

# Space-only lines per line of text: 1.05 and 1.09 on 286947 and 295437, at most 0.15 on the 4 good files.
WORD_PER_LINE_RATIO = 0.5


def word_per_line(text: str) -> bool:
    """True when pypdf put a space-only line between every word (seen 2026-11-25, cause unknown)."""
    lines = text.splitlines()
    spaces = sum(1 for line in lines if line and not line.strip())
    words = sum(1 for line in lines if line.strip())
    return words > 0 and spaces / words >= WORD_PER_LINE_RATIO


def _read_manifest(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _extract(file: Path, doc_id: str, root: Path, result: dict) -> dict:
    """Write or delete text/<id>.txt from a checked file; return the derived manifest columns."""
    scanned = result["status"] != "ok"
    txt = root / "text" / f"{doc_id}.txt"
    wpl = False
    if scanned:
        txt.unlink(missing_ok=True)
    else:
        pages = [p.extract_text() or "" for p in PdfReader(file).pages]
        text = "".join(f"=== page {i} ===\n{t.rstrip()}\n\n" for i, t in enumerate(pages, 1))
        wpl = word_per_line(text)
        txt.parent.mkdir(parents=True, exist_ok=True)
        txt.write_text(text, encoding="utf-8")
    return {"pages": result["pages"], "text_bytes": result["text_bytes"], "scanned": int(scanned), "word_per_line": int(wpl)}


def recheck(root: Path) -> list[dict]:
    manifest = root / "manifest.csv"
    with manifest.open(newline="", encoding="utf-8") as f:
        header = next(csv.reader(f), [])
    if header != FIELDS:
        return [{"status": "refused", "reason": [f"manifest header is {header}, expected {FIELDS}"]}]
    rows, report = _read_manifest(manifest), []
    for row in rows:
        pdf = root / "pdfs" / f"{row['document_id']}.pdf"
        if not pdf.exists():
            report.append({"document_id": row["document_id"], "status": "skipped", "reason": ["no kept PDF"]})
            continue
        result = check(pdf)
        if result["status"] == "fail" or result["sha256"] != row["sha256"]:
            why = result["failures"] or [f"kept PDF sha256 {result['sha256'][:12]} is not the manifest's {row['sha256'][:12]}"]
            report.append({"document_id": row["document_id"], "status": "skipped", "reason": why})
            continue
        new = {k: str(v) for k, v in _extract(pdf, row["document_id"], root, result).items()}
        changed = {k: [row[k], v] for k, v in new.items() if row[k] != v}
        if changed:
            row.update(new)
            report.append({"document_id": row["document_id"], "status": "changed", "changed": changed})
    with manifest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    return report


def ingest(file: Path, doc_id: str, root: Path, title: str, route: str, obtained: str, today: str) -> dict:
    result = check(file)
    if result["status"] == "fail":
        return {"document_id": doc_id, "status": "refused", "reason": result["failures"]}

    manifest = root / "manifest.csv"
    if manifest.exists():
        with manifest.open(newline="", encoding="utf-8") as f:
            header = next(csv.reader(f), [])
        if header != FIELDS:
            return {"document_id": doc_id, "status": "refused", "reason": [f"manifest header is {header}, expected {FIELDS}"]}
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

    (root / "pdfs").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(file, root / "pdfs" / f"{doc_id}.pdf")
    row = {
        "document_id": doc_id,
        "title": title,
        "sha256": result["sha256"],
        "bytes": result["bytes"],
        **_extract(file, doc_id, root, result),
        "route": route,
        "obtained": obtained,
        "ingested": today,
    }
    scanned, wpl = bool(row["scanned"]), bool(row["word_per_line"])
    new = not manifest.exists()
    with manifest.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    return {"document_id": doc_id, "status": "ingested", "scanned": bool(scanned), "word_per_line": wpl, "pages": result["pages"]}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", type=Path, nargs="?")
    ap.add_argument("--id", help="eSCRIBE DocumentId")
    ap.add_argument("--recheck", action="store_true", help="re-check every kept PDF and update its manifest row")
    ap.add_argument("--title", help="attachment title (default: the file name without .pdf)")
    ap.add_argument("--route", default="C", help="acquisition route, docs/ACQUISITION_TESTS.md")
    today = datetime.date.today().isoformat()
    ap.add_argument("--obtained", default=today, help="date the file was downloaded")
    ap.add_argument("--root", type=Path, default=Path("data/raw/private"))
    args = ap.parse_args(argv)
    if args.recheck:
        if args.file or args.id:
            ap.error("--recheck takes no FILE or --id")
        report = recheck(args.root)
        for r in report:
            print(json.dumps(r))
        return 1 if any(r["status"] == "refused" for r in report) else 0
    if not (args.file and args.id):
        ap.error("FILE and --id are required (or use --recheck)")
    if not args.id.isdigit():
        ap.error(f"--id must be a numeric DocumentId, got {args.id!r}")
    out = ingest(args.file, args.id, args.root, args.title or args.file.stem, args.route, args.obtained, today)
    print(json.dumps(out))
    return 1 if out["status"] == "refused" else 0


if __name__ == "__main__":
    sys.exit(main())
