# TODO — archive of CLOSED items

Closed work moved out of `TODO.md` so the file that is read at the start of **every** session carries only live work. **Nothing here is a to-do.**

`TODO.md`'s `## Done` section keeps a one-line entry for each of these, so the *never redo a closed item without asking* rule still works by grepping there; this file holds the reasoning behind each one.

Items are verbatim as they were closed, newest-moved first in the order they appeared in `TODO.md`. Line numbers and "next up" markers inside them are historical — do not act on them.

---

- [x] **Owner runs:** `git pull` in this repo and in `data/raw/private`, on the laptop — the manifest gained a `word_per_line` column 2026-11-25, and an old `src/ingest_pdf.py` would append rows with shifted columns, unnoticed · confirm: `git merge-base --is-ancestor 56e346e HEAD && git -C data/raw/private merge-base --is-ancestor 0db6e97 HEAD` on the laptop · before the downloads below · since 2026-11-25

- [x] **Owner runs:** download each `wanted` row of `docs/WANTED.md` in Firefox on the laptop (286336 first), then `src/ingest_pdf.py` on it — requesters are waiting, and eSCRIBE answers curl with a 403 challenge · confirm: `grep -c '| wanted |$' docs/WANTED.md` prints 0 · 286336 soon (`edmonton-tax-viz` waiting), the rest no deadline · since 2026-11-25
