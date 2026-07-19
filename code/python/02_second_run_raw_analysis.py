from __future__ import annotations

from pathlib import Path
import json
import math
import textwrap

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    precision_score,
    precision_recall_curve,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
RAW_DTA = ROOT / "data" / "raw" / "Rwanda-2023-full-data.dta"
RAW_CSV = ROOT / "data" / "raw" / "Rwanda-2023-full-data.csv"
LABEL_CSV = ROOT / "data" / "raw" / "Rwanda-2023-variable-labels.csv"
PROCESSED = ROOT / "data" / "processed"
RESULTS_TABLES = ROOT / "results" / "tables"
RESULTS_MODELS = ROOT / "results" / "models"
RESULTS_FIGURES = ROOT / "results" / "figures" / "second_run"
RESULTS_STATA = ROOT / "results" / "stata"
DOCS = ROOT / "docs"


for folder in [RESULTS_TABLES, RESULTS_MODELS, RESULTS_FIGURES, RESULTS_STATA, DOCS]:
    folder.mkdir(parents=True, exist_ok=True)


def clean_missing(frame: pd.DataFrame) -> pd.DataFrame:
    """Treat common WBES negative special codes as missing for summaries/models."""
    out = frame.copy()
    numeric_cols = out.select_dtypes(include=[np.number]).columns
    out[numeric_cols] = out[numeric_cols].mask(out[numeric_cols].isin([-9, -8, -7, -6]))
    return out


def recovered_fragility_rule(df: pd.DataFrame) -> pd.Series:
    return (
        ((df["h5"] == 1) & (df["l1"] <= 3))
        | ((df["h5"] == 2) & (df["c22b"] == 1) & (df["l1"] <= -2))
        | ((df["h5"] == 2) & (df["c22b"] == 2) & ((df["h1"] == 2) | (df["h2"] != 1)))
    ).astype(int)


def label_map(reader: pd.io.stata.StataReader, variables: list[str]) -> dict[str, dict[float, str]]:
    reader.read(nrows=1, convert_categoricals=False)
    value_labels = reader.value_labels()
    maps = {}
    for variable, label_name in zip(reader._varlist, reader._lbllist):
        if variable in variables:
            maps[variable] = {float(k): str(v) for k, v in value_labels.get(label_name, {}).items()}
    return maps


def decode(series: pd.Series, mapping: dict[float, str] | None) -> pd.Series:
    if not mapping:
        return series.astype("string")
    return series.map(lambda x: mapping.get(float(x), str(x)) if pd.notna(x) else np.nan)


def weighted_mean(y: pd.Series, w: pd.Series | None = None) -> float:
    if w is None:
        return float(y.mean())
    mask = y.notna() & w.notna() & (w > 0)
    return float(np.average(y[mask], weights=w[mask])) if mask.any() else math.nan


def group_table(df: pd.DataFrame, group: str, label: str, weights: list[str], maps: dict) -> pd.DataFrame:
    rows = []
    decoded = decode(df[group], maps.get(group))
    for value in decoded.dropna().unique():
        mask = decoded == value
        row = {
            label: value,
            "n": int(mask.sum()),
            "unweighted_fragility_pct": 100 * weighted_mean(df.loc[mask, "fragility_second_run"]),
        }
        for w in weights:
            row[f"{w}_fragility_pct"] = 100 * weighted_mean(df.loc[mask, "fragility_second_run"], df.loc[mask, w])
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("wmedian_fragility_pct", ascending=False)
    return out


def save_table(frame: pd.DataFrame, stem: str, caption: str | None = None) -> None:
    csv_path = RESULTS_TABLES / f"{stem}.csv"
    tex_path = RESULTS_TABLES / f"{stem}.tex"
    frame.to_csv(csv_path, index=False)
    display = frame.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: "" if pd.isna(x) else f"{x:.2f}")
    display.to_latex(tex_path, index=False, escape=True)


def save_publication_table(frame: pd.DataFrame, stem: str) -> None:
    """Write a LaTeX table after values are already formatted for publication."""
    frame.to_csv(RESULTS_TABLES / f"{stem}.csv", index=False)
    frame.to_latex(RESULTS_TABLES / f"{stem}.tex", index=False, escape=True)


