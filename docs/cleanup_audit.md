# Cleanup audit

Date: 2026-04-25

This audit records the dry-run cleanup used before deleting unused or superseded project files. The cleanup preserves raw data, converted CSV data, Word-source drafts, final PDFs, LaTeX sources, APA references, notebooks, generated research tables, generated research figures, and documentation.

## Deleted after dry run

### Regenerable LaTeX build files

These are compiler by-products produced by `pdflatex` and `biber`. They are not source files and can be regenerated from `main.tex`, the `.bib` file, tables, figures, and section files.

- `papers/paper_1/main.aux`
- `papers/paper_1/main.bbl`
- `papers/paper_1/main.bcf`
- `papers/paper_1/main.blg`
- `papers/paper_1/main.fdb_latexmk`
- `papers/paper_1/main.fff`
- `papers/paper_1/main.fls`
- `papers/paper_1/main.log`
- `papers/paper_1/main.out`
- `papers/paper_1/main.run.xml`
- `papers/paper_1/main.ttt`
- `papers/paper_2/main.aux`
- `papers/paper_2/main.bbl`
- `papers/paper_2/main.bcf`
- `papers/paper_2/main.blg`
- `papers/paper_2/main.fdb_latexmk`
- `papers/paper_2/main.fff`
- `papers/paper_2/main.fls`
- `papers/paper_2/main.log`
- `papers/paper_2/main.out`
- `papers/paper_2/main.run.xml`
- `papers/paper_2/main.synctex.gz`
- `papers/paper_2/main.ttt`

### Superseded legacy output files

These were older exploratory outputs or duplicate exports. The current papers and reproducible notebook use the rebuilt CSV/TEX tables and regenerated PNG figures instead.

- `results/tables/predicted_by_class.xlsx`
- `results/tables/fragility_model_results.docx`
- `results/figures/Figure1_Sample_Composition.png`
- `results/figures/Figure2_Confusion_Matrix_and_Metrics.png`
- `results/figures/Figure3_Predicted_Probability_Distribution.png`
- `results/figures/Figure4_Predictor_Comparison.png`
- `results/figures/Figure5_Digital_Exclusion.png`
- `results/figures/Figure6_Financial_Stress.png`
- `results/figures/Figure7_Firm_Characteristics.png`
- `results/figures/Figure8_Regression_Coefficient.png`
- `results/figures/Figure9_Missing_Data.png`
- `results/figures/Figure10_Research_Dashboard.png`
- `results/figures/graph_1_method_visual.jpg`
- `results/figures/roc_curve_initial.png`
- `results/figures/roc_curve_selected_useful.png`
- `results/figures/roc_fragility_model.png`

### Archived duplicate and proprietary-format working copies

These files were already classified as duplicate or superseded. They were removed to keep the project reproducible from open formats and retained source documentation.

- `archive/duplicates/`
- `archive/stata_graphs/`
- `archive/temp/~$ll paper 2.docx`
- `archive/temp/~WRL0003.tmp`

### Empty working folders

These folders had no active content after Python scripts were merged into the notebook.

- `code/scripts/`
- `code/utils/`
- `papers/paper_1/figures/`
- `papers/paper_1/tables/`

## Retained deliberately

- `data/raw/Rwanda-2023-full-data.dta`: retained as the original raw-data provenance file.
- `data/raw/Rwanda-2023-full-data.csv`: retained as the reproducible analysis copy.
- `docs/drafts/original_word/*.docx`: retained because these are original intellectual-source drafts, not disposable outputs.
- `docs/briefs/Email_to_Simeon.docx`: retained as project correspondence/provenance.
- `papers/paper_1/main.pdf` and `papers/paper_2/main.pdf`: retained as compiled manuscript previews.
- `results/figures/figure_*.png`, `results/tables/table_*.csv`, and `results/tables/table_*.tex`: retained because they are generated from the current notebook and feed the manuscripts.
- `.venv/`: retained because it may contain the local execution environment; environment deletion should be a separate explicit maintenance step.

## Current cleanup principle

The project now keeps source data, transparent analysis code, generated open-format outputs, APA 7 manuscript sources, and compiled previews. Legacy proprietary exports and regenerable compiler artifacts have been removed.
