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
`civic-docs-index-data`, the row's status becomes `fetched YYYY-MM-DD` with
the text's path there, and the requester is told.

| DocumentId | Title | Requester | Why | Added | Status |
|---|---|---|---|---|---|
| 164273 | Completed NRP Projects 2009–2022 | `edmonton-tax-viz` | Last unread source for the road reconstruction sub-asset split (its `docs/SPEC_cost_gaps.md` §3.1) | 2026-11-24 | wanted: 403 from a script, re-tested 2026-11-16 |
| 286947 | City Auditor's Neighbourhood Renewal audit | `edmonton-tax-viz` | Same as 164273 | 2026-11-24 | wanted: 403 from a script, re-tested 2026-11-16 |

URLs follow `https://pub-edmonton.escribemeetings.com/filestream.ashx?DocumentId=<id>`.