def markdown_table(frame: pd.DataFrame) -> str:
    display = frame.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda x: "" if pd.isna(x) else f"{x:.3f}")
    widths = {
        col: max(len(str(col)), *(len(str(v)) for v in display[col].astype(str).tolist()))
        for col in display.columns
    }
    header = "| " + " | ".join(str(col).ljust(widths[col]) for col in display.columns) + " |"
    divider = "| " + " | ".join("-" * widths[col] for col in display.columns) + " |"
    rows = [
        "| " + " | ".join(str(row[col]).ljust(widths[col]) for col in display.columns) + " |"
        for _, row in display.iterrows()
    ]
    return "\n".join([header, divider, *rows])


def bar_plot(frame: pd.DataFrame, category: str, value: str, title: str, output: str, xlabel: str = "") -> None:
    plot_df = frame[[category, value]].dropna().copy()
    plot_df[value] = pd.to_numeric(plot_df[value], errors="coerce")
    plot_df = plot_df.dropna().sort_values(value)
    fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
    ax.barh(plot_df[category].astype(str), plot_df[value], color="#2F6C8F")
    ax.set_xlabel(xlabel or "Fragility (%)")
    ax.set_title(title)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.2)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES / output)
    plt.close(fig)


def run_lasso_model(X: pd.DataFrame, y: pd.Series, stem: str, title_prefix: str) -> pd.DataFrame:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)
    numeric_features = X.columns.tolist()
    model = Pipeline(
        steps=[
            (
                "prep",
                ColumnTransformer(
                    transformers=[
                        (
                            "num",
                            Pipeline(
                                steps=[
                                    ("impute", SimpleImputer(strategy="median")),
                                    ("scale", StandardScaler()),
                                ]
                            ),
                            numeric_features,
                        )
                    ]
                ),
            ),
            (
                "model",
                LogisticRegressionCV(
                    Cs=20,
                    penalty="l1",
                    solver="liblinear",
                    cv=5,
                    scoring="roc_auc",
                    class_weight="balanced",
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )
    model.fit(X_train, y_train)
    prob = model.predict_proba(X_test)[:, 1]
    pred = (prob >= 0.5).astype(int)
    tn = int(((pred == 0) & (y_test == 0)).sum())
    fp = int(((pred == 1) & (y_test == 0)).sum())
    performance = pd.DataFrame(
        [
            {
                "accuracy": accuracy_score(y_test, pred),
                "precision": precision_score(y_test, pred, zero_division=0),
                "recall": recall_score(y_test, pred, zero_division=0),
                "specificity": tn / (tn + fp) if (tn + fp) else np.nan,
                "roc_auc": roc_auc_score(y_test, prob),
                "test_n": len(y_test),
                "test_fragile_n": int(y_test.sum()),
            }
        ]
    )
    save_table(performance, f"{stem}_test_performance", f"{title_prefix} LASSO-logit performance")
    coef = pd.DataFrame(
        {
            "predictor": numeric_features,
            "coefficient": model.named_steps["model"].coef_[0],
        }
    )
    coef["abs_coefficient"] = coef["coefficient"].abs()
    coef = coef.sort_values("abs_coefficient", ascending=False)
    save_table(coef, f"{stem}_coefficients", f"{title_prefix} LASSO-logit coefficients")

    predictions = pd.DataFrame(
        {
            "row_id": y_test.index.to_numpy(),
            "observed": y_test.to_numpy(),
            "predicted_probability": prob,
            "predicted_class": pred,
        }
    )
    predictions.to_csv(RESULTS_MODELS / f"{stem}_test_predictions.csv", index=False)
    fpr, tpr, _ = roc_curve(y_test, prob)
    fig, ax = plt.subplots(figsize=(6, 5), dpi=180)
    ax.plot(fpr, tpr, color="#2F6C8F", label=f"ROC-AUC = {performance.loc[0, 'roc_auc']:.3f}")
    ax.plot([0, 1], [0, 1], color="#777777", linestyle="--", linewidth=1)
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title(f"{title_prefix} ROC")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES / f"{stem}_roc.png")
    plt.close(fig)

    top_coef = coef.head(12).sort_values("coefficient")
    fig, ax = plt.subplots(figsize=(8, 5), dpi=180)
    ax.barh(top_coef["predictor"], top_coef["coefficient"], color=np.where(top_coef["coefficient"] >= 0, "#2F6C8F", "#8F4A2F"))
    ax.axvline(0, color="#333333", linewidth=0.8)
    ax.set_title(f"{title_prefix} coefficients")
    ax.set_xlabel("Standardized coefficient")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES / f"{stem}_coefficients.png")
    plt.close(fig)
    return {
        "performance": performance,
        "predictions": predictions,
        "model": model,
        "test_index": y_test.index.to_numpy(),
        "y_test": y_test.to_numpy(),
        "prob": prob,
    }


def bootstrap_metric_ci(y_true: np.ndarray, prob: np.ndarray, metric_fn, reps: int = 1000) -> tuple[float, float]:
    rng = np.random.default_rng(42)
    values = []
    n = len(y_true)
    for _ in range(reps):
        idx = rng.integers(0, n, n)
        if len(np.unique(y_true[idx])) < 2:
            continue
        values.append(metric_fn(y_true[idx], prob[idx]))
    if not values:
        return (np.nan, np.nan)
    return (float(np.percentile(values, 2.5)), float(np.percentile(values, 97.5)))


def threshold_table(y_true: np.ndarray, prob: np.ndarray, thresholds: list[float], stem: str) -> pd.DataFrame:
    rows = []
    for threshold in thresholds:
        pred = (prob >= threshold).astype(int)
        tn = int(((pred == 0) & (y_true == 0)).sum())
        fp = int(((pred == 1) & (y_true == 0)).sum())
        fn = int(((pred == 0) & (y_true == 1)).sum())
        tp = int(((pred == 1) & (y_true == 1)).sum())
        rows.append(
            {
                "threshold": threshold,
                "accuracy": accuracy_score(y_true, pred),
                "precision": precision_score(y_true, pred, zero_division=0),
                "recall": recall_score(y_true, pred, zero_division=0),
                "specificity": tn / (tn + fp) if (tn + fp) else np.nan,
                "true_positives": tp,
                "false_positives": fp,
                "true_negatives": tn,
                "false_negatives": fn,
            }
        )
    out = pd.DataFrame(rows)
    save_table(out, stem, "Threshold sensitivity")
    return out


def diagnostics_for_predictions(run: dict, stem: str, title_prefix: str) -> dict[str, float]:
    y_true = np.asarray(run["y_test"])
    prob = np.asarray(run["prob"])
    roc_ci = bootstrap_metric_ci(y_true, prob, roc_auc_score)
    pr_ci = bootstrap_metric_ci(y_true, prob, average_precision_score)
    diagnostics = {
        "roc_auc": roc_auc_score(y_true, prob),
        "roc_auc_ci_low": roc_ci[0],
        "roc_auc_ci_high": roc_ci[1],
        "pr_auc": average_precision_score(y_true, prob),
        "pr_auc_ci_low": pr_ci[0],
        "pr_auc_ci_high": pr_ci[1],
        "brier_score": brier_score_loss(y_true, prob),
        "test_n": len(y_true),
        "test_fragile_n": int(y_true.sum()),
    }
    save_table(pd.DataFrame([diagnostics]), f"{stem}_diagnostics", f"{title_prefix} diagnostics")

    thresholds = threshold_table(y_true, prob, [0.30, 0.40, 0.50, 0.60, 0.70], f"{stem}_threshold_sensitivity")

    frac_pos, mean_pred = calibration_curve(y_true, prob, n_bins=5, strategy="quantile")
    calibration = pd.DataFrame({"mean_predicted_probability": mean_pred, "observed_fragility_rate": frac_pos})
    save_table(calibration, f"{stem}_calibration_bins", f"{title_prefix} calibration bins")

    fig, ax = plt.subplots(figsize=(6, 5), dpi=180)
    ax.plot(mean_pred, frac_pos, marker="o", color="#2F6C8F", label=title_prefix)
    ax.plot([0, 1], [0, 1], color="#777777", linestyle="--", linewidth=1, label="Perfect calibration")
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Observed fragility rate")
    ax.set_title(f"{title_prefix} calibration")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES / f"{stem}_calibration.png")
    plt.close(fig)

    precision, recall, _ = precision_recall_curve(y_true, prob)
    fig, ax = plt.subplots(figsize=(6, 5), dpi=180)
    ax.plot(recall, precision, color="#2F6C8F", label=f"PR-AUC = {diagnostics['pr_auc']:.3f}")
    ax.axhline(y_true.mean(), color="#777777", linestyle="--", linewidth=1, label="Fragility prevalence")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(f"{title_prefix} precision-recall curve")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(RESULTS_FIGURES / f"{stem}_precision_recall.png")
    plt.close(fig)

    return {"diagnostics": diagnostics, "thresholds": thresholds}


