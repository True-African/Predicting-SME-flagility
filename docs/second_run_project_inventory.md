# Second-Run Project Inventory

Date: 2026-05-19

## Overview

The cleaned LASSO project is now organised around raw WBES data, processed CSV inputs, a single reproducible notebook, second-run Stata/Python audit scripts, generated tables and figures, and two APA 7 LaTeX manuscripts.

## Core data

| Path | Role | Status | Research use |
|---|---|---|---|
| `data/raw/Rwanda-2023-full-data.dta` | Original World Bank Enterprise Survey Stata file | Essential | Authoritative raw source for the second run, variable labels, survey weights, and outcome reconstruction. |
| `data/raw/Rwanda-2023-full-data.csv` | CSV conversion of the raw Stata file | Essential | Open-format analysis copy; row count matches the Stata file. |
| `data/raw/Rwanda-2023-variable-labels.csv` | Extracted variable labels | Essential | Used to audit official meanings of key variables. |
| `data/processed/classification_probabilities.csv` | Legacy fragility outcome and probabilities | Reusable but audited | Provides the supplied outcome that the recovered rule matches exactly. |
| `data/processed/Rwanda_2023_predictors_only.csv` | Thirteen model predictors | Reusable | Used for the LASSO rerun; flagged because some predictors are mechanically related to the outcome. |
| `data/processed/analysis_dataset.csv` | Curated analysis dataset | Reusable | Supports Paper 1 tables, but should be interpreted alongside raw-data verification. |
| `data/processed/omega_score.csv` | Legacy Omega score export | Weak evidence | Flagged for improvement because the score is not currently a validated raw-data reconstruction. |

## Code

| Path | Role | Status | Research use |
|---|---|---|---|
| `code/notebooks/01_reproducible_analysis_and_research_expansion.ipynb` | Main merged notebook | Essential | Shows formulas, recovered rule, LASSO workflow, plots, and future-paper logic. |
| `code/python/02_second_run_raw_analysis.py` | Second-run raw-data audit and model rerun | Essential | Reads the raw `.dta`, exports Stata-compatible CSV/TEX tables, reruns LASSO, and generates plots. |
| `code/stata/01_raw_data_second_run.do` | Stata do-file | Essential but not yet verified by Stata log | Ready for manual/batch Stata execution from the raw `.dta` file. |

## Results

| Folder | Role | Status |
|---|---|---|
| `results/stata/` | Second-run raw-data audit outputs | Newly generated from Python using the raw Stata file. |
| `results/tables/second_run_*.csv` and `.tex` | Second-run manuscript tables | Newly generated and reusable in Papers 1 and 2. |
| `results/figures/second_run/` | Second-run plots | Newly generated publication-style plots. |
| `results/models/second_run_lasso_test_predictions.csv` | Second-run held-out predictions | Newly generated; useful for model audit. |

## Manuscripts

| Path | Role | Status |
|---|---|---|
| `papers/paper_1/main.tex` and `sections/*.tex` | Main LASSO-logit manuscript | Updated to reflect the second run, official labels, APA 7, and expanded literature. |
| `papers/paper_1/references.bib` | Shared bibliography | Expanded beyond 20 entries, with DOI or stable source links. |
| `papers/paper_2/main.tex` | Weighted prevalence manuscript | Updated to use second-run weighted outputs. |

## Documentation

| Path | Role |
|---|---|
| `docs/raw_data_second_run_audit.md` | Raw-data structure, outcome validation, weighted prevalence, and model rerun summary. |
| `docs/stata_python_result_comparison.md` | Comparison of the raw-data rerun with existing project outputs. |
| `docs/second_run_research_logic_audit.md` | Interpretation of the current research logic and weak points. |
| `docs/second_run_final_report.md` | Final report on what changed and what remains. |
| `docs/drafts/original_word/*.docx` | Original intellectual source drafts retained for provenance. |

## Files flagged for improvement

- `data/processed/omega_score.csv`: reconstruct Omega from raw variables before reporting it as an empirical result.
- LASSO performance tables: high AUC is confirmed, but it partly reflects overlap between rule variables and predictors.
- Paper language using "revenue volatility" and "digital platform difficulty": must be reconciled with official WBES labels.
- Paper 2 weighted estimates: add design-based standard errors before journal submission.
