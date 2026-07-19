# Stata/Python Second-Run Result Comparison

This file compares the new raw-data second run with the current project outputs. Stata execution status is recorded separately in `docs/second_run_final_report.md`; the Python second run uses the same raw `.dta` file and exports Stata-compatible CSV tables.

## Outcome reconstruction

- Supplied fragile firms: 62
- Second-run fragile firms: 62
- Agreement: 1.000
- Mismatches: 0

The recovered rule is confirmed against the processed classification file.

## Weighted prevalence

| approach   | fragility_pct |
| ---------- | ------------- |
| unweighted | 17.318        |
| wmedian    | 21.331        |
| wstrict    | 20.951        |
| wweak      | 21.560        |

These values should be compared against Paper 2's current table. They are expected to match if the same raw rule and weights are used.

## Machine-learning rerun

| accuracy | precision | recall | specificity | roc_auc | test_n | test_fragile_n |
| -------- | --------- | ------ | ----------- | ------- | ------ | -------------- |
| 0.967    | 0.882     | 0.938  | 0.973       | 0.978   | 90     | 16             |

## Leakage-reduced model

Rule variables excluded: h1, h2, h5, c22b

| accuracy | precision | recall | specificity | roc_auc | test_n | test_fragile_n |
| -------- | --------- | ------ | ----------- | ------- | ------ | -------------- |
| 0.611    | 0.279     | 0.750  | 0.581       | 0.770   | 90     | 16             |

The rerun confirms high apparent discrimination, but the result should be flagged for improvement because the model includes variables that are also used to define the outcome. This makes the result useful as an audit of the screening rule, not as independent evidence of external predictive validity.

## Results requiring improvement before journal submission

- Treat the leakage-reduced model as the more honest internal benchmark until an independent outcome such as closure, revenue contraction, employment loss, or follow-up survival is available.
- Rebuild the theoretical finance/digital Omega score directly from raw variables; the existing Omega export is not empirically informative.
- Add design-based standard errors for weighted estimates.
- Decide whether `a2` or `a3a` should be the authoritative geography variable.
- Reconcile all manuscript language with official WBES variable labels.
