# Reproducibility Guide

## Software Requirements

Use Python 3.10 or later. The local project contains a `.venv`; install dependencies from `requirements.txt` if creating a fresh environment.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For manuscript compilation, install a LaTeX distribution with `apa7`, `biblatex-apa`, and `biber`.

## Data Requirements

The workflow expects:

- `data/raw/Rwanda-2023-full-data.csv`
- `data/raw/Rwanda-2023-variable-labels.csv`
- `data/processed/Rwanda_2023_predictors_only.csv`
- `data/processed/classification_probabilities.csv`
- `data/processed/Labeled_Predictors_for_Rwanda_SME_Fragility_Study.csv`
- `data/processed/omega_score.csv`

The raw Stata file is retained for provenance:

- `data/raw/Rwanda-2023-full-data.dta`

## Analysis Order

Run the merged notebook:

```powershell
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute code\notebooks\01_reproducible_analysis_and_research_expansion.ipynb --output 01_reproducible_analysis_and_research_expansion.ipynb --output-dir code\notebooks --ExecutePreprocessor.timeout=300
```

The notebook:

- documents the raw-data contribution to the research question
- implements and audits the fragility and Omega formulas
- reconstructs the exact classification rule
- reruns the LASSO-logit model
- generates publication tables and figures
- outlines external-data extensions for future papers

Generated Paper 1 outputs include:

- `data/processed/analysis_dataset.csv`
- `results/tables/table_1_sample_summary.*`
- `results/tables/table_2_fragility_profile.*`
- `results/tables/table_3_sector_by_fragility.*`
- `results/tables/table_4_lasso_test_performance.*`
- `results/tables/table_5_lasso_coefficients.*`
- `results/tables/table_raw_variable_context.csv`
- `results/tables/table_recovered_classification_rule_summary.*`
- `results/figures/figure_lasso_test_roc.png`
- `results/figures/figure_formula_components_by_fragility.png`
- `results/figures/figure_formula_vs_supplied_fragility.png`
- `results/figures/figure_finance_digital_risk_space.png`
- `results/figures/figure_weighted_unweighted_region_fragility.png`
- `results/models/lasso_test_predictions.csv`
- `results/models/fragility_formula_components.csv`
- `results/models/recovered_fragility_rule_audit.csv`

Generated Paper 2 outputs include:

- `papers/paper_2/tables/table_1_weighted_prevalence.*`
- `papers/paper_2/tables/table_2_region_weighted_fragility.*`
- `papers/paper_2/tables/table_2_sector_weighted_fragility.*`
- `papers/paper_2/tables/table_2_size_weighted_fragility.*`
- `papers/paper_2/figures/figure_1_weighted_prevalence.png`
- `papers/paper_2/figures/figure_2_weighted_by_region.png`
- `papers/paper_2/figures/figure_2_weighted_by_sector.png`
- `papers/paper_2/figures/figure_2_weighted_by_size.png`

The exact recovered outcome rule is documented in `docs/classification_rule_recovery.md`.

## Manuscript Compilation

Paper 1:

```powershell
Set-Location papers\paper_1
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Paper 2:

```powershell
Set-Location papers\paper_2
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Both papers use `apa7` with `biblatex-apa`, so `biber` is required. Do not use the older `bibtex` workflow.

## Current Manuscript Previews

- `papers/paper_1/main.pdf`
- `papers/paper_2/main.pdf`

## Cleanup Record

The cleanup dry run and deletion log is stored in `docs/cleanup_audit.md`. The deleted files were regenerable LaTeX build artifacts, superseded legacy outputs, archived duplicate/proprietary working copies, and empty folders. Original data and Word-source drafts were retained.
