# GitHub Backup Safety Audit

Date: 2026-07-19

## Repository Privacy Recommendation

Use a private GitHub repository. The project contains raw and processed firm-level survey data, Word drafts, and model prediction outputs. These materials should not be pushed to a public repository unless the data license and all authors explicitly permit public release.

## Secret Scan

A text-file scan was run for common secret patterns including API keys, tokens, passwords, bearer credentials, GitHub tokens, Canvas tokens, and OpenAI key patterns. The scan excluded binary files, `.venv/`, `tmp_biber/`, PDFs, DOCX, images, and `.dta` files.

Result: no obvious credential secrets were found. Matches were false positives in LaTeX logs, manuscript text, and notebook prose.

## Sensitive or Review-Required Materials

| Path | Risk | Recommendation |
|---|---|---|
| `data/raw/Rwanda-2023-full-data.dta` | Raw survey microdata | Track only in private repo; confirm license before public release |
| `data/raw/Rwanda-2023-full-data.csv` | Converted raw survey microdata | Track only in private repo |
| `data/processed/*.csv` | Derived firm-level analysis data | Track only in private repo unless anonymization/license is confirmed |
| `results/models/*.csv` | Firm-level predictions and classification audit outputs | Track only in private repo |
| `docs/drafts/original_word/*.docx` | Original Word drafts and strategy notes | Track private repo only |
| `docs/briefs/Email_to_Simeon.docx` | Brief/email-style document | Review before sharing outside private repo |
| `results/stata/logs/*.log` | Logs may include local paths and workflow details | Acceptable for private backup; review before public release |

## Large/Binary File Handling

Git LFS is installed. `.gitattributes` configures Git LFS for `.dta`, `.docx`, `.pdf`, `.png`, `.jpg`, `.jpeg`, and `.xlsx` files.

Largest research-relevant files outside disposable folders are modest in size, led by:

- `docs/drafts/original_word/Lasso_paper_strategy_and_drafts.docx` around 1.9 MB
- `data/raw/Rwanda-2023-full-data.dta` around 1.1 MB
- `docs/briefs/Email_to_Simeon.docx` around 0.95 MB
- `papers/paper_1/main.pdf` around 0.55 MB

## Disposable Files and Folders

The following are excluded by `.gitignore`:

- `.venv/`
- `tmp_biber/`
- `Stata 17/`
- LaTeX auxiliary files
- Jupyter checkpoints
- OS/temp files
- visual table-check screenshots

## Push Gate

Do not push to a public repository. A private GitHub backup is acceptable after the user confirms GitHub authentication and remote creation.

