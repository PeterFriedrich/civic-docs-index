# TODO

The source of truth for what's left. Read first every session; update in place.

**Format contract** (`tools/todo_archive.py` depends on it): top-level items are
`- [ ]` / `- [x]` lines directly under `## Open work`; `###` sub-headings may
group them; closed items are moved to `docs/TODO_archive.md` by the tool, which
leaves a one-line stub under `## Done`. An open item can be stale — reproduce the
symptom and re-measure the stated cause before acting on it.

## Open work

### Waiting on the owner

### Session work
- [ ] **Try OCR on the laptop** (owner, 2026-11-27; `docs/SCOPE.md` lists OCR as out of scope "for now", so this is a trial, not a scope change). Test case: 295439, the signed 2026 tax bylaw (`scanned=1`, PDF kept as `pdfs/295439.pdf`). Its unsigned twin 295437 has text and passed unamended, so it is the answer key: compare the OCR output against `text/295437.txt`. Propose the tool and where it plugs in (a new module or an `src/ingest_pdf.py` option) before building, since a new module needs a plan. Count the scans in the 12-row wanted batch too, so the scope decision has the scanned share. 2026-11-27: 1 of 12 (9739, the OIC 359/2018 attachment, 13 pages) — so far 2 scans in 19 documents. Done when the comparison is written down and the owner decides whether OCR goes into scope (a `docs/DECISIONS.md` row).

- [ ] **Scan detection misses scans with stamped header text.** `src/check_pdf.py` calls a PDF scanned only when *no* page has text, so 9739 (13 scanned pages, text is only the eSCRIBE stamp "Attachment #1 Page N of 13 Report: CR_6544", 589 bytes, 45 B/page) was ingested as `scanned=0` with a near-empty `text/9739.txt`. `docs/WANTED.md` already calls it a scan. Fix needs a plan (it changes what `scanned` means in the manifest): e.g. a page counts as scanned below some chars-per-page floor, and the file is scanned when most pages are. Done when 9739 re-checks as scanned, with a test, and the manifest row is corrected.
- [ ] **Extracted text has one word per line in 2 of 6 files: 286947 and 295437** (`manifest.csv` `word_per_line=1`; 2026-11-27 batch adds 9778, 78486 and the scan 9739). Each word is followed by a space-only line, so phrase search fails; the words and their order are intact. 164273 looks similar but is a table, one cell per line, and is fine. The ingest flags it (`src/ingest_pdf.py` `word_per_line`, tests in `tests/test_ingest_pdf.py`, 2026-11-25). The cause is unknown: 9 synthetic PDF layouts all extract cleanly with pypdf 7.1, so diagnose on the laptop with the kept `pdfs/286947.pdf`. Done when both files are re-extracted with `word_per_line=0`.
- [ ] **Run the acquisition route tests on the laptop** (`docs/ACQUISITION_TESTS.md`): route C (the owner's own browser, Firefox) first, then A and B (approved 2026-11-16). The checker exists (`src/check_pdf.py`). 2026-11-24: A and B blocked (403 challenge); C got 7 of 7, results table in the doc. Text for all 7 ingested on the laptop (`src/ingest_pdf.py`, private repo `f7680ea`). Left: the owner chooses a route (C now, D for batches?) and it gets a `docs/DECISIONS.md` row; the batch test. Done when a route is chosen.
- [ ] **Guard: no document text in tracked files.** The layout (public code, text in the private repo at `data/raw/private/`) is the owner's decision but has no test yet, so it has no `docs/DECISIONS.md` row. Names, titles and ids are allowed; bodies are not. Done when a test fails on a tracked file under `data/` other than `DATA.md` and `.gitkeep`, and the `docs/DECISIONS.md` row cites it in place of `[unverifiable]`.
- [ ] **Catalogue crawler** (plan first, it is a new module): meetings 2012 on from the calendar endpoint, agenda and minutes HTML, attachment links. Years before 2012 are unprobed. Count check against the calendar's own totals.
- [ ] **Test a free-tier hosted database as a second home for the index** (owner's ask, 2026-11-16). First confirm the Oracle Always Free database exists and its limits; that is from memory, unchecked. Done when the same text is loaded and queried there and the result is compared with on-box SQLite: setup, credentials each caller needs, query time.
- [ ] **An MCP for requests and status, built with search** (owner idea 2026-11-25; timing decided 2026-11-27, `docs/DECISIONS.md`). Not before search ships. One server: `search`, `request_document`, `request_status`; requests in a table in the SQLite index; `docs/WANTED.md` generated from it. Until then requests stay direct messages. It would be a long-running service like `open-data-search`, so ports and the unit are the `server` session's to arrange. Plan first.
- [ ] **The command line reports scans as `no_text: scan`**, separate from "not acquired" (`manifest.csv` `scanned=1`), so a caller knows the PDF exists but has no text. Add to `docs/SCOPE.md` item 4 when the search plan is written.
- [ ] **Fill `data/DATA.md`** for the portal source when the crawler lands (endpoints, record keys, the report-number prefix change).

## Done

Closed items moved out of `## Open work` live in **`docs/TODO_archive.md`** — one line each below, reasoning there.

- [x] **Owner runs:** — 2026-11-25 · `docs/TODO_archive.md`
- [x] **Owner runs:** — 2026-11-25 · `docs/TODO_archive.md`

- [x] Owner confirmed the scope and answered the six open questions (2026-11-16); rows in `docs/DECISIONS.md`.
