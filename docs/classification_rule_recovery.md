# Classification Rule Recovery

The supplied outcome `fragility_risk_flex` is no longer opaque. A decision-tree audit of the raw WBES CSV recovers an exact deterministic rule with 100% agreement against `data/processed/classification_probabilities.csv`.

## Exact recovered rule

Using the raw survey variables in `data/raw/Rwanda-2023-full-data.csv`, a firm is classified as fragile if any of the following conditions hold:

1. `h5 == 1` and `l1 <= 3`
2. `h5 == 2` and `c22b == 1` and `l1 <= -2`
3. `h5 == 2` and `c22b == 2` and (`h1 == 2` or `h2 != 1`)

Otherwise, the firm is classified as non-fragile.

## Verification

The notebook writes the verification audit to:

- `results/models/recovered_fragility_rule_audit.csv`
- `results/tables/table_recovered_classification_rule_summary.csv`
- `results/tables/table_recovered_classification_rule_summary.tex`

Current result:

| Measure | Value |
|---|---:|
| Supplied fragile firms | 62 |
| Recovered-rule fragile firms | 62 |
| Agreement | 1.000 |
| Mismatches | 0 |

## Construct-validity issue

The recovered computational rule is exact, but the variable labels require harmonization before journal submission.

Official labels extracted from the Stata file identify:

- `h1`: New products/services introduced over the last 3 years
- `h2`: New products/services also new for the establishment's main market
- `h5`: Establishment introduced a new/significantly improved process over the last 3 years
- `c22b`: Establishment has its own website
- `l1`: Number of permanent, full-time employees at the end of the last fiscal year

Some Word drafts instead describe `h5` as revenue volatility and `c22b` as digital-platform difficulty. The official Stata labels should be treated as authoritative unless the team can document why the processed workbook uses alternative labels.

## Paper implication

Paper 1 can now report the outcome transparently. However, claims about "revenue volatility" and "digital platform difficulty" should be revised or heavily qualified unless the original variable mapping is verified from the WBES questionnaire or original Stata code.
