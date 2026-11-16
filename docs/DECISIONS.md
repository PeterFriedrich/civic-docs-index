# Decisions Index

Append-only. **One ROW per locked decision** — when, what, why (including what
was rejected), and a pointer to where the argument lives in full. When a decision
locks, add a row; when one is superseded, strike it (`~~...~~`) or mark it
`SUPERSEDED <date>` in place and add the successor — don't delete history.

**What a row owes you:**

1. ⚠️ **EVERY ROW CARRIES A POINTER TO A DOC** — not only to code. Code moves;
   the argument has to live somewhere prose can hold it.
   `scripts/check_doc_citations.py` checks that every pointer resolves.
2. **The row is a self-contained summary** and may paraphrase the argument.
3. **The pointer is the authority.** When a row and its target disagree, the
   target wins and the row gets fixed.
4. **A row names the test that protects it**, or carries `[unverifiable]`.
   `scripts/check_decisions_log.py` enforces this on the merge gate (and that a
   superseded row is marked where it stands).

| When | Decision | Full reasoning |
|------|----------|----------------|
| 2026-11-16 | Extracted document text lives in the private data repo, cloned at the gitignored `data/raw/private/`. Meeting names, attachment titles, DocumentIds and report numbers may appear in tracked files here; they are public on the portal. Rejected: the stricter rule of keeping every name and id out, which was copied from a project whose data is private. [unverifiable] until the guard in `TODO.md` exists. | `docs/SCOPE.md` §"Out of scope" |
| 2026-11-16 | Keep extracted text and a manifest row (sha256, bytes, pages, route, date) per document; do not keep the PDF. Rejected: storing PDFs, for disk. [unverifiable] | `docs/ACQUISITION_TESTS.md` §"Getting files from the laptop to the server" |
| 2026-11-16 | Text files plus manifest are the source of truth; search is a SQLite FTS5 index rebuilt from them and gitignored. Rejected for now: a hosted database, which adds credentials and a network dependency for small text; a free-tier hosted database is to be tested separately (`TODO.md`). [unverifiable] | `docs/SCOPE.md` §"What it does" |
| 2026-11-16 | Acquire per DocumentId during the route tests, then whole agendas for meetings a project needs once sizes are measured. Rejected: per document only, because search cannot find text inside documents nobody asked for. [unverifiable] | `docs/SCOPE.md` §"What it does" |
| 2026-11-16 | The owner approved testing `curl` from the laptop with the default user agent and with a browser user agent (routes A and B), and browses in Firefox. Getting past the challenge from the server stays out of scope. [unverifiable] | `docs/ACQUISITION_TESTS.md` §"Routes" |
