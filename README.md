# LASSO Rwanda SME Fragility Research Project

This repository contains a reproducible research project on constructed small and medium-sized enterprise (SME) fragility in Rwanda using the 2023 World Bank Enterprise Survey. The workflow audits a legacy fragility classification, reconstructs the exact rule behind the outcome, evaluates predictor-outcome leakage, reruns Python and Stata analyses, generates publication tables and figures, and drafts APA 7 social-science manuscripts.

## Research Objective

The project asks whether a constructed firm-level fragility classification for formal Rwandan SMEs can be transparently reconstructed, audited, and predicted using penalized logistic regression. The current work treats the outcome as a screening index, not as observed survival, closure, bankruptcy, or financial distress.

## Project Structure

```text
data/
  raw/                  Raw Rwanda 2023 Enterprise Survey data, converted CSV, and labels
  processed/            Curated predictors, classifications, Omega scores, and analysis data
code/
  notebooks/            Reproducible notebook with merged research code
  python/               Second-run Python analysis script
  stata/                Stata do-file for raw-data verification
results/
  tables/               CSV and LaTeX result tables
  figures/              Publication figures and diagnostics
  models/               Prediction outputs and rule-recovery audits
  stata/                Stata outputs, logs, and codebook
papers/
  paper_1/              Main APA 7 LASSO-logit screening manuscript
  paper_2/              Weighted formal-SME fragility estimates manuscript
docs/
  drafts/               Original Word drafts and strategy notes
  inventory/            Earlier file inventory
  *.md                  Reproducibility, audit, comparison, and backup documentation
archive/
  backup_snapshot_*/    Lightweight backup packaging snapshots
.codex/
  skills/               Reusable Codex workflow skill
```

## Data Sources

Primary data files:

- `data/raw/Rwanda-2023-full-data.dta`
- `data/raw/Rwanda-2023-full-data.csv`
- `data/raw/Rwanda-2023-variable-labels.csv`

Processed analysis files:

- `data/processed/analysis_dataset.csv`
- `data/processed/Rwanda_2023_predictors_only.csv`
- `data/processed/classification_probabilities.csv`
- `data/processed/Labeled_Predictors_for_Rwanda_SME_Fragility_Study.csv`
- `data/processed/omega_score.csv`

These files may contain raw or derived firm-level survey data. Keep the repository private unless public-release rights are explicitly confirmed.

## Key Papers

Paper 1:

- Source: `papers/paper_1/main.tex`
- PDF: `papers/paper_1/main.pdf`
- Editable DOCX: `papers/paper_1/Paper_1_editable.docx`
- Word source: `papers/paper_1/Paper_1_word_complete_source.md`

Paper 2:

- Source: `papers/paper_2/main.tex`
- PDF: `papers/paper_2/main.pdf`

## Software Requirements

Python dependencies are listed in `requirements.txt`:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The manuscript workflow also requires:

- A LaTeX distribution with `apa7`, `biblatex-apa`, and `biber`
- Pandoc for DOCX generation
- Stata for the raw-data second-run do-file
- Git LFS for binary research artifacts

## Analysis Workflow

Run or review the notebook:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute code\notebooks\01_reproducible_analysis_and_research_expansion.ipynb --output 01_reproducible_analysis_and_research_expansion.ipynb --output-dir code\notebooks --ExecutePreprocessor.timeout=300
```

Run the second-run Python script:

```powershell
.\.venv\Scripts\python.exe code\python\02_second_run_raw_analysis.py
```

Run the Stata workflow from Stata:

```stata
do "D:\Research\LASSO\code\stata\01_raw_data_second_run.do"
```

The key audit files are:

- `docs/classification_rule_recovery.md`
- `docs/raw_data_second_run_audit.md`
- `docs/stata_python_result_comparison.md`
- `docs/second_run_final_report.md`
- `docs/reproducibility_guide.md`

## Compile Manuscripts

From each paper folder:

```powershell
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Regenerate Paper 1 DOCX from `papers/paper_1/`:

```powershell
pandoc Paper_1_word_complete_source.md --from markdown+tex_math_dollars --to docx --resource-path=".;..\..;..\..\results\figures;..\..\results\figures\second_run;..\..\results\tables" --citeproc --bibliography=references.bib --output="Paper_1_editable.docx"
```

## GitHub Backup Notes

This project is prepared for a private GitHub backup. `.gitignore` excludes local environments, Biber caches, LaTeX auxiliary files, temporary files, and visual formatting screenshots. `.gitattributes` configures Git LFS for binary research artifacts including `.dta`, `.docx`, `.pdf`, `.png`, `.jpg`, `.jpeg`, and `.xlsx`.

Backup audit files:

- `docs/github_backup_inventory.md`
- `docs/github_backup_safety_audit.md`
- `docs/github_backup_final_report.md`

Reusable Codex skill:

- `.codex/skills/lasso-research-workflow/SKILL.md`

## Ethical and Sensitivity Notice

This repository contains raw and derived firm-level survey data and unpublished manuscript drafts. It should remain private unless the data license, author permissions, and research-team governance explicitly permit a public release. Do not use the predictive model as a punitive score or as an automated eligibility rule; the manuscripts interpret it as a preliminary screening and audit framework.

## Current Status

Paper 1 and Paper 2 manuscript outputs exist. Paper 1 has been revised to emphasize construct validity, predictor-outcome leakage, transparency of mathematical notation, APA 7 references, and cautious policy interpretation. Paper 2 focuses on weighted formal-SME fragility estimates.

## Authorship

The current Paper 1 title page lists Stanley Mukasa and Simeon Nsabiyumva. Confirm final authorship, affiliations, acknowledgements, and data-use permissions before journal submission or public repository release.
