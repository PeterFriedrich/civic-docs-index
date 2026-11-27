# Wanted documents

Council documents other sessions need but can't fetch themselves, because every
attachment request from this box gets a `403` Cloudflare challenge
(`docs/ACQUISITION_TESTS.md`). These are the real targets for the acquisition
route tests, each with a requester and a reason.

**To add one:** send the `civic-docs-index` session a message with the URL or
DocumentId, the title, the requesting project, and why it's needed. This
session owns the file and makes the edit. Titles and DocumentIds are allowed
here; document text is not (`docs/DECISIONS.md`, 2026-11-16).

**Why by message:** decided 2026-11-27. Requests stay direct messages until
search ships. Then one MCP server carries `search`, `request_document` and
`request_status`, with requests in a table in the SQLite index and this file
generated from that table. Why wait: with two requesters and about ten active
rows, intake isn't the bottleneck (the laptop downloads are), and a server for
requests alone would be a running service with almost nothing to do. Rejected:
a request database without the MCP, because other sessions would write into
this project's file directly, unvalidated, which breaks "only the owner edits".
Switch earlier if requests outpace this session or requesters keep asking for
status.

**When one is fetched:** its extracted text goes to the private repo
`civic-docs-index-data` (`src/ingest_pdf.py`), the row's status becomes `fetched YYYY-MM-DD` with
the text's path there, and the requester is told by `SendMessage` (no GitHub issue,
no item in its `TODO.md`). If the requester isn't live in `ListAgents`, the status
says `not yet told` until it is. Add `told YYYY-MM-DD` to the status once sent.

The status says what text came out, not only that the PDF arrived:
- `fetched YYYY-MM-DD`: full text, in the private repo at the path given.
- `fetched YYYY-MM-DD, no text (scan)`: the PDF is a scan (`manifest.csv`
  `scanned=1`); there is no OCR. Name any substitute document with text.
- `wanted`: to fetch at the next laptop session.
- `later`: requested but deferred (the §"Later" table).
- `fetched YYYY-MM-DD, partial: <what's missing>`: text came out but isn't the
  whole thing the requester asked for (e.g. a cover report without its attachment).

The message to the requester names anything missing and any substitute used.

