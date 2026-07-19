# GitHub Backup Inventory

Date: 2026-07-19

Project root: `D:\Research\LASSO`

## Summary

The project contains raw and processed Rwanda Enterprise Survey data, Python and Stata analysis code, one reproducible notebook, model outputs, publication tables and figures, two LaTeX paper folders, editable Word/PDF outputs, and project documentation.

The folder was not a Git repository before this backup-preparation pass.

## Top-Level Inventory

| Path | Role | Tracking decision | Sensitivity |
|---|---|---|---|
| `data/raw/` | Raw Rwanda 2023 Enterprise Survey `.dta`, converted CSV, and variable labels | Track in private GitHub repo; `.dta` via Git LFS | High: raw survey microdata |
| `data/processed/` | Cleaned/processed CSV analysis inputs | Track | Medium: derived firm-level data |
| `code/notebooks/` | Reproducible notebook for analysis and research expansion | Track | Low-medium |
| `code/python/` | Python second-run analysis script | Track | Low |
| `code/stata/` | Stata do-file for raw-data second run | Track | Low |
| `results/tables/` | Generated CSV and LaTeX tables | Track | Low-medium |
| `results/figures/` | Generated publication figures | Track via Git LFS for PNG files | Low-medium |
| `results/models/` | Model prediction and classification-audit CSV outputs | Track | Medium: derived firm-level predictions |
| `results/stata/` | Stata outputs, codebook, logs, and metadata | Track selected source/output files; logs reviewed for local paths | Low-medium |
| `papers/paper_1/` | Main LaTeX manuscript, sections, references, PDF, editable DOCX, Mendeley bibliography | Track; binary outputs via Git LFS | Low-medium |
| `papers/paper_2/` | Weighted-estimates manuscript, PDF, tables, and figures | Track; binary outputs via Git LFS | Low-medium |
| `docs/` | Research reports, reproducibility guides, audits, original Word drafts, briefs | Track private repo only; DOCX via Git LFS | Medium-high for Word drafts |
| `archive/` | Archived or snapshot materials | Track lightweight records; review any future large archive files | Medium |
| `.codex/skills/lasso-research-workflow/` | Reusable workflow skill for future Codex sessions | Track | Low |
| `.venv/` | Local Python virtual environment | Exclude | Low; disposable and very large |
| `tmp_biber/` | Local Biber extraction/cache files | Exclude | Low; disposable and very large |
| `Stata 17/` | Local install/cache placeholder | Exclude | Low; machine-specific |

## File-Type Summary Excluding `.venv/` and `tmp_biber/`

| Extension | Count | Backup decision |
|---|---:|---|
| `.csv` | 61 | Track |
| `.png` | 60 | Track with Git LFS |
| `.tex` | 47 | Track |
| `.md` | 16 | Track |
| `.docx` | 5 | Track with Git LFS in private repo |
| `.log` | 4 | Exclude LaTeX logs; retain Stata logs only if useful |
| `.pdf` | 2 | Track with Git LFS |
| `.bib` | 2 | Track |
| `.ipynb` | 1 | Track |
| `.dta` | 1 | Track with Git LFS in private repo |
| `.do` | 1 | Track |
| `.py` | 1 | Track |

## Key Source and Output Files

- `data/raw/Rwanda-2023-full-data.dta`
- `data/raw/Rwanda-2023-full-data.csv`
- `data/raw/Rwanda-2023-variable-labels.csv`
- `data/processed/analysis_dataset.csv`
- `code/notebooks/01_reproducible_analysis_and_research_expansion.ipynb`
- `code/python/02_second_run_raw_analysis.py`
- `code/stata/01_raw_data_second_run.do`
- `papers/paper_1/main.tex`
- `papers/paper_1/main.pdf`
- `papers/paper_1/Paper_1_editable.docx`
- `papers/paper_1/Paper_1_word_complete_source.md`
- `papers/paper_1/references.bib`
- `papers/paper_2/main.tex`
- `papers/paper_2/main.pdf`
- `docs/reproducibility_guide.md`
- `docs/second_run_final_report.md`
- `docs/stata_python_result_comparison.md`

## Excluded Disposable Materials

- `.venv/`
- `tmp_biber/`
- LaTeX auxiliary files such as `.aux`, `.bbl`, `.bcf`, `.blg`, `.log`, `.out`, `.run.xml`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, and `.ttt`
- Jupyter checkpoints
- temporary files
- visual formatting QA screenshots in `papers/paper_1/table_check-*.png` and `papers/paper_1/table_2_10_11_check-*.png`

