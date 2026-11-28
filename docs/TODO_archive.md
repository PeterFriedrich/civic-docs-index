# TODO — archive of CLOSED items

Closed work moved out of `TODO.md` so the file that is read at the start of **every** session carries only live work. **Nothing here is a to-do.**

`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so the *never redo a closed item without asking* rule still works by grepping there; this file holds the reasoning behind each one.

Items are verbatim as they were closed, newest-moved first in the order they appeared in `TODO.md`. Line numbers and "next up" markers inside them are historical — do not act on them.

---

- [x] **Scan detection misses scans with stamped header text.** `src/check_pdf.py` calls a PDF scanned only when *no* page has text, so 9739 (13 scanned pages, text is only the eSCRIBE stamp "Attachment #1 Page N of 13 Report: CR_6544", 589 bytes, 45 B/page) was ingested as `scanned=0` with a near-empty `text/9739.txt`. `docs/WANTED.md` already calls it a scan. Fix needs a plan (it changes what `scanned` means in the manifest): e.g. a page counts as scanned below some chars-per-page floor, and the file is scanned when most pages are. Done when 9739 re-checks as scanned, with a test, and the manifest row is corrected. **Closed 2026-11-27:** a page under `SCAN_PAGE_BYTES` (100) is thin and a file is a scan when most pages are (`src/check_pdf.py`; tests `test_scan_with_a_stamped_header_on_every_page_is_scanned`, `test_a_few_thin_pages_do_not_make_a_text_file_a_scan`). `python -m src.ingest_pdf --recheck` corrected 9739 to `scanned=1` and deleted its text; no other row changed.

- [x] **Owner runs:** `git pull` in this repo and in `data/raw/private`, on the laptop — the manifest gained a `word_per_line` column 2026-11-25, and an old `src/ingest_pdf.py` would append rows with shifted columns, unnoticed · confirm: `git merge-base --is-ancestor 56e346e HEAD && git -C data/raw/private merge-base --is-ancestor 0db6e97 HEAD` on the laptop · before the downloads below · since 2026-11-25

- [x] **Owner runs:** download each `wanted` row of `docs/WANTED.md` in Firefox on the laptop (286336 first), then `src/ingest_pdf.py` on it — requesters are waiting, and eSCRIBE answers curl with a 403 challenge · confirm: `grep -c '| wanted |$' docs/WANTED.md` prints 0 · 286336 soon (`edmonton-tax-viz` waiting), the rest no deadline · since 2026-11-25
