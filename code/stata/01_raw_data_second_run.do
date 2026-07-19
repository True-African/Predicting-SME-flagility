version 17.0
clear all
set more off

global ROOT "D:/Research/LASSO"
global RAW "$ROOT/data/raw/Rwanda-2023-full-data.dta"
global PROCESSED "$ROOT/data/processed/classification_probabilities.csv"
global OUT "$ROOT/results/stata"
global TABLES "$ROOT/results/tables"
global FIGS "$ROOT/results/figures/second_run"
global LOGS "$ROOT/results/stata/logs"

cap mkdir "$OUT"
cap mkdir "$TABLES"
cap mkdir "$FIGS"
cap mkdir "$LOGS"

log using "$LOGS/second_run_stata.log", replace text

display "Second run of Rwanda 2023 raw Enterprise Survey data"
display "Started: $S_DATE $S_TIME"

use "$RAW", clear
describe
codebook h1 h2 h5 c22b l1 wmedian wstrict wweak a2 a3a a4a a6a k82 k162 k3a k3bc k33 b6

log close

log using "$OUT/second_run_codebook.txt", replace text
describe
codebook h1 h2 h5 c22b l1 wmedian wstrict wweak a2 a3a a4a a6a k82 k162 k3a k3bc k33 b6
log close

log using "$LOGS/second_run_stata.log", append text

gen long obs_id = _n

gen byte fragility_second_run = ///
    (h5 == 1 & l1 <= 3) | ///
    (h5 == 2 & c22b == 1 & l1 <= -2) | ///
    (h5 == 2 & c22b == 2 & (h1 == 2 | h2 != 1))
label define fragility_lbl 0 "Non-fragile" 1 "Fragile", replace
label values fragility_second_run fragility_lbl

preserve
keep obs_id fragility_second_run
tempfile rule
save `rule'
import delimited "$PROCESSED", clear
gen long obs_id = _n
merge 1:1 obs_id using `rule', nogen
gen byte match = fragility_risk_flex == fragility_second_run
export delimited using "$OUT/second_run_fragility_validation.csv", replace
collapse (count) n=match (sum) matches=match supplied_fragile=fragility_risk_flex second_run_fragile=fragility_second_run
gen mismatches = n - matches
gen agreement = matches / n
export delimited using "$TABLES/second_run_fragility_validation_summary.csv", replace
restore

preserve
keep h1 h2 h5 c22b l1 wmedian wstrict wweak a2 a3a a4a a6a k82 k162 k3a k3bc k33 b6
misstable summarize
summarize
restore

preserve
collapse ///
    (mean) unweighted=fragility_second_run ///
    [aw=wmedian]
gen approach = "wmedian"
rename unweighted fragility_pct
replace fragility_pct = fragility_pct * 100
tempfile weighted
save `weighted'
restore

preserve
collapse (mean) fragility_pct=fragility_second_run
replace fragility_pct = fragility_pct * 100
gen approach = "unweighted"
tempfile unweighted
save `unweighted'
restore

preserve
collapse (mean) fragility_pct=fragility_second_run [aw=wstrict]
replace fragility_pct = fragility_pct * 100
gen approach = "wstrict"
append using `weighted'
append using `unweighted'
tempfile prev
save `prev'
restore

preserve
collapse (mean) fragility_pct=fragility_second_run [aw=wweak]
replace fragility_pct = fragility_pct * 100
gen approach = "wweak"
append using `prev'
order approach fragility_pct
export delimited using "$OUT/second_run_weighted_prevalence.csv", replace
export delimited using "$TABLES/second_run_weighted_prevalence_stata.csv", replace
graph hbar fragility_pct, over(approach, sort(1)) ///
    ytitle("Fragility (%)") ///
    title("Weighted and unweighted fragility prevalence")
graph export "$FIGS/stata_weighted_unweighted_prevalence.png", replace width(1800)
restore

foreach group in a2 a4a a6a c22b h5 {
    preserve
    collapse ///
        (count) n=fragility_second_run ///
        (mean) unweighted_fragility_pct=fragility_second_run ///
        [aw=wmedian], by(`group')
    replace unweighted_fragility_pct = unweighted_fragility_pct * 100
    decode `group', gen(group_label)
    export delimited using "$OUT/second_run_`group'_table.csv", replace
    graph hbar unweighted_fragility_pct, over(group_label, sort(1)) ///
        ytitle("Weighted fragility (%)") ///
        title("Weighted fragility by `group'")
    graph export "$FIGS/stata_fragility_by_`group'.png", replace width(1800)
    restore
}

display "Second run completed: $S_DATE $S_TIME"
log close