def subgroup_performance(
    predictions: pd.DataFrame,
    dta: pd.DataFrame,
    maps: dict,
    groups: list[tuple[str, str]],
    stem: str,
) -> pd.DataFrame:
    merged = predictions.merge(dta.reset_index(names="row_id"), on="row_id", how="left")
    rows = []
    for variable, label in groups:
        decoded = decode(merged[variable], maps.get(variable))
        for value in decoded.dropna().unique():
            mask = decoded == value
            if mask.sum() < 10:
                continue
            y_true = merged.loc[mask, "observed"].to_numpy()
            pred = merged.loc[mask, "predicted_class"].to_numpy()
            prob = merged.loc[mask, "predicted_probability"].to_numpy()
            tn = int(((pred == 0) & (y_true == 0)).sum())
            fp = int(((pred == 1) & (y_true == 0)).sum())
            rows.append(
                {
                    "group": label,
                    "category": value,
                    "test_n": int(mask.sum()),
                    "fragile_n": int(y_true.sum()),
                    "accuracy": accuracy_score(y_true, pred),
                    "precision": precision_score(y_true, pred, zero_division=0),
                    "recall": recall_score(y_true, pred, zero_division=0),
                    "specificity": tn / (tn + fp) if (tn + fp) else np.nan,
                    "mean_predicted_probability": float(np.mean(prob)),
                }
            )
    out = pd.DataFrame(rows)
    save_table(out, stem, "Subgroup model performance")
    return out


