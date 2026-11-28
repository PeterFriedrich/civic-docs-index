# PDF acquisition: route tests (A, B, C run 2026-11-24)

The council portal serves listings and agenda HTML to the server but answers
every attachment request with a Cloudflare challenge. This plan compares ways
of getting attachment PDFs **off the server, on the owner's laptop**, on the
same documents. It does not try to get past the challenge.

## Measured on the server, 2026-11-16 (plain `curl`, default user agent)

| Request | Result |
|---|---|
| `POST /MeetingsCalendarView.aspx/GetCalendarMeetings`, June 2025 | 200, 21 meetings under key `d` |
| `GET /Meeting.aspx?Id=<guid>&Agenda=Agenda&lang=English` | 200, 216 KB |
| `GET /filestream.ashx?DocumentId=263222` | 403, `cf-mitigated: challenge`, HTML titled "Verifying your browser" |

Measured on the laptop 2026-11-24: see "Results" below. Before that, not
measured anywhere: PDF size, extracted text size, share of scanned
PDFs, and whether any route still works from the laptop (last success was a
single `curl` with a browser user agent on 2026-07-07).

## Documents

- **Known answer: DocumentId 263222.** Figures from two of its pages are
  already transcribed in the `edmonton-tax-viz` repo
  (`docs/FINDINGS_utility_validation.md`). The expected values are kept in the
  private data repo and are not copied into this repo.
- **Four another project is still missing:** 244141, 164273, 286947, 42331.
  They span 2011 to 2024, so they also test old documents.
- **One batch:** the attachments of one full agenda (about 140 links), for
  the routes that claim to handle a batch.

## Routes

| # | Route | Owner's effort per document | Can run unattended |
|---|---|---|---|
| A | `curl` on the laptop, default user agent | none | yes |
| B | `curl` on the laptop, browser user agent (the 2026-07-07 success) | none | yes |
| C | Open the link in the owner's browser; a watcher picks the PDF up from the download folder | one click | no |
| D | A small Firefox extension that downloads the attachment links on an agenda page the owner has open (`downloads.download()`) | one click per agenda | no |
| E | Ask the publisher whether a sanctioned bulk or API route exists | one message | n/a |

