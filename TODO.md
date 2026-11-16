# TODO

The source of truth for what's left. Read first every session; update in place.

**Format contract** (`tools/todo_archive.py` depends on it): top-level items are
`- [ ]` / `- [x]` lines directly under `## Open work`; `###` sub-headings may
group them; closed items are moved to `docs/TODO_archive.md` by the tool, which
leaves a one-line stub under `## Done`. An open item can be stale — reproduce the
symptom and re-measure the stated cause before acting on it.

## Open work

- [ ] **Owner: confirm or change the proposed scope** (`docs/SCOPE.md` §"What it does") and answer the open questions in the PR that added it. Done when the agreed parts have rows in `docs/DECISIONS.md`.
- [ ] **Run the acquisition route tests on the laptop** (`docs/ACQUISITION_TESTS.md`): route C (the owner's own browser) first; routes A and B only with the owner's yes. Needs the checker written and proven red on the saved challenge page first. Done when the results table is in that doc and a route is chosen.
- [ ] **Guard: no document text in tracked files.** The layout (public code, text in the private repo at `data/raw/private/`) is the owner's decision but has no test yet, so it has no `docs/DECISIONS.md` row. Done when a test fails on a tracked file under `data/` other than `DATA.md` and `.gitkeep`, and the row cites it.
- [ ] **Catalogue crawler** (after scope is confirmed; plan first, it is a new module): meetings 2012 on from the calendar endpoint, agenda and minutes HTML, attachment links. Years before 2012 are unprobed. Count check against the calendar's own totals.
- [ ] **Fill `data/DATA.md`** for the portal source when the crawler lands (endpoints, record keys, the report-number prefix change).

## Done