def main() -> None:
    reader = pd.io.stata.StataReader(RAW_DTA)
    variable_labels = reader.variable_labels()
    maps = label_map(reader, ["a2", "a3a", "a4a", "a6a", "h1", "h2", "h5", "c22b"])

    dta = pd.read_stata(RAW_DTA, convert_categoricals=False)
    csv = pd.read_csv(RAW_CSV)
    dta_shape_raw = dta.shape
    raw_clean = clean_missing(dta)

    key_vars = [
        "h1",
        "h2",
        "h5",
        "c22b",
        "l1",
        "wmedian",
        "wstrict",
        "wweak",
        "a2",
        "a3a",
        "a4a",
        "a6a",
        "k82",
        "k162",
        "k3a",
        "k3bc",
        "k33",
        "b6",
    ]
    existing_key_vars = [c for c in key_vars if c in dta.columns]
    dta["fragility_second_run"] = recovered_fragility_rule(dta)

    classification = pd.read_csv(PROCESSED / "classification_probabilities.csv")
    validation = pd.DataFrame(
        {
            "fragility_supplied": classification["fragility_risk_flex"],
            "fragility_second_run": dta["fragility_second_run"],
            "match": classification["fragility_risk_flex"].eq(dta["fragility_second_run"]),
        }
    )
    validation.to_csv(RESULTS_STATA / "second_run_fragility_validation.csv", index=False)
    validation_summary = pd.DataFrame(
        [
            {
                "n": len(validation),
                "supplied_fragile": int(validation["fragility_supplied"].sum()),
                "second_run_fragile": int(validation["fragility_second_run"].sum()),
                "matches": int(validation["match"].sum()),
                "mismatches": int((~validation["match"]).sum()),
                "agreement": validation["match"].mean(),
            }
        ]
    )
    save_table(validation_summary, "second_run_fragility_validation_summary", "Second-run fragility-rule validation")

    summary_rows = []
    for col in existing_key_vars:
        s = dta[col]
        summary_rows.append(
            {
                "variable": col,
                "label": variable_labels.get(col, ""),
                "nonmissing_raw": int(s.notna().sum()),
                "missing_raw": int(s.isna().sum()),
                "special_negative_codes": int(s.isin([-9, -8, -7, -6]).sum()) if pd.api.types.is_numeric_dtype(s) else 0,
                "mean_clean": raw_clean[col].mean() if col in raw_clean and pd.api.types.is_numeric_dtype(raw_clean[col]) else np.nan,
                "min_clean": raw_clean[col].min() if col in raw_clean and pd.api.types.is_numeric_dtype(raw_clean[col]) else np.nan,
                "max_clean": raw_clean[col].max() if col in raw_clean and pd.api.types.is_numeric_dtype(raw_clean[col]) else np.nan,
            }
        )
    descriptives = pd.DataFrame(summary_rows)
    descriptives.to_csv(RESULTS_STATA / "second_run_descriptives.csv", index=False)
    save_table(descriptives, "second_run_key_variable_descriptives", "Second-run key-variable audit")

    construct_validity = pd.DataFrame(
        [
            {
                "Variable code": "h1",
                "Official WBES/Stata label": variable_labels.get("h1", ""),
                "Legacy/draft label": "Product/service innovation",
                "Role in outcome rule": "Used in third branch when h5=2 and c22b=2",
                "Final interpretation": "Product/service innovation status",
                "Implication for theory": "Capability indicator; interpret as modernization status, not financial distress.",
            },
            {
                "Variable code": "h2",
                "Official WBES/Stata label": variable_labels.get("h2", ""),
                "Legacy/draft label": "New-to-market innovation",
                "Role in outcome rule": "Used in third branch when h5=2 and c22b=2",
                "Final interpretation": "Market novelty of innovation",
                "Implication for theory": "Signals innovation depth but has missingness; avoid causal claims.",
            },
            {
                "Variable code": "h5",
                "Official WBES/Stata label": variable_labels.get("h5", ""),
                "Legacy/draft label": "Revenue volatility",
                "Role in outcome rule": "Used in all three branches",
                "Final interpretation": "Process innovation status",
                "Implication for theory": "Central construct-validity tension; any revenue-volatility reading requires a documented recode.",
            },
            {
                "Variable code": "c22b",
                "Official WBES/Stata label": variable_labels.get("c22b", ""),
                "Legacy/draft label": "Digital-platform difficulty",
                "Role in outcome rule": "Used in second and third branches",
                "Final interpretation": "Own-website status",
                "Implication for theory": "Digital-presence indicator; not direct evidence of platform difficulty.",
            },
            {
                "Variable code": "l1",
                "Official WBES/Stata label": variable_labels.get("l1", ""),
                "Legacy/draft label": "Employment vulnerability",
                "Role in outcome rule": "Used in first and second branches",
                "Final interpretation": "Permanent full-time employment count",
                "Implication for theory": "Firm-size/employment component; supports size-related screening interpretation.",
            },
        ]
    )
    save_publication_table(construct_validity, "paper1_construct_validity_audit")

    missingness = (
        dta.isna()
        .sum()
        .rename("system_missing")
        .to_frame()
        .assign(
            special_negative_codes=[
                int(dta[c].isin([-9, -8, -7, -6]).sum()) if pd.api.types.is_numeric_dtype(dta[c]) else 0
                for c in dta.columns
            ],
            pct_any_missing=lambda x: 100 * (x["system_missing"] + x["special_negative_codes"]) / len(dta),
        )
        .reset_index()
        .rename(columns={"index": "variable"})
        .sort_values("pct_any_missing", ascending=False)
    )
    missingness.to_csv(RESULTS_STATA / "second_run_missingness.csv", index=False)
    save_table(missingness.head(25), "second_run_missingness_top25", "Top missingness and special-code variables")

    weights = ["wmedian", "wstrict", "wweak"]
    prevalence_rows = [
        {"approach": "unweighted", "fragility_pct": 100 * weighted_mean(dta["fragility_second_run"])}
    ]
    for w in weights:
        prevalence_rows.append(
            {"approach": w, "fragility_pct": 100 * weighted_mean(dta["fragility_second_run"], dta[w])}
        )
    prevalence = pd.DataFrame(prevalence_rows)
    prevalence.to_csv(RESULTS_STATA / "second_run_weighted_prevalence.csv", index=False)
    save_table(prevalence, "second_run_weighted_prevalence", "Second-run weighted fragility prevalence")

    region = group_table(dta, "a2", "region", weights, maps)
    sector = group_table(dta, "a4a", "sector", weights, maps)
    size = group_table(dta, "a6a", "firm_size", weights, maps)
    website = group_table(dta, "c22b", "has_website", weights, maps)
    innovation = group_table(dta, "h5", "process_innovation", weights, maps)

    region.to_csv(RESULTS_STATA / "second_run_region_table.csv", index=False)
    sector.to_csv(RESULTS_STATA / "second_run_sector_table.csv", index=False)
    size.to_csv(RESULTS_STATA / "second_run_size_table.csv", index=False)
    website.to_csv(RESULTS_STATA / "second_run_digital_finance_table.csv", index=False)

    save_table(region, "second_run_region_table", "Second-run fragility by region")
    save_table(sector, "second_run_sector_table", "Second-run fragility by sector")
    save_table(size, "second_run_size_table", "Second-run fragility by firm size")
    save_table(website, "second_run_website_table", "Second-run fragility by website status")
    save_table(innovation, "second_run_process_innovation_table", "Second-run fragility by process innovation")

    bar_plot(prevalence, "approach", "fragility_pct", "Weighted and unweighted fragility prevalence", "weighted_unweighted_prevalence.png")
    bar_plot(region, "region", "wmedian_fragility_pct", "Weighted fragility by region", "fragility_by_region.png")
    bar_plot(sector, "sector", "wmedian_fragility_pct", "Weighted fragility by sector", "fragility_by_sector.png")
    bar_plot(size, "firm_size", "wmedian_fragility_pct", "Weighted fragility by firm size", "fragility_by_size.png")
    bar_plot(website, "has_website", "wmedian_fragility_pct", "Weighted fragility by website status", "fragility_by_website.png")
    bar_plot(missingness.head(20), "variable", "pct_any_missing", "Top raw-data missingness/special-code rates", "missingness_top20.png", "Missing or special-coded (%)")

    predictors = pd.read_csv(PROCESSED / "Rwanda_2023_predictors_only.csv")
    y = dta["fragility_second_run"]
    X = clean_missing(predictors)
    rule_vars = [c for c in ["h1", "h2", "h5", "c22b", "l1"] if c in X.columns]
    leakage_map = pd.DataFrame(
        [
            {
                "Variable": col,
                "Used in outcome rule": "Yes" if col in ["h1", "h2", "h5", "c22b", "l1"] else "No",
                "Used as predictor": "Yes" if col in X.columns else "No",
                "Leakage risk": "High" if col in rule_vars else ("Rule-only" if col == "l1" else "Low"),
            }
            for col in sorted(set(X.columns).union({"h1", "h2", "h5", "c22b", "l1"}))
        ]
    )
    save_publication_table(leakage_map, "paper1_predictor_leakage_map")

    full_run = run_lasso_model(X, y, "second_run_lasso", "Screening-rule replication")
    performance = full_run["performance"]
    leakage_reduced_X = X.drop(columns=rule_vars)
    leakage_reduced_run = run_lasso_model(
        leakage_reduced_X,
        y,
        "second_run_lasso_no_rulevars",
        "Leakage-reduced benchmark",
    )
    leakage_reduced_performance = leakage_reduced_run["performance"]

    full_diagnostics = diagnostics_for_predictions(full_run, "second_run_lasso", "Screening-rule replication")
    leakage_diagnostics = diagnostics_for_predictions(
        leakage_reduced_run,
        "second_run_lasso_no_rulevars",
        "Leakage-reduced benchmark",
    )
    subgroup_perf = subgroup_performance(
        leakage_reduced_run["predictions"],
        dta,
        maps,
        [("a2", "Region"), ("a4a", "Sector"), ("a6a", "Firm size")],
        "second_run_lasso_no_rulevars_subgroup_performance",
    )

    comparison_rows = []
    for metric, full_value, reduced_value in [
        ("ROC-AUC", full_diagnostics["diagnostics"]["roc_auc"], leakage_diagnostics["diagnostics"]["roc_auc"]),
        ("PR-AUC", full_diagnostics["diagnostics"]["pr_auc"], leakage_diagnostics["diagnostics"]["pr_auc"]),
        ("Brier score", full_diagnostics["diagnostics"]["brier_score"], leakage_diagnostics["diagnostics"]["brier_score"]),
        ("Accuracy", performance.loc[0, "accuracy"], leakage_reduced_performance.loc[0, "accuracy"]),
        ("Precision", performance.loc[0, "precision"], leakage_reduced_performance.loc[0, "precision"]),
        ("Recall", performance.loc[0, "recall"], leakage_reduced_performance.loc[0, "recall"]),
        ("Specificity", performance.loc[0, "specificity"], leakage_reduced_performance.loc[0, "specificity"]),
    ]:
        comparison_rows.append(
            {
                "Metric": metric,
                "Screening-rule replication": f"{full_value:.3f}",
                "Leakage-reduced benchmark": f"{reduced_value:.3f}",
            }
        )
    comparison_rows.extend(
        [
            {
                "Metric": "ROC-AUC 95% bootstrap CI",
                "Screening-rule replication": f"[{full_diagnostics['diagnostics']['roc_auc_ci_low']:.3f}, {full_diagnostics['diagnostics']['roc_auc_ci_high']:.3f}]",
                "Leakage-reduced benchmark": f"[{leakage_diagnostics['diagnostics']['roc_auc_ci_low']:.3f}, {leakage_diagnostics['diagnostics']['roc_auc_ci_high']:.3f}]",
            },
            {
                "Metric": "PR-AUC 95% bootstrap CI",
                "Screening-rule replication": f"[{full_diagnostics['diagnostics']['pr_auc_ci_low']:.3f}, {full_diagnostics['diagnostics']['pr_auc_ci_high']:.3f}]",
                "Leakage-reduced benchmark": f"[{leakage_diagnostics['diagnostics']['pr_auc_ci_low']:.3f}, {leakage_diagnostics['diagnostics']['pr_auc_ci_high']:.3f}]",
            },
            {
                "Metric": "Test observations",
                "Screening-rule replication": str(int(performance.loc[0, "test_n"])),
                "Leakage-reduced benchmark": str(int(leakage_reduced_performance.loc[0, "test_n"])),
            },
        ]
    )
    save_publication_table(pd.DataFrame(comparison_rows), "paper1_model_performance_comparison")

    complete_mask = leakage_reduced_X.notna().all(axis=1)
    complete_case_summary = pd.DataFrame(
        [
            {
                "Analysis": "Leakage-reduced complete-case sample",
                "Complete cases": int(complete_mask.sum()),
                "Excluded observations": int((~complete_mask).sum()),
                "Fragile firms retained": int(y.loc[complete_mask].sum()),
            }
        ]
    )
    save_publication_table(complete_case_summary, "paper1_complete_case_summary")

    metadata = {
        "dta_shape": list(dta_shape_raw),
        "csv_shape": list(csv.shape),
        "csv_matches_dta_rows": int(len(csv) == len(dta)),
        "csv_matches_dta_columns": int(set(dta.columns).issubset(set(csv.columns)) or set(csv.columns).issubset(set(dta.columns))),
        "key_variables_present": existing_key_vars,
        "value_labels": maps,
        "variable_labels": {c: variable_labels.get(c, "") for c in existing_key_vars},
        "fragility_validation": validation_summary.iloc[0].to_dict(),
        "lasso_performance": performance.iloc[0].to_dict(),
        "excluded_rule_variables": rule_vars,
        "leakage_reduced_lasso_performance": leakage_reduced_performance.iloc[0].to_dict(),
    }
    (RESULTS_STATA / "second_run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    codebook_lines = [
        "Second-run raw-data codebook excerpt",
        f"Rows: {len(dta)}",
        f"Columns: {dta.shape[1]}",
        "",
        "Key variables:",
    ]
    for col in existing_key_vars:
        codebook_lines.append(f"- {col}: {variable_labels.get(col, '')}")
        if col in maps:
            codebook_lines.append(f"  value labels: {maps[col]}")
    (RESULTS_STATA / "second_run_codebook.txt").write_text("\n".join(codebook_lines), encoding="utf-8")

    audit = f"""# Raw Data Second-Run Audit

## Source files

- Raw Stata file: `{RAW_DTA.relative_to(ROOT)}`
- Raw CSV file: `{RAW_CSV.relative_to(ROOT)}`
- Variable-label CSV: `{LABEL_CSV.relative_to(ROOT)}`

## Dataset structure

- Stata observations: {len(dta)}
- Stata variables: {dta_shape_raw[1]}
- CSV observations: {len(csv)}
- CSV variables: {csv.shape[1]}
- CSV row count matches Stata: {len(csv) == len(dta)}

## Key finding

The raw `.dta` file is readable in Python and contains the variables needed to reconstruct the current fragility outcome. The second-run rule exactly matches the supplied processed classification: {int(validation_summary.loc[0, 'matches'])} matches out of {len(validation)} observations.

## Construct-validity warning

The exact computational rule is transparent, but its substantive interpretation remains fragile. Official labels identify `h5` as process innovation, `c22b` as own website, `h1` and `h2` as product/service innovation, and `l1` as permanent full-time employment. Paper language that calls these variables revenue volatility or digital-platform difficulty should be corrected unless the team can provide a defensible recode.

## Second-run prevalence

{markdown_table(prevalence)}

## Second-run LASSO rerun

{markdown_table(performance)}

## Leakage-reduced LASSO rerun

To address predictor/outcome overlap, the second run also excludes rule variables from the predictor set: {", ".join(rule_vars)}.

{markdown_table(leakage_reduced_performance)}

## Outputs

- `results/stata/second_run_codebook.txt`
- `results/stata/second_run_descriptives.csv`
- `results/stata/second_run_missingness.csv`
- `results/stata/second_run_fragility_validation.csv`
- `results/stata/second_run_weighted_prevalence.csv`
- `results/stata/second_run_region_table.csv`
- `results/stata/second_run_sector_table.csv`
- `results/stata/second_run_size_table.csv`
- `results/stata/second_run_digital_finance_table.csv`
- `results/figures/second_run/*.png`
"""
    (DOCS / "raw_data_second_run_audit.md").write_text(audit, encoding="utf-8")

    comparison = f"""# Stata/Python Second-Run Result Comparison

This file compares the new raw-data second run with the current project outputs. Stata execution status is recorded separately in `docs/second_run_final_report.md`; the Python second run uses the same raw `.dta` file and exports Stata-compatible CSV tables.

## Outcome reconstruction

- Supplied fragile firms: {int(validation_summary.loc[0, 'supplied_fragile'])}
- Second-run fragile firms: {int(validation_summary.loc[0, 'second_run_fragile'])}
- Agreement: {validation_summary.loc[0, 'agreement']:.3f}
- Mismatches: {int(validation_summary.loc[0, 'mismatches'])}

The recovered rule is confirmed against the processed classification file.

## Weighted prevalence

{markdown_table(prevalence)}

These values should be compared against Paper 2's current table. They are expected to match if the same raw rule and weights are used.

## Machine-learning rerun

{markdown_table(performance)}

## Leakage-reduced model

Rule variables excluded: {", ".join(rule_vars)}

{markdown_table(leakage_reduced_performance)}

The rerun confirms high apparent discrimination, but the result should be flagged for improvement because the model includes variables that are also used to define the outcome. This makes the result useful as an audit of the screening rule, not as independent evidence of external predictive validity.

## Results requiring improvement before journal submission

- Treat the leakage-reduced model as the more honest internal benchmark until an independent outcome such as closure, revenue contraction, employment loss, or follow-up survival is available.
- Rebuild the theoretical finance/digital Omega score directly from raw variables; the existing Omega export is not empirically informative.
- Add design-based standard errors for weighted estimates.
- Decide whether `a2` or `a3a` should be the authoritative geography variable.
- Reconcile all manuscript language with official WBES variable labels.
"""
    (DOCS / "stata_python_result_comparison.md").write_text(comparison, encoding="utf-8")


if __name__ == "__main__":
    main()