| DocumentId | Title | Requester | Why | Added | Status |
|---|---|---|---|---|---|
| 164273 | Completed NRP Projects 2009–2022 | `edmonton-tax-viz` | Last unread source for the road reconstruction sub-asset split (its `docs/SPEC_cost_gaps.md` §3.1) | 2026-11-24 | fetched 2026-11-24, `text/164273.txt`; told 2026-11-25 |
| 286947 | City Auditor's Neighbourhood Renewal audit | `edmonton-tax-viz` | Same as 164273 | 2026-11-24 | fetched 2026-11-24, partial: cover report only, `text/286947.txt` (2 pages, ends "ATTACHMENT 1"; the audit is 286336); told 2026-11-25 |
| 295439 | Signed Bylaw 21442, 2026 Property Tax and Supplementary Property Tax Bylaw (published 2026-04-29). Item 8.1, City Council 2026-04-28; report FCS03408 is 295436 and the unsigned bylaw is 295437 | `edmonton-tax-viz` | Blind check of the 2026 mill rates against the primary document, not the `pwis-wc4c` dataset | 2026-11-24 | fetched 2026-11-24, no text (scan). Use `text/295437.txt`, the unsigned bylaw, which passed all three readings unamended per the 04-28 minutes; cite 295439; told 2026-11-25 |
| 286336 | Attachment 1 - OCA03356 - Neighbourhood Renewal Program Audit (the audit itself; 286947 is its cover). Audit Committee 2026-02-04, meeting `03800f25-e306-4f24-86ab-7873f79f9b24`, where the cover report is listed as 286335; the meeting that carries 286947 is not located | `edmonton-tax-viz` | Same as 164273 | 2026-11-25 | wanted |
| 236515 | Attachment 1 - FCS02218 - Fiscal Gap - An Assessment of Factors Contributing to the City of Edmonton's Operation and Capital (the likely home of the category figures). Executive Committee 2024-10-09 item 7.1, meeting `ca7dde3e-d08e-42a6-9fb0-2d0c94909689`; re-posted for City Council 2024-10-22 (meeting `c9b20667-6d9e-4a17-a09d-5ede3dfdf61b`) as 239202 | `alberta-regional-viz` | Edmonton source for its planned mandate register (its `docs/SCOPE_candidates.md` item 4); secondary-report figures are marked unchecked against FCS02218. Low priority | 2026-11-25 | wanted |
| 236514 | Report - FCS02218 Capital and Operating Funding Shortfall Analysis (the cover report; same meeting as 236515; Council re-post 239201, plus an Executive Committee cover 239200; presentation 236516 not requested) | `alberta-regional-viz` | Same as 236515 | 2026-11-25 | wanted |
| 9778 | Bylaw 18666 - Annexation Implementation Bylaw - Attachment 2 - Negotiation Commitments - CR_6605.pdf (Executive Committee 2019-01-14, meeting `9f618790-80a4-414f-9121-a6cb3226bc3b`) | `alberta-regional-viz` | Phase 2c core-vs-ring property tax rates (pooled regional rate, rate gap) and their captions: Annexation deal terms and any compensation a pooled rate would misstate | 2026-11-26 | wanted |
| 9739 | Annexation Update - Attachment 1 - Leduc _ Beaumont Order in Council.pdf (Inter-municipal and Regional Development Committee 2019-01-18, meeting `206a546e-7629-4cb3-86ae-3ebffac5372d`) | `alberta-regional-viz` | Phase 2c core-vs-ring property tax rates (pooled regional rate, rate gap) and their captions: The legacy-annexed tax rule (OIC 359/2018) in primary form | 2026-11-26 | wanted |
| 78486 | FCS00021rev - Leduc County Annexation Area - Taxpayer Support Options - REPORT .pdf (Executive Committee 2021-02-01, meeting `0c1966a2-b7fb-42bf-aeec-83437dbce27f`) | `alberta-regional-viz` | Phase 2c core-vs-ring property tax rates (pooled regional rate, rate gap) and their captions: How annexed-area taxes were set | 2026-11-26 | wanted |
| 4785 | Tax Policy Discussion - CR_7218 - Attachment 1 - Property Tax Policy Discussion Paper.pdf (Executive Committee 2020-01-27, meeting `fe4da525-7c4c-4578-b353-8cfa4a30e5c8`) | `alberta-regional-viz` | Phase 2c core-vs-ring property tax rates (pooled regional rate, rate gap) and their captions: Any rate comparison with neighbours | 2026-11-26 | wanted |
| 16753 | Edmontons Business Climate Competitiveness - CR_4256 Attachment 1 - Edmontons Business Competitiveness Report June 5 1.pdf (Executive Committee 2017-07-04, meeting `17783c7c-a84c-49df-924b-4bbb9069483f`) | `alberta-regional-viz` | Phase 2c core-vs-ring property tax rates (pooled regional rate, rate gap) and their captions: Rate and tax-burden comparison | 2026-11-26 | wanted |
| 226114 | Report - FCS02483 Budget Update - Non-residential Tax Base Growth Challenges.pdf (Executive Committee 2024-06-19, meeting `cb68655b-0b7c-466e-9937-23d378a474be`) | `alberta-regional-viz` | Phase 2c core-vs-ring property tax rates (pooled regional rate, rate gap) and their captions: The non-residential base decline the headline share shows | 2026-11-26 | wanted |

URLs follow `https://pub-edmonton.escribemeetings.com/filestream.ashx?DocumentId=<id>`.

## Later

Requested but not to be fetched yet: fetch when fetching gets cheaper (a batch route), or when the requester asks. Status `later`; a row moves up to the main table as `wanted` when it is promoted. All requested by `alberta-regional-viz` on 2026-11-26 for Phase 2c core-vs-ring property tax rates (pooled regional rate, rate gap) and their captions; ids are from the 2017–2025 agenda title scan.

