# SCOPE — what this project deliberately does not do

The one hand-kept input to the Claude web brief (`scripts/make_brief.py`, setup
in `docs/CLAUDE_WEB.md`). Everything else in the brief is generated from files
the repo already maintains; this is the list an outside reviewer can't derive —
ideas that were considered and turned down, so they stop coming back as
recommendations.

One bullet each: **the thing**, then why not, and a pointer if a decision row
or doc holds the argument. A turned-down idea that has a locked decision needs
no bullet here — the brief already carries `docs/DECISIONS.md`.

## What it does (proposed 2026-11-16, not locked)

Evidence and probe results: `docs/ACQUISITION_TESTS.md`. Nothing below is a
locked decision until it has a row in `docs/DECISIONS.md`.

1. **Catalogue**, crawled on the server from the portal's open endpoints
   (calendar JSON, agenda HTML, minutes HTML): meetings from 2012 on, agenda
   items, attachment file names, DocumentIds, report numbers, minutes text.
2. **Attachment text on request.** A session asks for a DocumentId; the PDF is
   acquired off the server by whichever route `docs/ACQUISITION_TESTS.md`
   picks, text is extracted per page, and the text plus a manifest row (sha256,
   bytes, pages, route, date) is committed to the private data repo.
3. **Search**: SQLite FTS5 over the catalogue and extracted text, plus exact
   lookup by DocumentId and report number. The index is derived and gitignored.
4. **A JSON command line** other sessions call from their own repo. A hit
   carries DocumentId, meeting, item, page and a passage. A DocumentId whose
   text has not been acquired is reported as such, never left out.

## Out of scope

- **Getting past the Cloudflare challenge on PDFs from the server** (challenge
  solvers, fingerprint spoofing, proxies or other exit IPs). The owner has not
  asked for it; PDFs are acquired off the server. `docs/ACQUISITION_TESTS.md`.
- **Mirroring every attachment.** Text is acquired for the documents sessions
  ask for. PDF and text sizes are unmeasured, and the server disk is small.
- **Publishing document text or PDFs.** This repo holds code and made-up
  fixtures; extracted text lives in the private data repo.
- **Embeddings or semantic search first.** Keyword search and ID lookup answer
  the known questions; embedding is slow on this server. Revisit after FTS5 is
  in use.
- **Answering questions or summarising.** The index returns passages with
  their source; the calling session reads them.
- **A web page or hosted service.** The callers are sessions on this server.
- **OCR and structured table extraction, for now.** The scanned share is
  unmeasured; decide after the first test batch.
- **Other portals and non-council documents, for now.** Edmonton's council
  portal first; nothing else until that is in use.
