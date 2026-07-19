# Second-Run Final Report

Date: 2026-05-19

## 1. What was found in the raw data

The raw file `data/raw/Rwanda-2023-full-data.dta` opens successfully in Python and contains 358 observations and 355 variables. The converted CSV `data/raw/Rwanda-2023-full-data.csv` has the same 358 observations. Key variables required by the current papers are present, including `h1`, `h2`, `h5`, `c22b`, `l1`, `wmedian`, `wstrict`, `wweak`, `a2`, `a3a`, `a4a`, and `a6a`.

Important official variable labels are:

- `h1`: new products/services introduced over the last three years
- `h2`: new products/services also new for the establishment's main market
- `h5`: new or significantly improved process over the last three years
- `c22b`: establishment has its own website
- `l1`: permanent full-time employees at the end of the last fiscal year
- `wmedian`, `wstrict`, `wweak`: WBES survey weights

Python can read the `.dta` file reliably when Stata categorical labels are kept as raw numeric codes. Direct categorical conversion fails because at least one Stata value-label set contains duplicate category text. The safe workflow is therefore to read raw numeric codes and separately extract labels.

## 2. Whether Stata successfully ran the raw file

A Stata do-file was created at:

`code/stata/01_raw_data_second_run.do`

The installed executable used was:

`C:\Program Files\Stata17\StataMP-64.exe`

The Stata batch run completed successfully and produced:

`results/stata/logs/second_run_stata.log`

The log closes normally with the message:

`Second run completed: 19 May 2026 06:36:41`

Stata-generated outputs include `results/stata/second_run_weighted_prevalence.csv`, `results/stata/second_run_fragility_validation.csv`, group tables, and Stata PNG plots in `results/figures/second_run/`.

## 3. Whether the second run reproduced the existing results

The raw-data reconstruction exactly reproduces the supplied processed classification:

- Observations: 358
- Supplied fragile firms: 62
- Second-run fragile firms: 62
- Matches: 358
- Mismatches: 0
- Agreement: 1.000

This confirms the computational rule but also reinforces the construct-validity warning: the official WBES labels do not support unqualified claims that the rule measures revenue volatility or digital-platform difficulty.

## 4. Weighted and unweighted estimates

The second run confirms the following prevalence estimates:

| Approach | Fragility percent |
|---|---:|
| Unweighted | 17.32 |
| wmedian | 21.33 |
| wstrict | 20.95 |
| wweak | 21.56 |

The weighted estimates support Paper 2's argument that national formal-firm interpretation should not rely on the unweighted sample share alone.

## 5. Machine-learning rerun

The LASSO-logit pipeline was rerun from the raw-data reconstruction. The held-out test set results are:

| Metric | Value |
|---|---:|
| Accuracy | 0.967 |
| Precision | 0.882 |
| Recall | 0.938 |
| Specificity | 0.973 |
| ROC-AUC | 0.978 |
| Test observations | 90 |
| Test fragile observations | 16 |

The result confirms high apparent discrimination. However, it should be flagged for improvement because the predictor set includes variables used to define the recovered outcome. The model is currently strongest as an audit of the screening rule, not as independent evidence of causal drivers or external predictive validity.

To fix this, a leakage-reduced model was added. It excludes the variables used in the recovered classification rule: `h1`, `h2`, `h5`, and `c22b`. Its held-out performance is:

| Metric | Value |
|---|---:|
| Accuracy | 0.611 |
| Precision | 0.279 |
| Recall | 0.750 |
| Specificity | 0.581 |
| ROC-AUC | 0.770 |
| Test observations | 90 |
| Test fragile observations | 16 |

This is now the more honest internal benchmark. The full model should be described as a rule audit; the leakage-reduced model should guide future predictive claims until independent outcome data are available.

## 6. Tables and plots generated

Second-run tables were generated in `results/tables/` and `results/stata/`, including:

- `second_run_fragility_validation_summary.csv/.tex`
- `second_run_key_variable_descriptives.csv/.tex`
- `second_run_missingness_top25.csv/.tex`
- `second_run_weighted_prevalence.csv/.tex`
- `second_run_region_table.csv/.tex`
- `second_run_sector_table.csv/.tex`
- `second_run_size_table.csv/.tex`
- `second_run_website_table.csv/.tex`
- `second_run_process_innovation_table.csv/.tex`
- `second_run_lasso_test_performance.csv/.tex`
- `second_run_lasso_coefficients.csv/.tex`

Second-run plots were generated in `results/figures/second_run/`:

- `weighted_unweighted_prevalence.png`
- `fragility_by_region.png`
- `fragility_by_sector.png`
- `fragility_by_size.png`
- `fragility_by_website.png`
- `missingness_top20.png`
- `lasso_test_roc.png`
- `lasso_coefficients.png`
- `second_run_lasso_no_rulevars_roc.png`
- `second_run_lasso_no_rulevars_coefficients.png`
- `predicted_probability_distribution.png`
- Stata-generated `stata_*.png` plots

## 7. How Paper 1 changed

Paper 1 was updated to:

- report the second-run raw-data validation
- cite the exact recovered rule as confirmed from the raw `.dta`
- correct the interpretation toward official WBES labels
- add second-run validation, LASSO plots, and a leakage-reduced ML benchmark
- caution that high LASSO performance is partly mechanical because some predictors overlap with the outcome rule
- expand the literature base beyond 20 DOI/source-linked references
- compile under strict APA 7 with `apa7`, `biblatex-apa`, and `biber`

The compiled PDF is:

`papers/paper_1/main.pdf`

## 8. How Paper 2 changed

Paper 2 was updated to:

- use second-run weighted prevalence tables
- use second-run regional tables and plots
- state that weighted estimates are about 21 percent, compared with the unweighted 17.3 percent
- clarify that these are formal-firm survey-frame estimates, not estimates for all Rwandan enterprises
- compile under strict APA 7 with `apa7`, `biblatex-apa`, and `biber`

The compiled PDF is:

`papers/paper_2/main.pdf`

## 9. Remaining gaps before journal submission

- Preserve and review the Stata log when revising tables; the do-file now runs successfully from the installed StataMP executable.
- Add design-based standard errors or confidence intervals for weighted estimates.
- Validate the fragility classification against an independent outcome such as closure, sales decline, employment contraction, or future survival.
- Reconstruct the Omega score directly from raw variables before reporting it as an empirical result.
- Decide whether `a2` or `a3a` is the authoritative geography variable.
- Resolve all older draft language that conflicts with official WBES labels.
- Add a data availability statement and ethics statement for the target journal.

## 10. Additional data that would strengthen future papers

- Rwanda district/province boundaries for spatial inequality analysis.
- NISR Establishment Census 2023 formal/informal enterprise data.
- NISR Integrated Business Enterprise Survey 2023 microdata or tables.
- District-level internet access, mobile-money, electricity, road density, and nightlights.
- Administrative data on firm entry, exit, tax registration, or employment if accessible.
- Sector-specific industrial-policy data for manufacturing-focused analysis.
