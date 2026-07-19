---
title: "Auditing and Predicting Constructed SME Fragility in Rwanda: A Penalized Logistic Screening Framework Using Enterprise Survey Data"
bibliography: references.bib
link-citations: true
---

# Auditing and Predicting Constructed SME Fragility in Rwanda: A Penalized Logistic Screening Framework Using Enterprise Survey Data

Stanley Mukasa^1*^ and Simeon Nsabiyumva^1^

^1*^Carnegie Mellon University Africa  
^1^African Leadership University

## *Abstract*

*Small and medium-sized enterprises are central to employment and structural transformation in Rwanda, yet many operate under market disruption, uneven digitalization, and constrained adaptive capacity. This paper audits and predicts a constructed firm-level fragility classification using the 2023 Rwanda Enterprise Survey. We recover the exact deterministic rule behind a legacy binary fragility indicator and show that it classifies 62 of 358 firms, or 17.3 percent of observations, as fragile. The recovered rule combines product/service innovation, process innovation, website status, and permanent full-time employment, exposing a central construct-validity problem: earlier project drafts label some of the same variables as revenue volatility and digital-platform difficulty. We therefore treat the official Stata labels as authoritative and interpret the outcome as a screening index rather than an observed survival, closure, or financial-distress measure. A least absolute shrinkage and selection operator (LASSO) logistic-regression pipeline is estimated with a held-out test split. The full model achieves an area under the receiver operating characteristic curve (ROC-AUC) of 0.978, but it includes variables used to construct the outcome and is therefore interpreted as screening-rule replication. The leakage-reduced benchmark excludes outcome-rule variables and yields ROC-AUC of 0.770, area under the precision-recall curve (PR-AUC) of 0.428, and accuracy of 61.1 percent. The central contribution is a reproducible audit workflow showing how constructed policy-screening indices should be validated before they are interpreted as measures of firm distress. The paper clarifies the validation, governance, and external-outcome evidence required before SME fragility scores can inform policy targeting.*

**Keywords:** small and medium-sized enterprise (SME) fragility, penalized logistic regression (LASSO), predictor-outcome leakage, construct validity audit, Enterprise Survey data, predictive screening, constructed outcome validation

# Introduction

Recent research on small and medium-sized enterprise (SME) resilience emphasizes that digitalization, innovation, and organizational learning increasingly shape how firms absorb disruption and adapt under crisis conditions [@sagala2024antifragility; @sinha2025digitalisation]. This contemporary concern builds on foundational development-economics evidence that SMEs are important engines of employment, innovation diffusion, and inclusive growth in developing economies [@beck2006small; @ayyagari2007small]. In Rwanda, as in many emerging economies, SMEs operate within a changing policy and market environment shaped by digital transformation, financial constraints, and recurrent demand shocks. These pressures make early identification of firm vulnerability a central policy concern, but realized closure or exit is often observed too late for preventive support.

This paper reframes SME vulnerability as a predictive fragility-screening problem. Rather than estimating the causal effect of a single intervention or predicting observed survival duration, we ask whether a constructed fragility classification can be reproduced, audited, and predicted transparently from enterprise-survey variables. Four questions organize the analysis: Can the legacy SME fragility classification be reconstructed from raw survey variables? To what extent does full-model performance reflect outcome-rule replication? How much independent predictive signal remains after removing outcome-rule variables? What governance conditions are required before such a score can inform policy? The distinction matters. A predictive model can support screening and prioritization even when cross-sectional data cannot identify causal effects [@shmueli2010explain].

The empirical setting is the Rwanda 2023 Enterprise Survey. The project folder contained raw survey data, curated predictor files, Stata-derived classification exports, draft manuscripts, and model figures. We reorganized these materials into a reproducible workflow and generated new Python and Stata outputs from the raw and curated analysis files. The resulting analysis uses 358 formal firms covered by the World Bank Enterprise Survey frame. The data should not be interpreted as covering all Rwandan SMEs, informal enterprises, microenterprises, or firms below the Enterprise Survey eligibility threshold.

The paper makes three contributions. First, it presents a transparent firm-level fragility-screening framework suitable for social-science research using cross-sectional enterprise data in a low-data African enterprise context. Second, it demonstrates why predictive performance must be interpreted alongside outcome construction: the full model validates the mechanics of the recovered index, while the leakage-reduced model provides the more substantively meaningful benchmark for independent predictive signal. Third, it provides a generalizable workflow for auditing constructed policy-screening outcomes in settings where index labels, variable coding, and predictive performance could otherwise produce misleading policy claims. The workflow can inform research on enterprise surveys, social registries, credit-screening indices, and development-program targeting tools when the outcome is constructed rather than directly observed.

# Literature Review

## SME Fragility and Resilience in Developing Economies

The literature on SMEs in developing economies emphasizes both their economic importance and their vulnerability to institutional and market constraints. Earlier work shows that small firms account for a large share of private-sector activity but often face limited access to finance, weak infrastructure, and policy uncertainty [@beck2006small; @ayyagari2007small]. Recent crisis-era evidence reinforces this point: firm resilience is shaped by liquidity, finance, technological capability, and the ability to reconfigure operations under disruption [@papadopoulos2020digital; @guo2020digitalization; @mishrif2023technology; @amadasun2022finance].

Research on firm resilience has increasingly moved beyond a simple failed/not-failed distinction. Organizational resilience studies view firms as having different capacities to anticipate, absorb, and adapt to shocks [@lengnickhall2005adaptive; @duchek2020organizational]. In this framing, fragility can be interpreted as limited adaptive capacity under stress rather than as realized exit. Recent work on digital transformation and resilience similarly treats resilience as a dynamic capability built through learning, innovation, leadership, and technology-enabled adaptation [@awad2024digital; @sagala2024toward; @sagala2024antifragility; @martinrojas2026resilience].

