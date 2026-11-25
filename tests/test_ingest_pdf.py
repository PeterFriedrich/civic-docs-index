"""src/ingest_pdf.py: check, keep, extract, record. Fixtures are made up."""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import ingest_pdf  # noqa: E402
from tests.test_check_pdf import make_pdf, write  # noqa: E402


def run(tmp_path, data: bytes, doc_id="101", name="doc.pdf"):
    src = write(tmp_path, data, name)
    root = tmp_path / "private"
    rc = ingest_pdf.main([str(src), "--id", doc_id, "--root", str(root), "--obtained", "2026-11-24"])
    return rc, root


def manifest(root):
    with (root / "manifest.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_text_pdf_keeps_pdf_writes_text_and_row(tmp_path):
    rc, root = run(tmp_path, make_pdf(["alpha", "beta"]), name="Some Title, Attachment 1.pdf")
    assert rc == 0
    assert (root / "pdfs" / "101.pdf").read_bytes().startswith(b"%PDF-")
    text = (root / "text" / "101.txt").read_text()
    assert "=== page 1 ===\nalpha" in text and "=== page 2 ===\nbeta" in text
    [row] = manifest(root)
    assert row["title"] == "Some Title, Attachment 1"  # comma survives the CSV
    assert (row["pages"], row["scanned"], row["route"], row["obtained"]) == ("2", "0", "C", "2026-11-24")
    assert row["word_per_line"] == "0"


def test_scan_is_recorded_not_dropped(tmp_path):
    rc, root = run(tmp_path, make_pdf(["", ""]))
    assert rc == 0
    assert not (root / "text" / "101.txt").exists()
    assert (root / "pdfs" / "101.pdf").exists()
    [row] = manifest(root)
    assert (row["scanned"], row["text_bytes"]) == ("1", "0")


def test_challenge_page_refused_and_nothing_written(tmp_path, capsys):
    rc, root = run(tmp_path, b"<!doctype html><title>Verifying your browser</title>")
    assert rc == 1
    assert not root.exists()
    assert "refused" in capsys.readouterr().out


def test_same_id_same_file_is_noop(tmp_path):
    data = make_pdf(["alpha"])
    run(tmp_path, data)
    rc, root = run(tmp_path, data)
    assert rc == 0
    assert len(manifest(root)) == 1


def test_same_id_different_file_refused(tmp_path, capsys):
    run(tmp_path, make_pdf(["alpha"]))
    rc, root = run(tmp_path, make_pdf(["gamma"]))
    assert rc == 1
    assert "sha256 differs" in capsys.readouterr().out
    assert len(manifest(root)) == 1
    assert "alpha" in (root / "text" / "101.txt").read_text()


def test_non_numeric_id_rejected(tmp_path):
    src = write(tmp_path, make_pdf(["alpha"]))
    try:
        ingest_pdf.main([str(src), "--id", "Attachment 1", "--root", str(tmp_path / "p")])
    except SystemExit as e:
        assert e.code == 2
    else:
        raise AssertionError("expected argparse error")


# The shape of text/295437.txt page 1: a space-only line after every word.
WORD_PER_LINE = "THE\n \nCITY\n \nOF\n \nEDMONTON\n \n \nBYLAW\n \n21442\n \n"


def test_word_per_line_text_is_kept_and_flagged(tmp_path, monkeypatch, capsys):
    import pypdf

    monkeypatch.setattr(pypdf.PageObject, "extract_text", lambda self, *a, **k: WORD_PER_LINE)
    rc, root = run(tmp_path, make_pdf(["alpha"]))
    assert rc == 0
    assert '"word_per_line": true' in capsys.readouterr().out
    assert (root / "text" / "101.txt").read_text().startswith("=== page 1 ===\nTHE\n \nCITY")
    [row] = manifest(root)
    assert row["word_per_line"] == "1"


def test_one_cell_per_line_table_is_not_word_per_line():
    # text/164273.txt: a table, one cell per line, no space-only lines.
    assert not ingest_pdf.word_per_line("Highlands\nReconstruction\nHolyrood\nMicrosurfacing\n2015\n")
    assert not ingest_pdf.word_per_line("")


def test_old_manifest_header_refused_nothing_appended(tmp_path, capsys):
    root = tmp_path / "private"
    root.mkdir()
    old = "document_id,title,sha256,bytes,pages,text_bytes,scanned,route,obtained,ingested\n"
    (root / "manifest.csv").write_text(old)
    src = write(tmp_path, make_pdf(["alpha"]))
    rc = ingest_pdf.main([str(src), "--id", "101", "--root", str(root)])
    assert rc == 1
    assert "manifest header" in capsys.readouterr().out
    assert (root / "manifest.csv").read_text() == old
    assert not (root / "text").exists()
