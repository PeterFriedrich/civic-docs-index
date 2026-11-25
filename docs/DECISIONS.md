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
| 2026-11-16 | SUPERSEDED 2026-11-24. Keep extracted text and a manifest row (sha256, bytes, pages, route, date) per document; do not keep the PDF. Rejected: storing PDFs, for disk. [unverifiable] | `docs/ACQUISITION_TESTS.md` §"Where text and PDFs live" |
| 2026-11-16 | Text files plus manifest are the source of truth; search is a SQLite FTS5 index rebuilt from them and gitignored. Rejected for now: a hosted database, which adds credentials and a network dependency for small text; a free-tier hosted database is to be tested separately (`TODO.md`). [unverifiable] | `docs/SCOPE.md` §"What it does" |
| 2026-11-16 | Acquire per DocumentId during the route tests, then whole agendas for meetings a project needs once sizes are measured. Rejected: per document only, because search cannot find text inside documents nobody asked for. [unverifiable] | `docs/SCOPE.md` §"What it does" |
| 2026-11-16 | The owner approved testing `curl` from the laptop with the default user agent and with a browser user agent (routes A and B), and browses in Firefox. Getting past the challenge from the server stays out of scope. [unverifiable] | `docs/ACQUISITION_TESTS.md` §"Routes" |
| 2026-11-24 | Supersedes the 2026-11-16 do-not-keep-the-PDF row. Fetch and extract on the owner's laptop with `src/ingest_pdf.py`: text (`text/<id>.txt`) and a manifest row go to the private repo; the PDF is kept as `pdfs/<id>.pdf`, gitignored there, for re-extraction without re-fetching. A changed file under a known id is refused, a scan is recorded with `scanned=1`. The server crawls and serves, and gets text by `git pull`. Why: PDFs only reach the laptop (browser route), the laptop has the disk, the server is tighter; persistence comes from GitHub. Rejected: shipping PDFs to the server to extract there; committing PDFs (several GB at council scale). Cost: PDFs have no backup off the laptop. Guards: `test_text_pdf_keeps_pdf_writes_text_and_row`, `test_same_id_different_file_refused`, `test_scan_is_recorded_not_dropped`. | `docs/ACQUISITION_TESTS.md` §"Where text and PDFs live" |
| 2026-11-25 | Requesters of a `docs/WANTED.md` document are told it is fetched by `SendMessage` only; the status records `told <date>` or `not yet told`. Why: the least intrusive channel. Rejected for now: a GitHub issue in the requester's repo (emails the owner) and a pull-side `TODO.md` item in the requester's repo. An MCP over a request database this project owns is a later option (`TODO.md`). [unverifiable] | `docs/WANTED.md` §"When one is fetched" |
