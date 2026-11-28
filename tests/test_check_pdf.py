"""src/check_pdf.py: the one check every acquisition route's output goes through.

Fixtures are made up; no council document text is in this repo.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import check_pdf  # noqa: E402


# Real text pages carry hundreds of bytes; a bare "alpha" page would count as thin (scan-like).
FILLER = " and the remaining body text of this made-up page, which runs on for well over the hundred bytes that a text page needs"


def make_pdf(pages: list[str], pad: bool = True) -> bytes:
    """A minimal text-layer PDF, one string per page ('' gives a page with no text).

    pad appends FILLER to each non-empty page so it is a text page, not a thin one.
    """
    pages = [t + FILLER if t and pad else t for t in pages]
    n = len(pages)
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Count %d /Kids [%s] >>" % (n, b" ".join(b"%d 0 R" % (4 + 2 * i) for i in range(n))),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    for i, text in enumerate(pages):
        stream = b"BT /F1 12 Tf 72 720 Td (%s) Tj ET" % text.encode() if text else b""
        objs.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>" % (5 + 2 * i)
        )
        objs.append(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream))
    out, offsets = b"%PDF-1.4\n", []
    for k, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n%s\nendobj\n" % (k, body)
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    return out


def write(tmp_path, data: bytes, name="doc.pdf") -> Path:
    p = tmp_path / name
    p.write_bytes(data)
    return p


def test_challenge_page_saved_as_pdf_fails(tmp_path):
    html = b"<!doctype html><html><head><title>Verifying your browser</title></head></html>"
    r = check_pdf.check(write(tmp_path, html))
    assert r["status"] == "fail"
    assert "Cloudflare challenge" in r["failures"][0]
    assert check_pdf.main([str(tmp_path / "doc.pdf")]) == 1


def test_text_pdf_is_ok_and_measured(tmp_path, capsys):
    p = write(tmp_path, make_pdf(["Widgets 12,345", "Total 67.8M"]))
    assert check_pdf.main([str(p)]) == 0
    r = json.loads(capsys.readouterr().out)
    assert r["status"] == "ok" and r["pages"] == 2
    assert all(b > 0 for b in r["text_bytes_per_page"])
    assert len(r["sha256"]) == 64 and r["bytes"] == p.stat().st_size


def test_known_answer_passes_and_an_altered_figure_fails(tmp_path):
    p = write(tmp_path, make_pdf(["Widgets 12,345", "Total 67.8M"]))
    assert check_pdf.check(p, {"1": ["12,345"], "2": ["67.8"]})["status"] == "ok"
    r = check_pdf.check(p, {"1": ["12,346"], "2": ["67.8"]})
    assert r["status"] == "fail" and "12,346" in r["failures"][0]


def test_figure_on_the_wrong_page_fails_and_says_where(tmp_path):
    p = write(tmp_path, make_pdf(["Widgets 12,345", "Total 67.8M"]))
    r = check_pdf.check(p, {"1": ["67.8"]})
    assert r["status"] == "fail" and "found on p.[2]" in r["failures"][0]


def test_pdf_without_text_is_recorded_as_scanned_not_dropped(tmp_path):
    p = write(tmp_path, make_pdf(["", ""]))
    r = check_pdf.check(p)
    assert r["status"] == "scanned" and r["pages"] == 2
    assert check_pdf.main([str(p)]) == 0


def test_scan_with_a_stamped_header_on_every_page_is_scanned(tmp_path):
    # 9739: 13 scanned pages whose only text is the stamp "Attachment #1 Page N of 13 Report: CR_6544".
    stamps = [f"Attachment #1 Page {i} of 3 Report: CR_0000" for i in range(1, 4)]
    r = check_pdf.check(write(tmp_path, make_pdf(stamps, pad=False)))
    assert r["status"] == "scanned" and r["thin_pages"] == 3 and r["text_bytes"] > 0


def test_a_few_thin_pages_do_not_make_a_text_file_a_scan(tmp_path):
    # Divider and blank pages occur in text files (236515: 10 of 159); half or fewer thin is text.
    r = check_pdf.check(write(tmp_path, make_pdf(["Widgets 12,345", "", "Total 67.8M", ""])))
    assert r["status"] == "ok" and r["thin_pages"] == 2


def test_truncated_pdf_fails(tmp_path):
    r = check_pdf.check(write(tmp_path, b"%PDF-1.4\nnot really"))
    assert r["status"] == "fail" and "unreadable PDF" in r["failures"][0]
