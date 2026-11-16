# PDF acquisition: route tests (plan, nothing run off the server yet)

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

Not measured anywhere yet: PDF size, extracted text size, share of scanned
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
3. Text extraction gives non-empty text for at least one page, or the file is
   recorded as "scanned, no text layer". Never silently skipped.
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

## Getting files from the laptop to the server

Proposed: the laptop extracts nothing. It pushes PDFs to a folder on the
server over the existing SSH access; the server validates, extracts, commits
text and manifest to the private data repo, and deletes the PDF. The PDF is
not kept: text and sha256 only (owner, 2026-11-16).

## Convention this follows

- Catalogue from the portal's JSON and agenda HTML is what the existing
  eSCRIBE scrapers do (`Scrape_eScribe`; READMEs read, code not read).
- Code public, data in a private repo cloned at the gitignored
  `data/raw/private/`: the `drive-landscape` layout.
- SQLite FTS5 with JSON out: the advice from the one sibling project that has
  built search. Not yet verified here at council scale.
