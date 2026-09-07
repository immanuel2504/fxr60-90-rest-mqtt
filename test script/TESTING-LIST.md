# Live testing list

Run these on a PC that can open the reader. This PC cannot reach it.

| # | What | Command | What to extract |
|---|---|---|---|
| 1 | `/cloud/impinjGen2X` GET then PUT then GET | `py -3 test_impinj_gen2x_roundtrip.py` | HTTP status and both GET bodies (empty vs after configure) |

Reports: `test script/reports/success/` or `reports/failure/`.
