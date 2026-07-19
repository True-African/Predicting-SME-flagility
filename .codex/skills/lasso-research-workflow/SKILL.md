---
name: lasso-research-workflow
description: Audit, reproduce, package, and preserve the LASSO Rwanda SME fragility research project. Use when working in a LASSO-style research folder with Enterprise Survey raw data, Python/Stata analyses, LaTeX and DOCX manuscripts, APA 7 references, generated tables/figures, or a GitHub backup/release workflow.
---

# LASSO Research Workflow

Use this skill to continue the Rwanda SME fragility research project without losing data, manuscript history, or reproducibility. Treat the project as a research archive first and an analysis workspace second.

## Safety Rules

- Preserve original files. Archive before destructive changes.
- Do not fabricate data, results, citations, DOIs, or claims.
- Clearly separate raw data, processed data, generated outputs, manuscripts, and documentation.
- Treat raw Enterprise Survey data, Word drafts, and logs as potentially sensitive.
- Prefer private GitHub repositories unless the user explicitly requests public.
- Use Git LFS for binary research artifacts when configured.
- Do not push secrets, credentials, API keys, private tokens, or unreviewed confidential material.

## Expected Project Structure

Use and preserve this structure when present:

```text
data/raw/
data/processed/
code/python/
code/notebooks/
code/stata/
results/tables/
results/figures/
results/models/
results/stata/
papers/paper_1/
papers/paper_2/
docs/
archive/
```

## Core Workflow

1. Scan the folder with `rg --files`, `Get-ChildItem`, and `git status -sb`.
2. Read existing docs before changing research claims: `docs/reproducibility_guide.md`, `docs/final_research_report.md`, `docs/second_run_final_report.md`, `docs/classification_rule_recovery.md`, and `docs/stata_python_result_comparison.md`.
3. Audit data provenance: raw `.dta`, converted CSV, variable-label CSV, and processed analysis data.
4. Reproduce analysis using `code/notebooks/01_reproducible_analysis_and_research_expansion.ipynb`, `code/python/02_second_run_raw_analysis.py`, and `code/stata/01_raw_data_second_run.do`.
5. Compare generated tables and figures against manuscript claims.
6. Update papers only after confirming result files.
7. Compile LaTeX papers and regenerate editable DOCX files when manuscript sources change.
8. Update documentation and Git backup reports before committing.

## Fragility Outcome Protocol

- The operative outcome is `fragility_risk_flex`.
- The recovered rule is a constructed screening classification, not observed survival, closure, bankruptcy, or financial distress.
- Official Stata/WBES labels are authoritative when they conflict with legacy draft labels.
- Outcome-rule variables include `h1`, `h2`, `h5`, `c22b`, and `l1`.
- Models that include `h1`, `h2`, `h5`, or `c22b` should be interpreted as screening-rule replication because of predictor-outcome leakage.
- The leakage-reduced model is the stronger benchmark for independent predictive signal.

## Manuscript Protocol

For Paper 1, use `papers/paper_1/main.tex`, `papers/paper_1/sections/*.tex`, `papers/paper_1/references.bib`, `papers/paper_1/Paper_1_word_complete_source.md`, and `papers/paper_1/Paper_1_editable.docx`.

Use cautious social-science language:

- Say "predictive signals" rather than "drivers" unless a causal design exists.
- Say "constructed fragility classification" rather than "survival outcome."
- Define all abbreviations on first use.
- Explain every formula parameter with "where ..." text.
- Discuss each table and figure in the surrounding section.
- Keep tables and figures inside relevant sections, before references.

For APA 7:

- Use `apa7` and `biblatex-apa`.
- Compile with `biber`, not BibTeX.
- Include DOI or stable source URL where available.
- Do not keep uncited references without a deliberate reason.

## Reproducibility Commands

From `papers/paper_1/`:

```powershell
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Regenerate the editable Word document from `papers/paper_1/`:

```powershell
pandoc Paper_1_word_complete_source.md --from markdown+tex_math_dollars --to docx --resource-path=".;..\..;..\..\results\figures;..\..\results\figures\second_run;..\..\results\tables" --citeproc --bibliography=references.bib --output="Paper_1_editable.docx"
```

Then reapply Word formatting if needed: justified paragraphs, no headers/footers, and readable table font sizes.

## GitHub Backup Protocol

Before pushing:

1. Run a secret scan over text files.
2. Confirm `.gitignore` excludes disposable files only.
3. Confirm `.gitattributes` tracks binary research artifacts with Git LFS when available.
4. Keep raw data in a private repository unless explicit public-release permission exists.
5. Run `git status -sb` and inspect staged files.
6. Do not use `git add .` if the worktree contains unrelated or sensitive unreviewed files.

Recommended branch: `backup/research-ready-lasso`

Recommended commit message: `Backup complete LASSO research project with reusable workflow skill`

## Quality Checklist

- Project inventory updated.
- Safety audit updated.
- Raw data, processed data, code, manuscripts, tables, figures, and docs accounted for.
- Paper 1 PDF and DOCX exist.
- Paper 2 PDF and source exist.
- Stata do-file exists.
- Notebook exists.
- References compile or documented if not checked.
- No secrets found in text scan.
- Sensitive data risk documented.
- GitHub repository is private unless the user explicitly chooses public.
