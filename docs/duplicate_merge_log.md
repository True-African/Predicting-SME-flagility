# Duplicate and Overlap Log

## Confirmed duplicate or near-duplicate materials

| Material | Decision | Reason |
|---|---|---|
| `classification 1.xlsx`, `duplicates/classification.xlsx`, `duplicates/classification 11.xlsx` | Kept converted `data/processed/classification_probabilities.csv`; deleted duplicate Excel copies after cleanup audit | Same structure, same 358 observations, same risk distribution and predicted probabilities. |
| `duplicates/selected_data.xlsx` | Deleted after cleanup audit | Same 358 observations and probability values under `p_hat`; superseded by open CSV outputs. |
| `Results Tables/fragility_model_results.docx`, `duplicates/logit_model_results.docx`, `duplicates/marginal_effects.docx`, `duplicates/marginal_effects 1.docx` | Deleted after cleanup audit | Word tables duplicate older model outputs and are superseded by regenerated CSV/TEX tables. |
| Root ROC image variants and Stata `.gph` files | Deleted after cleanup audit | The reproducible notebook now regenerates current PNG figures; Stata `.gph` files require proprietary software and were not used by the manuscripts. |
| `Full Paper 1.docx`, `Full paper 2.docx`, `Lasso paper.docx` | Preserved in `docs/drafts/original_word` | They overlap substantially. `Full paper 2` is the strongest current narrative draft; `Lasso paper` is a strategy/draft accumulation file. |

## Important consistency notes

The Word drafts and old Stata tables do not fully agree on selected variables and labels. Some tables describe `h5` and `c22b` as revenue volatility and digital difficulty, while the official Stata labels identify them as process innovation and own website. The new reproducible notebook records the active variable names, variable labels, and exact recovered classification rule.

The converted `omega_score.csv` file has a constant `omega_score` column equal to the sample prevalence. The manuscript therefore uses `classification_probabilities.csv` as the probability source and treats the constant omega score as a legacy export requiring correction.