## Digitalization, Innovation, and Modernization Risk

Digitalization adds a further dimension. Firms that struggle to use digital tools may be less able to access customers, suppliers, payment systems, or information. Studies of SMEs during and after COVID-19 find that digital technologies supported crisis response, business continuity, and customer engagement, while also requiring complementary skills, finance, and organizational learning [@papadopoulos2020digital; @guo2020digitalization; @mishrif2023technology; @awad2024digital; @robertson2022digitalmaturity; @lestari2024business; @sinha2025digitalisation]. In emerging markets, this difficulty interacts with institutional voids such as uneven infrastructure, limited digital skills, and fragmented support systems [@khanna1997why]. The implication is not that digital presence or innovation is always protective. Modernization may also be reactive, costly, or incomplete when firms adopt new practices under pressure without the complementary resources needed to convert those practices into resilience.

## Predictive Modeling Versus Causal Inference in Firm-Risk Research

Methodologically, many SME risk studies use descriptive statistics or conventional regression. Penalized regression offers a useful middle ground between interpretability and prediction. LASSO shrinks weak predictors toward zero and is especially useful when researchers want sparse models from many plausible covariates [@tibshirani1996regression; @friedman2010regularization; @hastie2015sparsity]. Stata and Python implementations now make regularized regression relatively accessible for applied social science, but model selection still depends on transparent cross-validation, preprocessing, and outcome construction [@ahrens2020lassopack; @arlot2010crossvalidation]. In social-science applications, predictive performance should be interpreted carefully and separated from causal claims [@shmueli2010explain; @mullainathan2017machine; @athey2019machine].

## Constructed Indices, Leakage, and Auditability

The gap addressed by this paper is methodological as well as empirical. Development researchers often use constructed classifications because direct measures of closure, survival duration, or financial distress are unavailable. Such indices can be useful, but they require documentation of variable labels, coding direction, missing-value handling, and the relationship between index components and model predictors. When a model includes variables that are also used to construct the target outcome, high predictive accuracy may reflect index mechanics rather than independent empirical discovery [@kleinberg2018human]. This paper therefore contributes beyond applying LASSO to Rwanda Enterprise Survey data: it shows how to audit a constructed SME fragility index before treating it as evidence about firm distress or using it for policy screening.

# Theoretical Framework

The analysis is guided by organizational resilience, dynamic capabilities, and institutional voids theory. Organizational resilience theory frames fragility as limited capacity to absorb disruption and maintain function. Dynamic capabilities theory emphasizes the ability to sense, seize, and reconfigure resources under uncertainty [@teece1997dynamic]. Institutional voids theory explains why these firm-level capabilities may be especially consequential in emerging-market settings where finance, infrastructure, skills, and market-support systems are uneven [@khanna1997why].

The reconstructed outcome creates a theoretical puzzle. The official metadata indicate that the operative rule uses innovation, website status, and employment-size information. These variables are often interpreted as signs of capability, modernization, or organizational upgrading. Yet in the recovered screening index they are associated with a higher probability of being fragility-classified. This paper therefore interprets the empirical pattern as a fragility paradox of modernization rather than as evidence that innovation or digital presence causes fragility.

Several mechanisms could explain this paradox. First, innovation may be reactive: firms may introduce new products, services, or processes because they are under competitive or demand pressure, not because they are robust. Under this interpretation, innovation is a symptom of adaptation under stress. Second, growth-stage modernization may create liquidity strain, coordination costs, and managerial overload. A firm that is expanding, digitizing, or changing production processes may face short-run vulnerability even if its long-run prospects improve. Third, institutional incompleteness may limit the returns to digital and process upgrading when finance, infrastructure, skills, and market systems are uneven. Fourth, a website or process change may signal partial modernization rather than full digital maturity. Finally, part of the paradox may be a screening-rule artifact produced by the construction of the dependent variable itself. Future evidence could distinguish these mechanisms by linking the screening index to longitudinal outcomes, investment costs, credit constraints, digital usage intensity, and post-survey firm survival.

This framework leads to a cautious interpretation. The model identifies predictive signals of a constructed fragility classification. It does not show that innovation, website ownership, or employment levels cause fragility. The main theoretical contribution is to show how a capability-oriented screening rule can generate interpretive ambiguity unless variable labels, index construction, and predictive validation are audited together.

# Data, Measurement, and Construct Validity

## Data

