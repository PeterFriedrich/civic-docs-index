# Wanted documents

Council documents other sessions need but can't fetch themselves, because every
attachment request from this box gets a `403` Cloudflare challenge
(`docs/ACQUISITION_TESTS.md`). These are the real targets for the acquisition
route tests, each with a requester and a reason.

**To add one:** send the `civic-docs-index` session a message with the URL or
DocumentId, the title, the requesting project, and why it's needed. This
session owns the file and makes the edit. Titles and DocumentIds are allowed
here; document text is not (`docs/DECISIONS.md`, 2026-11-16).

**When one is fetched:** its extracted text goes to the private repo
`civic-docs-index-data` (`src/ingest_pdf.py`), the row's status becomes `fetched YYYY-MM-DD` with
the text's path there, and the requester is told by `SendMessage` (no GitHub issue,
no item in its `TODO.md`). If the requester isn't live in `ListAgents`, the status
says `not yet told` until it is. Add `told YYYY-MM-DD` to the status once sent.

The status says what text came out, not only that the PDF arrived:
- `fetched YYYY-MM-DD`: full text, in the private repo at the path given.
- `fetched YYYY-MM-DD, no text (scan)`: the PDF is a scan (`manifest.csv`
  `scanned=1`); there is no OCR. Name any substitute document with text.
- `fetched YYYY-MM-DD, partial: <what's missing>`: text came out but isn't the
  whole thing the requester asked for (e.g. a cover report without its attachment).

The message to the requester names anything missing and any substitute used.

| DocumentId | Title | Requester | Why | Added | Status |
|---|---|---|---|---|---|
| 164273 | Completed NRP Projects 2009–2022 | `edmonton-tax-viz` | Last unread source for the road reconstruction sub-asset split (its `docs/SPEC_cost_gaps.md` §3.1) | 2026-11-24 | fetched 2026-11-24, `text/164273.txt`; told 2026-11-25 |
| 286947 | City Auditor's Neighbourhood Renewal audit | `edmonton-tax-viz` | Same as 164273 | 2026-11-24 | fetched 2026-11-24, partial: cover report only, `text/286947.txt` (2 pages, ends "ATTACHMENT 1"; the audit is 286336); told 2026-11-25 |
| 295439 | Signed Bylaw 21442, 2026 Property Tax and Supplementary Property Tax Bylaw (published 2026-04-29). Item 8.1, City Council 2026-04-28; report FCS03408 is 295436 and the unsigned bylaw is 295437 | `edmonton-tax-viz` | Blind check of the 2026 mill rates against the primary document, not the `pwis-wc4c` dataset | 2026-11-24 | fetched 2026-11-24, no text (scan). Use `text/295437.txt`, the unsigned bylaw, which passed all three readings unamended per the 04-28 minutes; cite 295439; told 2026-11-25 |
| 286336 | Attachment 1 - OCA03356 - Neighbourhood Renewal Program Audit (the audit itself; 286947 is its cover). Audit Committee 2026-02-04, meeting `03800f25-e306-4f24-86ab-7873f79f9b24`, where the cover report is listed as 286335; the meeting that carries 286947 is not located | `edmonton-tax-viz` | Same as 164273 | 2026-11-25 | wanted |

URLs follow `https://pub-edmonton.escribemeetings.com/filestream.ashx?DocumentId=<id>`.