| DocumentId | Title | Group | Status |
|---|---|---|---|
| 9776 | Bylaw 18666 - Annexation Implementation Bylaw - CR_6605 Report - Bylaw 18666 - Omnibus Bylaw - Annexation Implementation.pdf (Executive Committee 2019-01-14, meeting `9f618790-80a4-414f-9121-a6cb3226bc3b`) | Regional sharing | later |
| 9777 | Bylaw 18666 - Annexation Implementation Bylaw - Attachment 1 - Bylaw 18666 - Annexation Implementation.pdf (Executive Committee 2019-01-14, meeting `9f618790-80a4-414f-9121-a6cb3226bc3b`) | Regional sharing | later |
| 13007 | Leduc CountyBeaumont Annexation Adjustment - Leduc CountBeaumont Annexation Adjustment.pdf (Inter-municipal and Regional Development Committee 2018-05-25, meeting `633910aa-34cd-43ca-b15b-ac0d52f3bdbf`) | Regional sharing | later |
| 5651 | Annexation Costs - Supplemental Operating Budget A - CR_6761 - Annexation Costs - Supplemental Operating Budget Adjustment - REPORT.pdf (City Council 2019-11-05, meeting `d00f394c-d187-47d8-b3f8-a6a7fc6d5385`) | Regional sharing | later |
| 66715 | FCS00021 - Property Valuation - Leduc County Annexation Area - REPORT.pdf (Executive Committee 2020-10-26, meeting `aa68df69-2c18-46d2-a6be-706d658c6178`) | Regional sharing | later |
| 4988 | Intermunicipal Collaboration Frameworks Update - CR_7423_ Intermunicipal Collaboration Frameworks Update January 17 2020 IRDC.pdf (Inter-municipal and Regional Development Committee 2020-01-17, meeting `1ee547fc-282b-44a5-b612-b2a751f9f1d1`) | Regional sharing | later |
| 4989 | Intermunicipal Collaboration Frameworks Update - CR_7423 Intermunicipal Collaboration Frameworks - Attachment 1 - FINAL City.pdf (Inter-municipal and Regional Development Committee 2020-01-17, meeting `1ee547fc-282b-44a5-b612-b2a751f9f1d1`) | Regional sharing | later |
| 64588 | Attachment 1 - CR_7913 Beaumont Intermunicipal Collaboration Framework Agreement.pdf (Inter-municipal and Regional Development Committee 2020-10-09, meeting `812bf629-3c37-4c54-aef1-48c61e9bdf47`) | Regional sharing | later |
| 64589 | Attachment 2 - CR_7913 Devon Intermunicipal Collaboration Framework Agreement.pdf (Inter-municipal and Regional Development Committee 2020-10-09, meeting `812bf629-3c37-4c54-aef1-48c61e9bdf47`) | Regional sharing | later |
| 14934 | Edmonton Metropolitan Region Board Update - CR_5424 Edmonton Metropolitan Region Board Update.pdf (Inter-municipal and Regional Development Committee 2018-01-18, meeting `081bb908-6df6-46e3-b99c-51871c1de133`) | Regional sharing | later |
| 64591 | Report - CE00026 - Edmonton Metropolitan Region Board - Metropolitan Region Servicing Plan.pdf (Inter-municipal and Regional Development Committee 2020-10-09, meeting `812bf629-3c37-4c54-aef1-48c61e9bdf47`) | Regional sharing | later |
| 64592 | Attachment 1 - CE00026 Edmonton Metropolitan Region Servicing Plan Breifing Note .pdf (Inter-municipal and Regional Development Committee 2020-10-09, meeting `812bf629-3c37-4c54-aef1-48c61e9bdf47`) | Regional sharing | later |
| 130867 | UPE01044 Collaborative Economic Development - Initiative Orientation - REPORT.pdf (City Council 2022-02-22, meeting `4095f41b-83b1-4b17-b008-6889aa9f1ebc`) | Regional sharing | later |
| 17949 | Regional Economic Development Entity - Update - Attachment5-DraftThreeYearRegionalEconomicDevelopmentEntityBudgetCostSharing.pdf (City Council 2017-04-25, meeting `82a400c3-563b-4819-88dc-c52d5256e115`) | Regional sharing | later |
| 15382 | Albertas Industrial Heartland Association - Membe - CR_4981 Albertas Industrial Heartland Association - Membership Agreement.pdf (Executive Committee 2017-11-28, meeting `a5c5526b-964f-4c20-922b-68ca0d4625b1`) | Regional sharing | later |
| 10901 | Collective Tax Burden on Small and Medium Sized Bu - CR_5467 - Collective Tax Burden on Small and Medium Sized Business - REPORT .pdf (Executive Committee 2018-10-15, meeting `ad5871e3-bbf1-4275-aacd-c9c3539b07ba`) | Rate and tax policy | later |
| 8300 | Alternative Financing Models for Industrial Develo - Attachment 3 - CR_5606 Summary Assessment of Competitiveness and Investment Readiness of Edmon.pdf (Executive Committee 2019-04-25, meeting `5fd81693-06e7-48e5-98fc-58ee72862afe`) | Rate and tax policy | later |
| 4786 | Tax Policy Discussion - CR_7218 - Attachment 2 - Report 7139.pdf (Executive Committee 2020-01-27, meeting `fe4da525-7c4c-4578-b353-8cfa4a30e5c8`) | Rate and tax policy | later |
| 88576 | CR_8017 Residential _ Non-Residential Assessment Ratio.pdf (Executive Committee 2021-04-12, meeting `404618cc-a9b5-4086-9a2f-923af2f6319b`) | Rate and tax policy | later |
| 64923 | CR_7719 -Amendments to Policy C607 - Potential Tax Policy Parameters for Exceptions - REPORT.pdf (Executive Committee 2020-10-16, meeting `5529138b-7dba-41e2-8073-44fe7e0243f0`) | Rate and tax policy | later |
| 5622 | Assessment and Taxation Audit - CR_7692 - Assessment and Taxation Audit.pdf (Audit Committee 2019-11-08, meeting `49ffca56-43db-49c0-9955-a0f1ea1f5d1f`) | Rate and tax policy | later |
| 5623 | Assessment and Taxation Audit - Attachment 1 - Assessment and Taxation.pdf (Audit Committee 2019-11-08, meeting `49ffca56-43db-49c0-9955-a0f1ea1f5d1f`) | Rate and tax policy | later |
| 5624 | Administration Response - Assessment and Taxation - CR_7682 - Administration Response - Assessment and Taxation Audit - REPORT.pdf (Audit Committee 2019-11-08, meeting `49ffca56-43db-49c0-9955-a0f1ea1f5d1f`) | Rate and tax policy | later |
| 81934 | FCS00132 - Pending LRT Lines and City-wide Transit Routes Assessment Growth Options - REPORT (1).pdf (Executive Committee 2021-03-01, meeting `98f93548-449d-4d10-bc91-a54aafb5542c`) | Rate and tax policy | later |
| 81935 | FCS00132 - Pending LRT Lines and City-wide Transit Routes Assessment Growth Options - Attachment 1.pdf (Executive Committee 2021-03-01, meeting `98f93548-449d-4d10-bc91-a54aafb5542c`) | Rate and tax policy | later |
| 162841 | FCS01332 Jurisdictional Scan of Police Funding - REPORT.pdf (City Council 2022-10-03, meeting `d4dab0a9-751e-42ee-8a5a-6f9351a595cd`) | Provincial cost shares | later |
| 162843 | Attachment 2 - FCS01332 Jurisdictional Scan of Police Funding.pdf (City Council 2022-10-03, meeting `d4dab0a9-751e-42ee-8a5a-6f9351a595cd`) | Provincial cost shares | later |
| 193932 | Report - EXT02009 - Police Funding Formula Analysis .pdf (City Council 2023-08-22, meeting `8e39782c-cb09-40f9-8bb8-abe7813834c2`) | Provincial cost shares | later |
| 92286 | FCS00480 - Municipal Sustainability Initiative - Summary of Historical Cuts to Operating and Capital Dollars - REPORT.pdf (City Council 2021-04-19, meeting `4f8b7ecb-66b8-4140-b46d-ab9657dc5048`) | Provincial cost shares | later |
| 100828 | FCS00480rev - Municipal Sustainability Initiative - Summary of Historical Cuts to Operating and Capital Dollars - REPORT.pdf (City Council 2021-06-07, meeting `85917484-cc9a-44de-9ef3-8cb441027cf3`) | Provincial cost shares | later |
| 5235 | Fall 2019 Supplemental Capital Budget Adjustment - - CR_7485rev - Attachment 4 - MSI Reduction Strategy Detai.pdf (City Council 2019-12-05, meeting `1c0ae48f-2baf-48a1-bb8f-b7f2e890698a`) | Provincial cost shares | later |
| 7314 | Policing Costs Related to Highway 19 - Cost Reduct - Policing Costs Related to Highway 19 Report CR_6754.pdf (Urban Planning Committee 2019-06-25, meeting `0a77c7c0-02bc-4aab-9364-db8b838e2dad`) | Provincial cost shares | later |
| 250836 | Report - FCS02746 Fiscal Gap Strategies Work Plan.pdf (Executive Committee 2025-03-05, meeting `cef4d90f-e45a-4351-8d55-17e848338ff6`) | Fiscal gap and transit | later |
| 3397 | 2020 Alberta Urban Municipalities Association Reso - CR_8381 - Attachment 2 - Fiscal Framework.pdf (City Council 2020-06-22, meeting `057b539c-bcf4-4139-9150-3d06c47c9677`) | Fiscal gap and transit | later |
| 3398 | 2020 Alberta Urban Municipalities Association Reso - CR_8381 - Attachment 3 - Permanent Transit Funding.pdf (City Council 2020-06-22, meeting `057b539c-bcf4-4139-9150-3d06c47c9677`) | Fiscal gap and transit | later |
| 135559 | REPORT - CO00803 Bus Network Expansion Opportunities - Transit Funding Model Options.pdf (Executive Committee 2022-03-23, meeting `ab98dfb3-b8d3-487a-b0d2-370c6fbd308b`) | Fiscal gap and transit | later |
