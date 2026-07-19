# Raw Data Second-Run Audit

## Source files

- Raw Stata file: `data\raw\Rwanda-2023-full-data.dta`
- Raw CSV file: `data\raw\Rwanda-2023-full-data.csv`
- Variable-label CSV: `data\raw\Rwanda-2023-variable-labels.csv`

## Dataset structure

- Stata observations: 358
- Stata variables: 355
- CSV observations: 358
- CSV variables: 355
- CSV row count matches Stata: True

## Key finding

The raw `.dta` file is readable in Python and contains the variables needed to reconstruct the current fragility outcome. The second-run rule exactly matches the supplied processed classification: 358 matches out of 358 observations.

## Construct-validity warning

The exact computational rule is transparent, but its substantive interpretation remains fragile. Official labels identify `h5` as process innovation, `c22b` as own website, `h1` and `h2` as product/service innovation, and `l1` as permanent full-time employment. Paper language that calls these variables revenue volatility or digital-platform difficulty should be corrected unless the team can provide a defensible recode.

## Second-run prevalence

| approach   | fragility_pct |
| ---------- | ------------- |
| unweighted | 17.318        |
| wmedian    | 21.331        |
| wstrict    | 20.951        |
| wweak      | 21.560        |

## Second-run LASSO rerun

| accuracy | precision | recall | specificity | roc_auc | test_n | test_fragile_n |
| -------- | --------- | ------ | ----------- | ------- | ------ | -------------- |
| 0.967    | 0.882     | 0.938  | 0.973       | 0.978   | 90     | 16             |

## Leakage-reduced LASSO rerun

To address predictor/outcome overlap, the second run also excludes rule variables from the predictor set: h1, h2, h5, c22b.

| accuracy | precision | recall | specificity | roc_auc | test_n | test_fragile_n |
| -------- | --------- | ------ | ----------- | ------- | ------ | -------------- |
| 0.611    | 0.279     | 0.750  | 0.581       | 0.770   | 90     | 16             |

## Outputs

- `results/stata/second_run_codebook.txt`
- `results/stata/second_run_descriptives.csv`
- `results/stata/second_run_missingness.csv`
- `results/stata/second_run_fragility_validation.csv`
- `results/stata/second_run_weighted_prevalence.csv`
- `results/stata/second_run_region_table.csv`
- `results/stata/second_run_sector_table.csv`
- `results/stata/second_run_size_table.csv`
- `results/stata/second_run_digital_finance_table.csv`
- `results/figures/second_run/*.png`