Order: C first. It is what the owner already does by hand, it needs no
automated request, and it yields the first real PDFs to measure. Its open
risk is matching a saved file name back to its DocumentId (the browser saves
under the attachment's title, not the id); D is built only if that matching
proves unreliable or the per-document effort is the thing in the way. E costs
one message and runs in parallel.

**A and B were approved for testing by the owner on 2026-11-16**, default
user agent first. The owner's browser is Firefox.

All routes: one request at a time, at least 5 seconds apart, stop at the
first challenge response rather than retrying.

## What counts as a pass

One checker judges every route's output, so routes are compared on the same
terms. For each file:

1. First bytes are `%PDF-`. A challenge page saved under a `.pdf` name is the
   expected failure and must be reported as a failure, not as a document.
2. sha256, byte size and page count are recorded. The same DocumentId must
   give the same sha256 by every route that returns it.
3. Text extraction gives text pages, or the file is recorded as "scanned"
   (since 2026-11-27: most pages under 100 bytes of text, which catches a scan
   with a stamped header on every page; before, only a file with no text at
   all). Never silently skipped.
4. For 263222 only: the extracted text of the two transcribed pages contains
   the transcribed figures.

**The checker is `src/check_pdf.py`**, guarded by `tests/test_check_pdf.py`
(made-up fixtures). It was also run on the 403 challenge body the server got
on 2026-11-16 and failed it on check 1. Check 2's cross-route sha256
comparison is not in it yet; it is done by reading the recorded hashes.

    .venv/bin/python -m src.check_pdf FILE.pdf \
        --expect data/raw/private/known_answers/263222.json

Known answers are document text, so they live in the private data repo
(`known_answers/<DocumentId>.json`: page number to the strings that page must
contain). The 263222 file was written from the `edmonton-tax-viz`
transcription. Whether the deck's printed page numbers equal the PDF's page
positions is untested; if they differ, the failure names the page where each
figure was found.

## What is recorded per route

- Documents attempted, obtained, failed, with the HTTP status or failure seen.
- The owner's clicks and minutes.
- Whether it worked for the oldest document (42331) and for the batch.
- Bytes per PDF and per extracted text, and the scanned count. These size the
  private repo and decide whether OCR is worth scoping.

Results go in this file as a dated table. A route is chosen in
`docs/DECISIONS.md` only after that table exists.

## Results, 2026-11-24 (laptop)

### Routes A and B: blocked

One request each for 263222, 11 s apart, stopped at the first challenge.

| Route | HTTP | Body | `check_pdf` |
|---|---|---|---|
| A, default `curl` user agent | 403, `cf-mitigated: challenge` | 307,601 B HTML | fail, check 1 (challenge page) |
| B, Firefox 133 user agent | 403, `cf-mitigated: challenge` | 307,772 B HTML | fail, check 1 (challenge page) |

The laptop gets the same answer as the server. The 2026-07-07 browser-agent
success no longer reproduces.

### Route C: 7 of 7 obtained

The owner opened each link in Firefox; files saved to `~/Downloads` under
the attachment title. The first link showed the "Verifying your browser"
page, then downloaded. Effort: one click per document; minutes not timed.

| DocumentId | Saved as (title) | Bytes | Pages | Text | sha256 (first 12) |
|---|---|---|---|---|---|
| 263222 | PRESENTATION 7.4 EXT03099 - EPCOR Water Services - 2024 Annual Performance Based Regulation Progress Report | 414,863 | 20 | ok, 11,170 B; known answers pass (see below) | `65d247d8eba6` |
| 295439 | Signed Bylaw 21442 - Published April 29, 2026 | 656,733 | 11 | **scanned, no text layer** (Ricoh copier scan) | `fe21c20e42cc` |
| 295437 | Attachment 1 - FCS03408 - Bylaw 21442 | 232,471 | 11 | ok, 14,724 B | `9fd6b6d61640` |
| 164273 | IIS01330 Neighbourhood Renewal Funds - Attachment 1 - Completed NRP Projects 2009 - 2022 | 55,142 | 10 | ok, 9,970 B | `7d723d8fee9c` |
| 286947 | Report - OCA03356 - Neighbourhood Renewal Program Audit | 98,538 | 2 | ok, 3,079 B | `b4174cbbc31c` |
| 244141 | Memo to Council - Edmonton's Industrial Development Situation - Nov 29, 2024 | 594,004 | 8 | ok, 11,723 B | `50c073427f72` |
| 42331 | Costs and Revenues for New Areas - 2011CF7611 | 249,569 | 17 | ok, 37,915 B | `38f548603f1d` |

- **Oldest document (42331, 2011):** obtained, with a text layer.
- **Scanned:** 1 of 7, the signed bylaw. Signed bylaws are likely scans as a
  class. The unsigned bylaw attached to the report (295437) is the same 11
  pages with a text layer, and the 2026-04-28 minutes show 21442 passed all
  three readings with no amending motion, so its text stands in for the
  scan. Cite the signed copy as the official version.
- **286947 is 2 pages:** possibly the cover report only, with the full audit
  a separate attachment on the same item. Unchecked.
- **Known answers (263222):** the four figures recorded for page 6 are on PDF
  page 7; page 9's are on page 9. A single-page transcription slip, not a
  numbering offset. Corrected in the private repo (`9fea58e`); the check now
  passes.
- **Matching file to DocumentId:** done by title and by which link was
  opened, which works only when the expected title is known. Two files were
  at first missed because they sorted below newer ones. For a batch this is
  the weak point, and it is the case for route D (files saved as
  `<DocumentId>.pdf`).
- **Batch:** not run.
- **Cross-route sha256:** nothing to compare; only route C returned PDFs.

## Where text and PDFs live

Decided 2026-11-24 (owner), replacing the earlier proposal to push PDFs to
the server and extract there. Everything happens on the laptop, where the
browser routes deliver the files and the disk is larger:

    .venv/bin/python -m src.ingest_pdf ~/Downloads/<title>.pdf --id <DocumentId>

`src/ingest_pdf.py` runs `check_pdf`, refuses a failing file with nothing
written, then writes into the private repo (`data/raw/private/`):

- `text/<id>.txt`, one `=== page N ===` block per page (not for a scan);
- a `manifest.csv` row: document_id, title, sha256, bytes, pages,
  text_bytes, scanned, word_per_line, route, obtained, ingested.
  `word_per_line=1` means the text came out with a space-only line after
  every word: kept, but phrase search fails on it until re-extracted. A
  manifest with a different header is refused, not appended to;
- `pdfs/<id>.pdf`, a copy kept for re-extraction (better extraction, OCR)
  without re-fetching. `pdfs/` is gitignored in the private repo: never
  committed, and not backed up off the laptop.

The id is passed by hand because the browser names the file by title. The
same id with the same sha256 is a no-op; with a different sha256 it is
refused. The owner deletes the `~/Downloads` copy after the private repo is
pushed. The server gets the text by `git pull`; it never sees a PDF.

First run 2026-11-24: all 7 route C files, private repo `f7680ea`; the
sha256 values match the results table above.

## Convention this follows

- Catalogue from the portal's JSON and agenda HTML is what the existing
  eSCRIBE scrapers do (`Scrape_eScribe`; READMEs read, code not read).
- Code public, data in a private repo cloned at the gitignored
  `data/raw/private/`: the `drive-landscape` layout.
- SQLite FTS5 with JSON out: the advice from the one sibling project that has
  built search. Not yet verified here at council scale.
