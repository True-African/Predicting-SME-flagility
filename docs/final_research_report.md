# Final Research Report

## 1. Original Project Structure

The original root folder mixed raw data, processed Excel outputs, Word manuscript drafts, Stata graph files, PNG figures, model tables, duplicate files, and a Python virtual environment. The current cleaned project now has one consolidated research notebook and two APA 7 manuscript folders.

## 2. Files Reviewed

Reviewed materials include the Rwanda 2023 Stata dataset and converted CSV, three Word manuscript/strategy drafts, the collaborator brief, curated predictor CSVs, probability/classification exports, model-result Word tables, Stata graph files, PNG/JPG figures, and the progress notebook. A full generated inventory is available at `docs/inventory/file_inventory.md`.

## 3. Duplicates and Overlaps

The duplicate classification files and selected-data workbook encode the same 358 observations and probability distribution. Multiple Word model-result files contain identical tables. The manuscript drafts overlap strongly and appear to be iterations of one study rather than separate papers. Details are recorded in `docs/duplicate_merge_log.md`.

## 4. Reorganization Decisions

The project was reorganized into `data/`, `code/`, `results/`, `papers/`, and `docs/`. Raw data moved to `data/raw`; analysis inputs moved to `data/processed`; current figures and tables moved to `results`; Word drafts moved to `docs/drafts/original_word`. The original `.dta` file was converted to CSV, processed `.xlsx` files were converted to CSV and removed, duplicate/proprietary legacy outputs were deleted after a cleanup audit, and the two notebooks were merged into one reproducible notebook.

## 5. Recommended Analyses

The strongest immediate analysis is a predictive LASSO-logit model for firm fragility. Additional work recommended before journal submission includes validating the fragility index construction against the official WBES codebook, adding design-based standard errors, expanding robustness checks, and documenting how survey weights change national interpretation.

## 6. Proposed Papers

Two papers are now active from the available evidence.

**Paper 1:** Predicting SME Fragility in Rwanda: A Penalized Logistic Framework Using National Enterprise Data.

Research question: Which firm-level characteristics best predict SME fragility in Rwanda, and how well can a sparse predictive model classify fragile firms?

Contribution: The paper operationalizes fragility as a predictive risk construct and demonstrates that revenue volatility and digital platform difficulty dominate a sparse classification model.

Target field: entrepreneurship, development studies, SME policy, or applied social-science methods.

**Paper 2:** From Sample Prediction to Population Screening: Weighted Estimates of Formal-SME Fragility in Rwanda.

Research question: How does estimated formal-SME fragility change when WBES survey weights are applied?

Contribution: The paper moves from sample-level prediction to population-oriented prevalence estimates for formal firms and shows sensitivity across `wmedian`, `wstrict`, and `wweak`.

Target field: survey methodology, development policy, SME policy, or applied social-science methods.

Additional paper concepts are listed in `docs/best_next_papers.md`, but they require external spatial, formal/informal, digital-finance, or industrial-policy data before full manuscript development.

## 7. Generated LaTeX Manuscript

Paper 1 is in `papers/paper_1/main.tex` with sections in `papers/paper_1/sections/`. Paper 2 is in `papers/paper_2/main.tex`. Both use `apa7` and `biblatex-apa`, and both have compiled PDF previews.

## 8. Remaining Gaps Before Journal Submission

- Confirm the exact survey variable coding and labels against the World Bank Enterprise Survey codebook.
- Use `docs/classification_rule_recovery.md` to report the recovered exact outcome rule and resolve the mismatch between official Stata labels and Word-draft labels.
- Resolve inconsistencies in older Word drafts, especially the legacy reference to process innovation.
- Expand Paper 2 with design-based uncertainty estimates and a fuller survey-methods section.
- Add formal ethics/data availability statement required by the target journal.
- Add a complete citation audit and ensure every in-text citation appears in `references.bib`.
- Consider adding SHAP or tree-based models only after reproducible scripts produce validated outputs.

The best follow-on paper concepts are detailed in `docs/best_next_papers.md`.
