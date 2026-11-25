# TODO

The source of truth for what's left. Read first every session; update in place.

**Format contract** (`tools/todo_archive.py` depends on it): top-level items are
`- [ ]` / `- [x]` lines directly under `## Open work`; `###` sub-headings may
group them; closed items are moved to `docs/TODO_archive.md` by the tool, which
leaves a one-line stub under `## Done`. An open item can be stale — reproduce the
symptom and re-measure the stated cause before acting on it.

## Open work

- [ ] **Run the acquisition route tests on the laptop** (`docs/ACQUISITION_TESTS.md`): route C (the owner's own browser, Firefox) first, then A and B (approved 2026-11-16). The checker exists (`src/check_pdf.py`). 2026-11-24: A and B blocked (403 challenge); C got 7 of 7, results table in the doc. Left: the owner chooses a route (C now, D for batches?) and it gets a `docs/DECISIONS.md` row; the batch test. Done when a route is chosen.
- [ ] **Guard: no document text in tracked files.** The layout (public code, text in the private repo at `data/raw/private/`) is the owner's decision but has no test yet, so it has no `docs/DECISIONS.md` row. Names, titles and ids are allowed; bodies are not. Done when a test fails on a tracked file under `data/` other than `DATA.md` and `.gitkeep`, and the `docs/DECISIONS.md` row cites it in place of `[unverifiable]`.
- [ ] **Catalogue crawler** (plan first, it is a new module): meetings 2012 on from the calendar endpoint, agenda and minutes HTML, attachment links. Years before 2012 are unprobed. Count check against the calendar's own totals.
- [ ] **Test a free-tier hosted database as a second home for the index** (owner's ask, 2026-11-16). First confirm the Oracle Always Free database exists and its limits; that is from memory, unchecked. Done when the same text is loaded and queried there and the result is compared with on-box SQLite: setup, credentials each caller needs, query time.
- [ ] **Fill `data/DATA.md`** for the portal source when the crawler lands (endpoints, record keys, the report-number prefix change).

## Done
- [x] Owner confirmed the scope and answered the six open questions (2026-11-16); rows in `docs/DECISIONS.md`.
