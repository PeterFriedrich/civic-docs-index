# TODO

The source of truth for what's left. Read first every session; update in place.

**Format contract** (`tools/todo_archive.py` depends on it): top-level items are
`- [ ]` / `- [x]` lines directly under `## Open work`; `###` sub-headings may
group them; closed items are moved to `docs/TODO_archive.md` by the tool, which
leaves a one-line stub under `## Done`. An open item can be stale — reproduce the
symptom and re-measure the stated cause before acting on it.

## Open work

### Waiting on the owner

- [ ] **Owner runs:** `git pull` in this repo and in `data/raw/private`, on the laptop — the manifest gained a `word_per_line` column 2026-11-25, and an old `src/ingest_pdf.py` would append rows with shifted columns, unnoticed · confirm: `git merge-base --is-ancestor 56e346e HEAD && git -C data/raw/private merge-base --is-ancestor 0db6e97 HEAD` on the laptop · before the downloads below · since 2026-11-25
- [ ] **Owner runs:** download each `wanted` row of `docs/WANTED.md` in Firefox on the laptop (286336 first), then `src/ingest_pdf.py` on it — requesters are waiting, and eSCRIBE answers curl with a 403 challenge · confirm: `grep -c '| wanted |$' docs/WANTED.md` prints 0 · 286336 soon (`edmonton-tax-viz` waiting), the rest no deadline · since 2026-11-25

### Session work

- [ ] **Extracted text has one word per line in 2 of 6 files: 286947 and 295437** (`manifest.csv` `word_per_line=1`). Each word is followed by a space-only line, so phrase search fails; the words and their order are intact. 164273 looks similar but is a table, one cell per line, and is fine. The ingest flags it (`src/ingest_pdf.py` `word_per_line`, tests in `tests/test_ingest_pdf.py`, 2026-11-25). The cause is unknown: 9 synthetic PDF layouts all extract cleanly with pypdf 7.1, so diagnose on the laptop with the kept `pdfs/286947.pdf`. Done when both files are re-extracted with `word_per_line=0`.
- [ ] **Run the acquisition route tests on the laptop** (`docs/ACQUISITION_TESTS.md`): route C (the owner's own browser, Firefox) first, then A and B (approved 2026-11-16). The checker exists (`src/check_pdf.py`). 2026-11-24: A and B blocked (403 challenge); C got 7 of 7, results table in the doc. Text for all 7 ingested on the laptop (`src/ingest_pdf.py`, private repo `f7680ea`). Left: the owner chooses a route (C now, D for batches?) and it gets a `docs/DECISIONS.md` row; the batch test. Done when a route is chosen.
- [ ] **Guard: no document text in tracked files.** The layout (public code, text in the private repo at `data/raw/private/`) is the owner's decision but has no test yet, so it has no `docs/DECISIONS.md` row. Names, titles and ids are allowed; bodies are not. Done when a test fails on a tracked file under `data/` other than `DATA.md` and `.gitkeep`, and the `docs/DECISIONS.md` row cites it in place of `[unverifiable]`.
- [ ] **Catalogue crawler** (plan first, it is a new module): meetings 2012 on from the calendar endpoint, agenda and minutes HTML, attachment links. Years before 2012 are unprobed. Count check against the calendar's own totals.
- [ ] **Test a free-tier hosted database as a second home for the index** (owner's ask, 2026-11-16). First confirm the Oracle Always Free database exists and its limits; that is from memory, unchecked. Done when the same text is loaded and queried there and the result is compared with on-box SQLite: setup, credentials each caller needs, query time.
- [ ] **An MCP for requests and status, built with search** (owner idea 2026-11-25; timing decided 2026-11-27, `docs/DECISIONS.md`). Not before search ships. One server: `search`, `request_document`, `request_status`; requests in a table in the SQLite index; `docs/WANTED.md` generated from it. Until then requests stay direct messages. It would be a long-running service like `open-data-search`, so ports and the unit are the `server` session's to arrange. Plan first.
- [ ] **The command line reports scans as `no_text: scan`**, separate from "not acquired" (`manifest.csv` `scanned=1`), so a caller knows the PDF exists but has no text. Add to `docs/SCOPE.md` item 4 when the search plan is written.
- [ ] **Fill `data/DATA.md`** for the portal source when the crawler lands (endpoints, record keys, the report-number prefix change).

## Done
- [x] Owner confirmed the scope and answered the six open questions (2026-11-16); rows in `docs/DECISIONS.md`.