The study uses the Rwanda 2023 Enterprise Survey raw Stata file and curated predictor files provided in the project folder [@worldbank2025rwanda]. The raw file was converted to CSV, variable labels were extracted, and the analysis was rerun from the original `.dta' file using both Python and Stata. The reproducible analysis dataset contains 358 formal-firm observations, a recovered binary fragility classification, predicted probabilities from the legacy classification export, and thirteen firm-level predictors. The inference frame is the formal-firm Enterprise Survey universe. The data do not represent all Rwandan SMEs, informal enterprises, microenterprises, or firms below the Enterprise Survey eligibility threshold.

## Outcome Reconstruction

The dependent variable is `fragility_risk_flex`. It equals one for firms classified as fragile by the legacy export and zero otherwise. We recovered the deterministic rule behind this classification by auditing the converted raw CSV and then rerunning the reconstruction from the raw Stata file. Let $Y_i$ denote the recovered fragility classification. Using the raw survey codes, the current operative rule is:

$$

Y_i =
I
\left[
\begin{array}{l}
(h5_i = 1 \land l1_i \leq 3) \ \lor \\
(h5_i = 2 \land c22b_i = 1 \land l1_i \leq -2) \ \lor \\
(h5_i = 2 \land c22b_i = 2 \land (h1_i = 2 \lor h2_i \neq 1))
\end{array}
\right].

$$

The rule classifies 62 firms as fragile and 296 as non-fragile. It reproduces all 358 classifications with no mismatches. This is an important transparency gain, but it also means the dependent variable is a constructed screening index rather than an observed event such as closure, bankruptcy, revenue decline, or survival duration.

In the outcome-rule equation, $Y_i$ is the binary fragility classification for firm $i$, where $Y_i = 1$ means that firm $i$ is classified as fragile and $Y_i = 0$ means that it is not classified as fragile. The expression $I[\cdot]$ is an indicator function: it takes the value 1 when the condition inside the brackets is true and 0 when the condition is false. The symbol $i$ indexes firms. The logical connector $\land$ means "and," while $\lor$ means "or." For the binary rule variables, the raw World Bank Enterprise Survey coding is interpreted as 1 = Yes and 2 = No. Thus, `h5 = 1` means the establishment introduced a new or significantly improved process, `c22b = 1` means the establishment has its own website, and `h1 = 2` or `h2 = 2` indicate negative responses to the corresponding product/service innovation questions. The employment condition uses `l1`, the number of permanent full-time employees at the end of the last fiscal year. The recovered rule is reported exactly as found in the legacy classification logic, including the unusual `l1 <= -2` branch. In the observed data this branch does not change the final reconstruction; it remains in the equation to preserve transparency and to avoid silently rewriting the legacy export. Nonresponse codes such as don't know, refusal, or not applicable were not recoded into substantive categories for the rule reconstruction; where present, they are treated according to the numeric values in the raw file and flagged as a validation issue for future questionnaire-level review.

## Construct Validity and Variable-Label Audit

Table 1 below reports the variable-label audit. The official Stata labels identify $h1$ and $h2$ as product/service innovation variables, $h5$ as process innovation, $c22b$ as website status, and $l1$ as permanent full-time employment. Earlier project drafts describe $h5$ as revenue volatility and $c22b$ as digital-platform difficulty. The official labels are treated as authoritative in this manuscript. Therefore, the paper avoids strong claims about revenue volatility or digital-platform difficulty unless those terms are explicitly identified as legacy labels requiring further documentation.

**Table 1: Construct Validity and Variable-Label Audit**

| p{1.5cm}>{\RaggedRight\arraybackslash}p{4.2cm}>{\RaggedRight\arraybackslash}p{4.0cm}>{\RaggedRight\arraybackslash}p{5.0cm}} \ Variable code | Official WBES/Stata label | Legacy and final interpretation | Role in outcome rule and implication for theory |
| --- | --- | --- | --- |
| \ Variable code | Official WBES/Stata label | Legacy and final interpretation | Role in outcome rule and implication for theory |
| h1 | New Products/Services Introduced Over Last 3 Yrs | Legacy label: product/service innovation. Final interpretation: product/service innovation status. | Used in the third branch when h5=2 and c22b=2. Theoretically, it should be interpreted as modernization status, not financial distress. |
| h2 | New Products/Services Also New For Thr Establishment'S Main Market | Legacy label: new-to-market innovation. Final interpretation: market novelty of innovation. | Used in the third branch when h5=2 and c22b=2. It signals innovation depth but has missingness; causal claims should be avoided. |
| h5 | During Last 3 Yrs, Establishment Introduced New/Significantly Improved Process | Legacy label: revenue volatility. Final interpretation: process innovation status. | Used in all three branches. This is the central construct-validity tension; any revenue-volatility interpretation requires a documented recode. |
| c22b | Establishment Has Its Own Website | Legacy label: digital-platform difficulty. Final interpretation: own-website status. | Used in the second and third branches. It is a digital-presence indicator, not direct evidence of platform difficulty. |
| l1 | Num. Permanent, Full-Time Employees At End of Last Fiscal Year | Legacy label: employment vulnerability. Final interpretation: permanent full-time employment count. | Used in the first and second branches. It supports a size-related screening interpretation. |

The implication of Table 1 is that the construct should be described as a fragility-screening classification built from innovation, digital-presence, and employment-size variables. It should not be described as a direct measure of financial distress, revenue volatility, or digital-platform difficulty unless the research team later supplies a defensible recoding from the original questionnaire or Stata workflow.

## Alternative Fragility Index Logic

The Word draft preserved in the project archive gives a broader mathematical rationale for a possible finance-digital fragility index. Let $F_i$ denote firm $i$'s financial-access score, $D_i$ its digital-presence score, and $E_i$ its e-commerce-adoption score, with each component scaled to the interval $[0,1]$. The draft logic defines risk flags as:

$$
\begin{aligned}

R^{F}_i &= I(F_i < 0.25),\\
R^{D}_i &= I(D_i < 0.30),\\
R^{E}_i &= I(E_i < 0.10).

\end{aligned}
$$

In the risk-flag equations, $R^{F}_i$, $R^{D}_i$, and $R^{E}_i$ are binary risk flags for firm $i$. They equal 1 when the firm's financial-access, digital-presence, or e-commerce-adoption score falls below the stated threshold, and 0 otherwise. The superscripts $F$, $D$, and $E$ refer to finance, digital presence, and e-commerce, respectively. The thresholds 0.25, 0.30, and 0.10 come from the archived Word-draft logic and are not estimated from the current data.

The binary Fragility Risk Index is then:

$$

\text{Fragility}_i =
I\left[
(R^{F}_i R^{D}_i) + (R^{F}_i R^{E}_i) + (R^{D}_i R^{E}_i) \geq 1
\right].

$$

In this alternative-index equation, $\text{Fragility}_i$ is the alternative binary fragility index for firm $i$. The products $R^{F}_iR^{D}_i$, $R^{F}_iR^{E}_i$, and $R^{D}_iR^{E}_i$ identify whether the firm is simultaneously flagged in at least two of the three domains. The condition $\geq 1$ therefore means that a firm is classified as fragile when any two-domain combination of finance, digital-presence, and e-commerce risk is present.

This alternative rule is theoretically consistent with a finance-digital capability view of fragility, but the notebook shows that it classifies 104 firms as fragile and agrees with the supplied outcome in 76.5 percent of cases. It is therefore reported as a candidate robustness extension, not as the operative dependent-variable definition.

## Predictors and Leakage Map

Predictors include innovation indicators, employment, temporary employment change, capacity utilization, internet use for business, finance indicators, payment-delay variables, website/digital-presence indicators, e-payment share, sector, firm size, and managerial experience. Table 2 below separates variables used in the outcome rule from variables submitted as predictors. Four rule variables, `h1`, `h2`, `h5`, and `c22b`, also appear in the predictor set. This creates high leakage risk for the full model. The full model is therefore interpreted as screening-rule replication, while the leakage-reduced model is treated as the more substantive benchmark for independent predictive signal.

**Table 2: Outcome-Rule and Predictor Leakage Map**

| Variable | Used in outcome rule | Used as predictor | Leakage risk |
| --- | --- | --- | --- |
| a4a | No | Yes | Low |
| a6a | No | Yes | Low |
| b6 | No | Yes | Low |
| c22b | Yes | Yes | High |
| h1 | Yes | Yes | High |
| h2 | Yes | Yes | High |
| h5 | Yes | Yes | High |
| h8 | No | Yes | Low |
| k162 | No | Yes | Low |
| k33 | No | Yes | Low |
| k3a | No | Yes | Low |
| k3bc | No | Yes | Low |
| k82 | No | Yes | Low |
| l1 | Yes | No | Rule-only |

Table 3 below documents the full predictor set used in the screening models. This dictionary is necessary because several short Enterprise Survey codes are not self-interpreting. It also clarifies which variables enter both the full and leakage-reduced specifications and how binary 1/2 coding should be read.

**Table 3: Predictor Dictionary, Coding Direction, and Model Inclusion**

| p{1.3cm}>{\RaggedRight\arraybackslash}p{5.3cm}>{\RaggedRight\arraybackslash}p{3.0cm}>{\RaggedRight\arraybackslash}p{4.8cm}} \ Code | Official label and coding direction | Model inclusion | Interpretation notes |  |
| --- | --- | --- | --- | --- |
| \ Code | Official label and coding direction | Model inclusion | Interpretation notes |  |
| `a4a` | Industry sampling sector; categorical survey code. | Full model: Yes. Leakage-reduced: Yes. | Low leakage; used to capture industry composition. |  |
| `a6a` | Sampling size; categorical survey size band. | Full model: Yes. Leakage-reduced: Yes. | Low leakage; not the same as `l1`, which enters the rule. |  |
| `b6` | Full-time employees when establishment started operations; count. | Full model: Yes. Leakage-reduced: Yes. | Employment-history predictor selected in the leakage-reduced model; interpreted as a predictive signal, not a causal effect. |  |
| `c22b` | Establishment has its own website; 1 = Yes, 2 = No. | Full model: Yes. Leakage-reduced: No. | Digital-presence variable used in the outcome rule; high leakage risk in the full model. |  |
| `h1` | New products/services introduced over last 3 years; 1 = Yes, 2 = No. | Full model: Yes. Leakage-reduced: No. | Innovation variable used in the outcome rule; high leakage risk in the full model. |  |
| `h2` | New products/services also new for the establishment's main market; 1 = Yes, 2 = No. | Full model: Yes. Leakage-reduced: No. | Innovation-novelty variable used in the outcome rule; high leakage risk in the full model. |  |
| `h5` | Introduced new/significantly improved process over last 3 years; 1 = Yes, 2 = No. | Full model: Yes. Leakage-reduced: No. | Process-innovation variable used in the outcome rule; high leakage risk in the full model. |  |
| `h8` | Spent on R\ | D during last fiscal year; 1 = Yes, 2 = No. | Full model: Yes. Leakage-reduced: Yes. | Low leakage; selected in the leakage-reduced model. |
| `k162` | Applied for new loans/lines of credit in last fiscal year; 1 = Yes, 2 = No. | Full model: Yes. Leakage-reduced: Yes. | Credit-demand variable; low leakage and selected in the leakage-reduced model. |  |
| `k33` | Percentage of payments received using e-payments; percentage. | Full model: Yes. Leakage-reduced: Yes. | Digital-finance variable; low leakage and selected in the leakage-reduced model. |  |
| `k3a` | Working capital financed from internal funds/retained earnings; percentage. | Full model: Yes. Leakage-reduced: Yes. | Finance-source variable; low leakage and selected in the leakage-reduced model. |  |
| `k3bc` | Working capital borrowed from banks; percentage. | Full model: Yes. Leakage-reduced: Yes. | Finance-source variable; low leakage and selected in the leakage-reduced model. |  |
| `k82` | Has a line of credit or loan from a financial institution; 1 = Yes, 2 = No. | Full model: Yes. Leakage-reduced: Yes. | Formal-finance variable; low leakage and selected in the leakage-reduced model. |  |
| `l1` | Permanent full-time employees at end of last fiscal year; count. | Full model: No. Leakage-reduced: No. | Rule-only variable in the recovered classification; not submitted as a predictor in the curated file. |  |

## Empirical Strategy

The primary model is a cross-validated L1-penalized logistic regression, commonly known as least absolute shrinkage and selection operator (LASSO) logistic regression. LASSO is appropriate here because the analysis contains multiple plausible firm-level predictors, a modest sample size, and a need for an interpretable screening model. LASSO shrinks weak predictors toward zero while retaining a smaller set of variables with predictive value, making it useful when the research objective is sparse prediction rather than causal parameter estimation [@tibshirani1996regression; @friedman2010regularization; @hastie2015sparsity]. Five-fold cross-validation selects the penalty level, reducing dependence on a single arbitrary tuning choice [@arlot2010crossvalidation; @ahrens2020lassopack].

Formally, the estimator solves the penalized logistic objective

$$

\hat{\beta} =
\arg\min_{\beta}
\left[
-\ell(\beta; y, X) + \lambda \sum_{j=1}^{p} |\beta_j|
\right],

$$

where $\hat{\beta}$ is the vector of estimated model coefficients after penalization, and $\beta$ is a candidate vector of coefficients considered during estimation. The notation $\arg\min_{\beta}$ means "the value of $\beta$ that minimizes" the expression that follows. In practical terms, the model chooses the coefficient vector that gives the best penalized fit to the training data. The term $\ell(\beta; y, X)$ is the logistic log-likelihood, which measures how well the coefficients $\beta$ predict the observed outcome vector $y$ from the predictor matrix $X$. Here, $y$ contains the binary fragility classifications and $X$ contains the preprocessed firm-level predictors. The minus sign before $\ell(\beta; y, X)$ appears because the estimator is written as a minimization problem: minimizing the negative log-likelihood is equivalent to maximizing the log-likelihood. The parameter $\lambda$ is the nonnegative penalty level selected by five-fold cross-validation within the training data. Larger values of $\lambda$ impose stronger shrinkage. The summation $\sum_{j=1}^{p} |\beta_j|$ is the L1 penalty, where $j$ indexes predictors, $p$ is the total number of predictors, and $|\beta_j|$ is the absolute value of the coefficient for predictor $j$. Numeric predictors are standardized before estimation; reported coefficients are therefore penalized standardized coefficients from the fitted LASSO pipeline rather than post-LASSO unpenalized logit estimates. Because `class_weight = balanced` is used to improve minority-class detection, the predicted scores should be interpreted primarily as rankings unless recalibrated and externally validated.

The workflow uses a stratified 75/25 train-test split with random seed 42. Numeric features are median-imputed and standardized inside the training pipeline. Logistic regression is estimated with class balancing through `class_weight = balanced`. The main held-out test set contains 90 firms, including 16 fragility-classified firms. Predictive performance is evaluated with accuracy, precision, recall, specificity, the area under the receiver operating characteristic curve (ROC-AUC), the area under the precision-recall curve (PR-AUC), Brier score, calibration plots, threshold sensitivity, and bootstrap confidence intervals for ROC-AUC and PR-AUC.

Two model specifications are reported. The full model includes all curated predictors and is interpreted as a replication audit of the screening rule. The leakage-reduced model excludes the rule variables available in the predictor file: `h1`, `h2`, `h5`, and `c22b`. This second model asks whether other firm characteristics carry predictive information beyond the mechanics of the recovered rule. A complete-case audit is also generated: the leakage-reduced predictor set retains 347 of 358 observations before imputation, including 61 fragility-classified firms.

The analysis is not designed for causal inference. Coefficients are interpreted as predictive weights conditional on the model specification and data-generating workflow. Before policy deployment, the recovered classification should be validated against independent outcomes such as firm exit, revenue decline, employment contraction, or follow-up survival status.

## Reproducibility and Code Availability

The analysis workflow is documented in the project reproducibility guide and implemented in the cleaned notebook and second-run scripts. The key reproducibility settings are the Rwanda 2023 Enterprise Survey raw data source, the recovered classification rule above, the curated predictor dictionary in Table 3, median imputation for numeric variables, standardization inside the training pipeline, a stratified 75/25 train-test split, random seed 42, five-fold cross-validation for the LASSO penalty, and class-balanced logistic estimation. The manuscript tables and figures are generated from the project results folders rather than entered manually. This design allows the screening-rule reconstruction, leakage-reduced benchmark, calibration diagnostics, and threshold analysis to be rerun when updated data or external validation outcomes become available.

# Results

## Sample Profile and Outcome Reconstruction

Table 4 below reports the core sample structure. The study includes 358 formal firms, of which 62 are fragility-classified and 296 are not fragility-classified. The resulting prevalence is 17.3 percent. This table defines the empirical scale of the study: the analysis audits a formal-firm screening outcome within the Enterprise Survey sample, not all enterprises in Rwanda.

**Table 4: Sample Summary**

| Measure | Value |
| --- | --- |
| Observations | 358 |
| Fragility-classified firms | 62 |
| Non-fragility-classified firms | 296 |
| Mean predicted probability | 0.173 |

Table 5 below reports the second-run validation of the recovered rule. The reconstructed rule matches the supplied processed outcome for all 358 observations, with no mismatches. This result is foundational for the paper because it removes dependence on an unexplained legacy export and makes the dependent variable auditable.

**Table 5: Second-Run Fragility Rule Validation**

| n | supplied_fragile | second_run_fragile | matches | mismatches | agreement |
| --- | --- | --- | --- | --- | --- |
| 358 | 62 | 62 | 358 | 0 | 1.00 |

Table 6 below compares fragility-classified and non-fragility-classified firms using the curated legacy analysis dataset. The table shows large differences in the variables originally labelled as revenue volatility and digital difficulty, and in mean predicted probability. However, the official Stata labels show that the corresponding raw variables are process innovation and website status. The contribution of Table 6 is therefore diagnostic: it demonstrates why legacy labels must be reconciled with official survey metadata before substantive claims are made.

**Table 6: Descriptive Profile by Fragility Classification**

| fragility_label | n | revenue_volatility_pct | digital_difficulty_pct | mean_predicted_probability | mean_manager_experience |
| --- | --- | --- | --- | --- | --- |
| Fragility-classified | 62 | 98.4 | 98.4 | 0.807 | 8.8 |
| Not fragility-classified | 296 | 29.1 | 38.5 | 0.040 | 27.4 |

## Screening-Rule Replication and Independent Predictive Benchmark

Table 7 below presents the central empirical comparison. The full model, labelled as screening-rule replication, achieves ROC-AUC of 0.978 and PR-AUC of 0.952. These values show that the LASSO-logit pipeline can reproduce the constructed screening rule very well. However, the full model includes variables used to construct the outcome. Its high performance should therefore be interpreted as evidence that the rule has been replicated, not as independent predictive discovery.

The leakage-reduced benchmark excludes `h1`, `h2`, `h5`, and `c22b`. This model achieves ROC-AUC of 0.770, PR-AUC of 0.428, and accuracy of 61.1 percent. The performance gap between the two specifications is the main empirical result. It shows that the recovered rule carries substantial mechanical signal, while the remaining firm characteristics retain only moderate independent predictive information.

**Table 7: Full and Leakage-Reduced Model Performance**

| Metric | Screening-rule replication | Leakage-reduced benchmark |
| --- | --- | --- |
| ROC-AUC | 0.978 | 0.770 |
| PR-AUC | 0.952 | 0.428 |
| Brier score | 0.038 | 0.215 |
| Accuracy | 0.967 | 0.611 |
| Precision | 0.882 | 0.279 |
| Recall | 0.938 | 0.750 |
| Specificity | 0.973 | 0.581 |
| Test observations | 90 | 90 |

Figure 1 below shows the receiver operating characteristic curve for the full model using the second-run raw-data reconstruction. The test set contains 90 firms, including 16 fragility-classified firms, and the model includes outcome-rule variables. As shown in Figure 1, the curve lies close to the upper-left region of the plot. This confirms strong replication of the screening rule across classification thresholds.

![Figure 1: Screening-rule replication ROC curve, test set n=90, rule variables included](D:/Research/LASSO/results/figures/second_run/second_run_lasso_roc.png)

Figure 2 below shows the ROC curve for the leakage-reduced model. As shown in Figure 2, the curve remains above the diagonal line of no discrimination but is substantially weaker than the full-model curve. This figure contributes to the social-science interpretation of the results by showing that the project contains some predictive signal beyond the rule variables, but not enough to support strong policy claims without external validation.

![Figure 2: Leakage-reduced ROC curve, test set n=90, outcome-rule variables excluded](D:/Research/LASSO/results/figures/second_run/second_run_lasso_no_rulevars_roc.png)

## Calibration, Threshold Sensitivity, and Subgroup Performance

Figure 3 below reports the calibration plot for the leakage-reduced benchmark. Calibration evaluates whether predicted probabilities correspond to observed fragility-classification rates. As shown in Figure 3, the upper probability bins overstate observed fragility rates. This matters because class balancing improves classification of the minority class but can reduce probability calibration. The Brier score in Table 7 should therefore be interpreted alongside the ROC-AUC and PR-AUC, not as a deployment-ready probability estimate.

![Figure 3: Leakage-reduced calibration plot, test set n=90](D:/Research/LASSO/results/figures/second_run/second_run_lasso_no_rulevars_calibration.png)

Figure 4 below reports the precision-recall curve for the leakage-reduced benchmark. Because only 17.3 percent of firms are fragility-classified, PR-AUC is especially informative: it evaluates performance for the minority class more directly than accuracy. As shown in Figure 4, the leakage-reduced model performs above the prevalence baseline but remains far below the full screening-rule replication model. This reinforces the conclusion that independent predictive signal is moderate rather than decisive.

![Figure 4: Leakage-reduced precision-recall curve, test set n=90](D:/Research/LASSO/results/figures/second_run/second_run_lasso_no_rulevars_precision_recall.png)

Table 8 below reports threshold sensitivity for the leakage-reduced benchmark. Lower thresholds identify more fragility-classified firms but generate many false positives. At a 0.30 threshold, recall reaches 100 percent but specificity is only 26 percent. At a 0.70 threshold, specificity rises to 92 percent but recall falls to 38 percent. This table contributes directly to policy interpretation: no single threshold is universally correct, and any operational cutoff should depend on whether the policy objective prioritizes broad diagnostic outreach or more selective intervention.

**Table 8: Leakage-Reduced Threshold Sensitivity**

| threshold | accuracy | precision | recall | specificity | true_positives | false_positives | true_negatives | false_negatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.30 | 0.39 | 0.23 | 1.00 | 0.26 | 16 | 55 | 19 | 0 |
| 0.40 | 0.47 | 0.24 | 0.94 | 0.36 | 15 | 47 | 27 | 1 |
| 0.50 | 0.61 | 0.28 | 0.75 | 0.58 | 12 | 31 | 43 | 4 |
| 0.60 | 0.74 | 0.36 | 0.56 | 0.78 | 9 | 16 | 58 | 7 |
| 0.70 | 0.82 | 0.50 | 0.38 | 0.92 | 6 | 6 | 68 | 10 |

Table 9 below reports leakage-reduced test-set performance by region, sector, and firm size. The estimates should be read cautiously because some cells are small; for example, the large-firm test subgroup contains no fragility-classified firms. These subgroup results are descriptive diagnostics only, not evidence of stable differences in model fairness or performance. Still, the table is useful as an initial fairness and stability screen. It shows that accuracy, precision, and recall vary across subgroups, which means future versions of the model should report subgroup confidence intervals, bootstrapped uncertainty, and bias audits before any policy deployment.

**Table 9: Leakage-Reduced Subgroup Performance**

| group | category | test_n | fragile_n | accuracy | precision | recall | specificity | mean_predicted_probability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Region | Kigali | 33 | 1 | 0.67 | 0.08 | 1.00 | 0.66 | 0.38 |
| Region | Southern and Eastern | 29 | 9 | 0.66 | 0.47 | 0.78 | 0.60 | 0.51 |
| Region | Western and Northern | 28 | 6 | 0.50 | 0.25 | 0.67 | 0.45 | 0.50 |
| Sector | Manufacturing | 30 | 3 | 0.70 | 0.20 | 0.67 | 0.70 | 0.38 |
| Sector | Other Services | 38 | 8 | 0.63 | 0.35 | 0.88 | 0.57 | 0.48 |
| Sector | Retail | 22 | 5 | 0.45 | 0.23 | 0.60 | 0.41 | 0.53 |
| Firm size | Large | 14 | 0 | 1.00 | 0.00 | 0.00 | 1.00 | 0.12 |
| Firm size | Medium | 33 | 5 | 0.64 | 0.23 | 0.60 | 0.64 | 0.47 |
| Firm size | Small | 43 | 11 | 0.47 | 0.30 | 0.82 | 0.34 | 0.57 |

## Selected Predictive Signals and the Fragility Paradox

Table 10 below reports the largest full-model coefficients from the second-run workflow. The largest weights correspond to `h5`, `c22b`, and `h1`, which are all connected to the recovered outcome rule. This table helps explain why the full model performs so strongly: it is recovering rule mechanics rather than identifying independent predictive relationships.

**Table 10: Screening-Rule Replication Coefficients**

| predictor | coefficient | abs_coefficient |
| --- | --- | --- |
| h5 | 2.00 | 2.00 |
| c22b | 1.95 | 1.95 |
| h1 | 0.42 | 0.42 |
| k162 | 0.14 | 0.14 |
| k82 | 0.09 | 0.09 |
| h8 | 0.00 | 0.00 |
| h2 | 0.00 | 0.00 |
| k3a | 0.00 | 0.00 |
| k3bc | 0.00 | 0.00 |
| k33 | 0.00 | 0.00 |
| a4a | 0.00 | 0.00 |
| a6a | 0.00 | 0.00 |
| b6 | 0.00 | 0.00 |

Figure 5 below visualizes the same full-model coefficient pattern. As shown in Figure 5, process innovation and website-status variables dominate the classifier. This visual pattern is the empirical basis for the paper's construct-validity caution and for the modernization-fragility paradox discussed in the theoretical framework.

![Figure 5: Largest screening-rule replication coefficients](D:/Research/LASSO/results/figures/second_run/second_run_lasso_coefficients.png)

Table 11 below reports coefficients after the rule variables are removed. The largest remaining signal is `b6`, the number of full-time employees when the establishment started operations, followed by loan-application, e-payment, research-and-development, and working-capital variables. These results should be interpreted as predictive associations with a constructed classification. They suggest where future external validation should focus, but they do not establish causal pathways.

**Table 11: Leakage-Reduced Coefficients**

| predictor | coefficient | abs_coefficient |
| --- | --- | --- |
| b6 | -1.39 | 1.39 |
| k162 | 0.53 | 0.53 |
| k33 | -0.35 | 0.35 |
| h8 | 0.28 | 0.28 |
| k3a | -0.26 | 0.26 |
| k82 | 0.13 | 0.13 |
| a6a | -0.11 | 0.11 |
| k3bc | -0.07 | 0.07 |
| a4a | 0.07 | 0.07 |

# Discussion

## What the Model Can and Cannot Claim

The results support a narrow but important conclusion. The recovered fragility classification can be reconstructed exactly from raw survey variables, and the full LASSO-logit model can replicate the screening rule with very high discrimination. However, this is not the same as independently predicting firm distress. Because several predictors are also components of the constructed outcome, the full model primarily validates the mechanics of the index.

The leakage-reduced benchmark is therefore the more substantively meaningful result. Its ROC-AUC of 0.770 and PR-AUC of 0.428 indicate moderate independent predictive signal, not a deployment-ready risk score. This distinction changes the paper's contribution. The manuscript should be read as an audit of a fragility-screening index and as a prototype for transparent predictive screening, rather than as evidence that the model predicts observed closure, bankruptcy, or survival duration. More generally, the paper demonstrates a workflow for auditing constructed policy-screening outcomes in low-data development settings, where index labels, variable coding, and predictive performance can otherwise produce misleading policy claims.

## Construct Validity and the Fragility Paradox

Construct validity remains the central limitation. The official variable labels show that the operative rule uses innovation, website status, and employment-size information, while earlier drafts describe some of these variables as revenue volatility and digital-platform difficulty. This ambiguity affects theory, interpretation, and policy translation. In the current version, official labels take precedence. Consequently, the outcome is interpreted as a constructed screening classification that combines modernization and size-related information.

The most theoretically interesting pattern is the fragility paradox of modernization. Variables often treated as signals of capability, such as process innovation and website status, are central to the recovered fragility classification. One interpretation is that modernization may be reactive: firms innovate or establish digital presence because they are under pressure. A second interpretation is growth-stage vulnerability: modernization may bring coordination costs, liquidity strain, and managerial demands. A third interpretation is institutional incompleteness: digital or innovation activity may not translate into resilience when finance, infrastructure, skills, and market systems are uneven. A fourth interpretation is methodological: the paradox may partly reflect how the screening rule was constructed.

These mechanisms cannot be distinguished with the current cross-sectional data. The paper therefore treats them as theory-guided hypotheses for future research rather than as confirmed explanations. A stronger design would link the screening index to later outcomes, such as firm exit, employment contraction, revenue decline, or recovery after disruption.

## External Validity and Survey Design

The sample consists of 358 formal firms from the Rwanda 2023 Enterprise Survey. It does not cover the full Rwandan enterprise ecosystem. Informal enterprises, microenterprises, rural firms below the survey eligibility threshold, and firms outside the WBES frame may face different forms of fragility. Predictive performance in the formal-firm sample should therefore not be generalized to all Rwandan SMEs.

Survey design also matters. This paper reports sample-level predictive diagnostics, while the companion weighted-analysis paper estimates formal-firm fragility prevalence under WBES weights. Before national policy claims are made, future work should combine predictive diagnostics with survey-weighted prevalence, design-based uncertainty intervals, and subgroup checks by region, sector, firm size, ownership, and gender where available.

## Remaining Empirical Work

The revised analysis adds calibration, PR-AUC, threshold sensitivity, bootstrap confidence intervals, subgroup diagnostics, and a complete-case audit. These additions improve transparency, but they do not eliminate the need for external validation. The calibration evidence is especially important for deployment: the leakage-reduced model may rank firms moderately well, but its predicted probabilities should not be interpreted as calibrated estimates of true fragility risk without recalibration and external validation. Future work should report calibration intercepts and slopes, compare class-weighted and unweighted specifications, and test Platt scaling or isotonic calibration on validation folds before presenting predicted probabilities as risk probabilities. Future work should also validate the index against observed firm outcomes, test the alternative finance-digital Omega index, compare LASSO with other interpretable statistical-learning models only when those models are reproducibly generated, and audit fairness across policy-relevant groups. The most valuable extension is linkage to Rwanda's Establishment Census and Integrated Business Enterprise Survey, which can clarify what the WBES formal-firm frame omits about informal and microenterprise fragility [@nisr2025ibes; @nisr2024establishment].

# Policy Translation and Ethical Use

The screening framework should be used only as a preliminary diagnostic tool for supportive intervention. Its appropriate uses include identifying firms for outreach, offering diagnostic assessments, bundling finance and digital-capability support, and prioritizing follow-up research. It should not be used to deny credit, exclude firms from assistance, stigmatize businesses, or assign punitive risk labels.

Responsible deployment would require human review before any policy action. Firms should be able to understand why they were flagged, correct inaccurate information, and appeal decisions based on the score. The model should also be audited periodically across region, sector, firm size, ownership, and gender where data permit. These audits are necessary because a classifier that appears useful on average may still over-flag particular groups or under-detect need in others.

The governance principle is straightforward: fragility scores should expand access to support rather than restrict it. In practical terms, the score should trigger a conversation, not a final decision. It should be paired with qualitative assessment, field verification, and transparent eligibility rules. This is especially important in SME policy because risk scores can become self-fulfilling if they reduce access to finance or public support for firms already facing constraints.

Table 12 below translates this principle into concrete policy-use boundaries. The table is intentionally conservative because the current score is constructed, only moderately predictive after leakage reduction, and not externally validated against observed firm distress.

**Table 12: Policy-Use Safeguards for SME Fragility Scores**

| } Policy use case | Appropriate? | Required safeguard |
| --- | --- | --- |
| Diagnostic outreach | Yes | Use the score to invite voluntary assessment and support, with human review before follow-up action. |
| Credit denial | No | Prohibited use; the model is not validated for punitive or exclusionary financial decisions. |
| Grant prioritization | Conditional | Combine the score with field verification, transparent criteria, and an appeal mechanism. |
| Research sampling | Yes | Use only to identify cases for further study, with disclosure that the score is a constructed screening signal. |
| Automated eligibility | No | Not deployment-ready; eligibility decisions require independent validation, calibration, and governance review. |

# Conclusion

This paper audits and predicts a constructed SME fragility classification using Rwanda 2023 Enterprise Survey data. Its main contribution is not simply a high-performing predictive model. Rather, the paper shows how a legacy fragility indicator can be reconstructed, checked against official metadata, tested for predictor leakage, and evaluated with transparent validation diagnostics in a low-data African enterprise context. This index-auditing workflow is relevant beyond Rwanda because many social-science and development-policy datasets rely on constructed screening indicators whose validity depends on transparent coding, documentation, and external validation.

The substantive conclusion is cautious. The full model replicates the recovered screening rule very well, but the leakage-reduced benchmark provides the more meaningful estimate of independent predictive signal. That benchmark performs moderately, which supports continued development of the screening framework but not immediate policy deployment as a definitive risk score. The construct-validity audit further shows that the current outcome should be interpreted as an innovation, website-status, and employment-linked screening classification, not as a direct measure of observed firm failure or financial distress.

Before journal submission and policy use, the index should be validated against independent outcomes, tested with survey-design adjustments, and governed as a supportive diagnostic tool. Used carefully, the framework can help researchers and policymakers identify where more evidence is needed and how SME-support systems might better detect vulnerability before observable failure occurs.

# References

::: {#refs}
:::
