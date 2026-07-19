# Second-Run Research Logic Audit

Date: 2026-05-19

## Current research question

Paper 1 asks whether a sparse penalized-logit model can transparently audit and predict SME fragility in Rwanda using the 2023 World Bank Enterprise Survey. Paper 2 asks how the estimated prevalence of formal-firm fragility changes when WBES survey weights are applied.

## Outcome variable

The operative outcome is `fragility_risk_flex`. It is not treated as an observed failure event. It is a recovered screening classification.

The exact rule is:

```text
fragility = 1 if:
  h5 == 1 and l1 <= 3
  OR h5 == 2 and c22b == 1 and l1 <= -2
  OR h5 == 2 and c22b == 2 and (h1 == 2 or h2 != 1)
else 0
```

The second run confirms that this rule classifies 62 of 358 firms as fragile and matches the processed outcome exactly.

## Construct-validity issue

The computational rule is transparent, but the substantive labels need caution:

- `h1`: new products/services introduced over the last three years
- `h2`: new products/services also new for the establishment's main market
- `h5`: new or significantly improved process over the last three years
- `c22b`: establishment has its own website
- `l1`: permanent full-time employees at the end of the last fiscal year

Older Word drafts describe some variables as revenue volatility and digital-platform difficulty. The papers should use the official WBES labels unless the team recovers the original recoding logic.

## LASSO model logic

The LASSO-logit model uses thirteen curated predictors and a stratified train-test split. The second run confirms high held-out discrimination:

- Accuracy: 0.967
- Precision: 0.882
- Recall: 0.938
- Specificity: 0.973
- ROC-AUC: 0.978

This confirms the model pipeline, but the result should be flagged for improvement. Some predictors are close to or identical with variables used in the recovered classification rule. The model therefore validates the mechanics of the screening rule more than it discovers independent determinants of fragility.

## Leakage-reduced fix

The second-run workflow now estimates an additional LASSO model excluding the rule variables available in the predictor file: `h1`, `h2`, `h5`, and `c22b`. This gives a more honest internal benchmark:

- Accuracy: 0.611
- Precision: 0.279
- Recall: 0.750
- Specificity: 0.581
- ROC-AUC: 0.770

The corrected interpretation is: the full model audits the recovered rule; the leakage-reduced model provides the internal predictive benchmark; a future externally validated model requires an independent outcome such as closure, employment contraction, sales decline, or follow-up survival.

## Weighting logic

Paper 2 uses three WBES weight variables:

- `wmedian`
- `wstrict`
- `wweak`

The second run confirms:

| Approach | Fragility percent |
|---|---:|
| Unweighted | 17.32 |
| wmedian | 21.33 |
| wstrict | 20.95 |
| wweak | 21.56 |

The weighted estimates are higher than the sample estimate, supporting the claim that national formal-firm interpretation requires weights.

## Current empirical claims

Supported:

- The raw `.dta` file contains 358 observations and 355 variables.
- The CSV row count matches the Stata file.
- The recovered rule exactly reproduces the supplied classification.
- Weighted formal-firm fragility is roughly 21 percent.
- Fragility differs strongly by region, with lower weighted prevalence in Kigali and higher prevalence in the Southern and Eastern stratum.
- The LASSO pipeline reproduces high apparent discrimination.

Needs improvement:

- The current outcome is a screening construct, not a validated failure measure.
- LASSO performance should not be used as independent causal evidence.
- Omega-score results should remain exploratory until reconstructed from raw variables.
- Design-based uncertainty estimates are still needed.
- Spatial, informal-sector, and digital-finance papers need external data before full claims can be made.
