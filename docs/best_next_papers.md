# Best Next Papers from the Raw CSV and External Data

## 1. Spatial Inequality in SME Fragility

**Working title:** Spatial Concentration and Regional Inequality in SME Fragility in Rwanda

**Core question:** Are fragile firms spatially concentrated, and do Kigali, Western/Northern, and Southern/Eastern regions show different fragility profiles once survey weights are applied?

**Data needed:**
- WBES Rwanda 2023 firm-level CSV: `data/raw/Rwanda-2023-full-data.csv`
- WBES region variables: `a2`, `a3a`
- Survey weights: `wmedian`, `wstrict`, `wweak`
- Rwanda district/province boundaries from an official NISR or Rwanda geospatial source
- Optional: nightlights, road density, internet coverage, electricity access, distance to Kigali

**Main contribution:** Moves the project from firm-level prediction to spatial development policy. The strongest version would show where formal-firm fragility is concentrated and whether regional infrastructure/digital gaps explain it.

**Likely methods:** Weighted descriptive maps, spatial joins, choropleth maps, multilevel logit, regional marginal effects.

## 2. Formal vs Informal Enterprise Fragility Gaps

**Working title:** What Formal-Firm Surveys Miss: Informality and Enterprise Fragility in Rwanda

**Core question:** How does the formal-firm universe covered by WBES differ from Rwanda's broader formal and informal enterprise landscape?

**Data needed:**
- WBES Rwanda 2023 formal-firm data
- NISR Integrated Business Enterprise Survey 2023
- NISR Establishment Census 2023
- NISR microdata metadata for formal/informal enterprises

**Known external-data facts to motivate the paper:**
- IBES 2023 estimates 260,780 business enterprises, with informal enterprises accounting for 88 percent of total enterprises.
- Establishment Census 2023 reports 269,326 establishments and 261,549 enterprises.
- Establishment Census metadata reports 35,825 formal enterprises and 233,369 informal enterprises in the formal/informal enterprise variable.

**Main contribution:** Shows that WBES is valuable for formal SMEs with at least five employees, but it cannot represent Rwanda's large informal and microenterprise base. This would be a strong social-science paper because it connects sampling frames to policy blind spots.

**Likely methods:** Frame comparison, sector-size decomposition, formal/informal gap analysis, policy simulation.

## 3. Digital Finance, E-Payments, and Resilience

**Working title:** Digital Finance and SME Resilience in Rwanda: Evidence from E-Payments, Websites, and Financial Access

**Core question:** Do digital-payment and online-presence indicators identify firms with stronger adaptive capacity?

**Data needed:**
- WBES variables on website, internet use, e-payments, finance, loans, collateral, working capital, payment delays
- Optional: mobile-money penetration, fintech access indicators, district internet coverage

**Main contribution:** Builds directly on recent open-access literature showing that digital technologies help SMEs respond to crises, but tests the issue in an African enterprise-survey setting.

**Likely methods:** Weighted logit/probit, LASSO feature selection, interaction between finance and digital adoption, heterogeneity by sector and region.

## 4. Manufacturing-Sector Fragility and Industrial Policy

**Working title:** Manufacturing SME Fragility and Rwanda's Industrial Upgrading Agenda

**Core question:** Are manufacturing SMEs more exposed to fragility through infrastructure, capacity utilization, finance, and export constraints?

**Data needed:**
- WBES manufacturing/service sector variables
- Capacity utilization, employment, exports, infrastructure, outages, finance, and innovation indicators
- Establishment Census sectoral employment and district concentration

**Main contribution:** Connects the micro-level fragility project to industrial policy and manufacturing-led development. This is likely the best applied policy paper after Paper 1.

**Likely methods:** Sector-stratified models, manufacturing-only model, infrastructure constraint index, weighted descriptive comparisons.

## 5. Weighted National Fragility Estimates Using WBES Survey Weights

**Working title:** From Sample Prediction to Population Screening: Weighted Estimates of Formal-SME Fragility in Rwanda

**Core question:** How does the estimated prevalence of SME fragility change when WBES sampling weights are applied?

**Data needed:**
- WBES Rwanda 2023 weights: `wmedian`, `wstrict`, `wweak`
- Recovered fragility rule
- Region, sector, and size strata

**Main contribution:** Turns Paper 1's sample-level model into a nationally interpretable formal-firm estimate. This should be done before making any national policy claims.

**Likely methods:** Weighted prevalence, design-based standard errors, weighted model comparison, sensitivity analysis across the three WBES weights.

## Priority Order

1. Weighted national fragility estimates.
2. Spatial inequality in SME fragility.
3. Formal vs informal enterprise fragility gaps.
4. Digital finance, e-payments, and resilience.
5. Manufacturing-sector fragility and industrial policy.

The weighted paper should come first because it directly strengthens Paper 1. The formal/informal and spatial papers are likely the strongest new-paper opportunities once external data are added.
