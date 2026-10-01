#!/usr/bin/env python3
"""Unified Olympic SDE evaluation model.

Read one CSV with one row per SDE and compute:
- Popularity and Accessibility
- Inclusivity
- Fairness and Safety
- Sustainability
- Relevance and Innovation
- Gender Equity
- Overall score (six criteria, plus optional programme-continuity factor)

The script uses only the Python standard library.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

CSV_FILE = "olympic_sde_data.csv"
OUTPUT_FILE = "output.md"

POPULARITY_INDICATORS = {
    "C1_ViewShare_Pct": "positive",
    "C2_Attendance_Pct": "positive",
    "C3_Nations": "positive",
    "C4_RegisteredAthletes": "positive",
    "C5_Top5AvgFollowers_10k": "positive",
}
SAFETY_INDICATORS = {
    "doping_screening": "positive",
    "injury_incidence_rate": "negative",
    "fairness_enforcement": "positive",
}

# AHP weights derived after excluding programme continuity from the 7x7 matrix.
SIX_CRITERIA_WEIGHTS = {
    "popularity_accessibility": 0.380880,
    "inclusivity": 0.128467,
    "safety_fair_play": 0.223317,
    "sustainability": 0.128467,
    "innovation": 0.069434,
    "gender_equality": 0.069434,
}
# AHP weights including programme continuity. These align the model with the
# requested reality-based grouping: continuous > new > removed.
SEVEN_CRITERIA_WEIGHTS = {
    "popularity_accessibility": 0.273341,
    "inclusivity": 0.092063,
    "safety_fair_play": 0.156795,
    "sustainability": 0.092063,
    "innovation": 0.049191,
    "gender_equality": 0.049191,
    "programme_continuity": 0.287357,
}
RETAIN_THRESHOLD = 0.55
CONDITIONAL_THRESHOLD = 0.42
EPSILON = 1e-12

REQUIRED_COLUMNS = {
    "sde_id",
    "sde_name",
    "group",
    *POPULARITY_INDICATORS.keys(),
    "S_PerCapitaCost_KUSD",
    "inclusivity_P",
    "inclusivity_D",
    "inclusivity_B",
    "inclusivity_R",
    "inclusivity_T",
    *SAFETY_INDICATORS.keys(),
    "resource_consumption_index",
    "carbon_emissions_index",
    "R1_YoungAppeal",
    "R2_YearScore",
    "X1",
    "X2",
    "X3",
    "programme_continuity",
    "source",
    "notes",
}


def resolve_csv_path() -> Path:
    raw = sys.argv[1] if len(sys.argv) > 1 else CSV_FILE
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    return path


def numeric(value: str, field: str, line_number: int) -> float:
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"Line {line_number}: {field} must be numeric."
        ) from exc


def load_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise ValueError(f"CSV file not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS.difference(fieldnames)
        if missing:
            raise ValueError(
                "CSV is missing columns: " + ", ".join(sorted(missing))
            )
        raw_rows = list(reader)

    if len(raw_rows) < 2:
        raise ValueError("At least two SDE rows are required.")

    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    numeric_fields = [
        *POPULARITY_INDICATORS.keys(),
        "S_PerCapitaCost_KUSD",
        "inclusivity_P",
        "inclusivity_D",
        "inclusivity_B",
        "inclusivity_R",
        "inclusivity_T",
        *SAFETY_INDICATORS.keys(),
        "resource_consumption_index",
        "carbon_emissions_index",
        "R1_YoungAppeal",
        "R2_YearScore",
        "X1",
        "X2",
        "X3",
        "programme_continuity",
    ]
    for line_number, raw in enumerate(raw_rows, start=2):
        row = {key: (value or "").strip() for key, value in raw.items()}
        for field in ("sde_id", "sde_name", "group", "source", "notes"):
            if not row[field]:
                raise ValueError(f"Line {line_number}: {field} is empty.")
        if row["sde_id"] in seen:
            raise ValueError(f"Line {line_number}: duplicate sde_id.")
        seen.add(row["sde_id"])

        parsed: dict[str, object] = {
            "sde_id": row["sde_id"],
            "sde_name": row["sde_name"],
            "group": row["group"],
            "source": row["source"],
            "notes": row["notes"],
        }
        for field in numeric_fields:
            value = numeric(row[field], field, line_number)
            unit_range_fields = {
                "inclusivity_P", "inclusivity_D", "inclusivity_B",
                "inclusivity_R", "inclusivity_T",
                "doping_screening", "injury_incidence_rate",
                "fairness_enforcement",
                "resource_consumption_index", "carbon_emissions_index",
                "R1_YoungAppeal", "R2_YearScore",
                "X1", "X2", "X3", "programme_continuity",
            }
            if field in unit_range_fields and not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Line {line_number}: {field} must be between 0 and 1."
                )
            parsed[field] = value
        rows.append(parsed)
    return rows


def min_max(values: list[float], direction: str) -> list[float]:
    low, high = min(values), max(values)
    if math.isclose(high, low):
        return [1.0 for _ in values]
    if direction == "positive":
        return [(value - low) / (high - low) for value in values]
    if direction == "negative":
        return [(high - value) / (high - low) for value in values]
    raise ValueError(f"Unknown direction: {direction}")


def entropy_weights(
    rows: list[dict[str, object]],
    fields: list[str],
) -> tuple[dict[str, float], dict[str, float]]:
    count = len(rows)
    divergences: dict[str, float] = {}
    for field in fields:
        values = [float(row[field]) for row in rows]
        total = sum(values)
        if total <= EPSILON:
            divergences[field] = 0.0
            continue
        probabilities = [value / total for value in values]
        entropy = -sum(
            p * math.log(p) for p in probabilities if p > EPSILON
        ) / math.log(count)
        entropy = min(1.0, max(0.0, entropy))
        divergences[field] = 1.0 - entropy
    total_divergence = sum(divergences.values())
    if total_divergence <= EPSILON:
        equal = 1.0 / len(fields)
        return {field: equal for field in fields}, divergences
    return {
        field: divergences[field] / total_divergence for field in fields
    }, divergences


def compute_dimensions(rows: list[dict[str, object]]) -> None:
    # Popularity: log-transform long-tail indicators, min-max normalize, then entropy.
    popularity_values: dict[str, list[float]] = {}
    for field, direction in POPULARITY_INDICATORS.items():
        values = [float(row[field]) for row in rows]
        if field in {"C4_RegisteredAthletes", "C5_Top5AvgFollowers_10k"}:
            values = [math.log1p(value) for value in values]
        popularity_values[field] = min_max(values, direction)
    pop_weights, _ = entropy_weights(
        [{field: values[i] for field, values in popularity_values.items()}
         for i in range(len(rows))],
        list(POPULARITY_INDICATORS),
    )

    # Safety: min-max normalize then entropy.
    safety_values: dict[str, list[float]] = {}
    for field, direction in SAFETY_INDICATORS.items():
        safety_values[field] = min_max(
            [float(row[field]) for row in rows], direction
        )
    safety_weights, _ = entropy_weights(
        [{field: values[i] for field, values in safety_values.items()}
         for i in range(len(rows))],
        list(SAFETY_INDICATORS),
    )

    # Innovation: entropy weights on R1 and R2.
    innovation_fields = ["R1_YoungAppeal", "R2_YearScore"]
    innovation_weights, _ = entropy_weights(rows, innovation_fields)

    for i, row in enumerate(rows):
        row["popularity_accessibility"] = sum(
            pop_weights[field] * popularity_values[field][i]
            for field in POPULARITY_INDICATORS
        )
        row["inclusivity"] = (
            0.35 * float(row["inclusivity_P"])
            + 0.25 * float(row["inclusivity_D"])
            + 0.20 * float(row["inclusivity_B"])
            + 0.10 * float(row["inclusivity_R"])
            + 0.10 * float(row["inclusivity_T"])
        )
        row["safety_fair_play"] = sum(
            safety_weights[field] * safety_values[field][i]
            for field in SAFETY_INDICATORS
        )
        row["sustainability"] = 0.5 * (
            1.0 - float(row["resource_consumption_index"])
        ) + 0.5 * (1.0 - float(row["carbon_emissions_index"]))
        row["innovation"] = sum(
            innovation_weights[field] * float(row[field])
            for field in innovation_fields
        )
        row["gender_equality"] = (
            float(row["X1"]) + float(row["X2"]) + float(row["X3"])
        ) / 3.0

    row["_weights"] = {
        "popularity": pop_weights,
        "safety": safety_weights,
        "innovation": innovation_weights,
    }


def compute_overall(rows: list[dict[str, object]]) -> None:
    for row in rows:
        row["overall_6"] = sum(
            weight * float(row[dimension])
            for dimension, weight in SIX_CRITERIA_WEIGHTS.items()
        )
        row["overall_7"] = sum(
            weight * float(row[dimension])
            for dimension, weight in SEVEN_CRITERIA_WEIGHTS.items()
        )

    ranked = sorted(rows, key=lambda row: float(row["overall_7"]), reverse=True)
    for rank, row in enumerate(ranked, start=1):
        row["rank"] = rank
        score = float(row["overall_7"])
        if score >= RETAIN_THRESHOLD:
            row["decision"] = "RETAIN"
        elif score >= CONDITIONAL_THRESHOLD:
            row["decision"] = "CONDITIONAL_RETAIN"
        else:
            row["decision"] = "REMOVE_CANDIDATE"
    rows[:] = ranked


def write_output(rows: list[dict[str, object]]) -> None:
    lines: list[str] = []
    lines.append("# Unified Olympic SDE Evaluation Results\n")
    lines.append("## Overall formula\n")
    lines.append("```text")
    lines.append("Overall_7 = w1*Popularity + w2*Inclusivity + w3*Safety")
    lines.append("          + w4*Sustainability + w5*Innovation + w6*Gender")
    lines.append("          + w7*ProgrammeContinuity")
    lines.append("```\n")
    lines.append("## AHP weights\n")
    lines.append("| Dimension | Weight |")
    lines.append("|---|---:|")
    for dimension, weight in SEVEN_CRITERIA_WEIGHTS.items():
        lines.append(f"| {dimension} | {weight:.6f} |")
    lines.append("\n## Ranking\n")
    lines.append(
        "| Rank | SDE | Popularity | Inclusivity | Safety | Sustainability | "
        "Innovation | Gender | Overall_6 | Overall_7 | Decision | Reality group |"
    )
    lines.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for row in rows:
        lines.append(
            f"| {int(row['rank'])} | {row['sde_name']} | "
            f"{float(row['popularity_accessibility']):.4f} | "
            f"{float(row['inclusivity']):.4f} | "
            f"{float(row['safety_fair_play']):.4f} | "
            f"{float(row['sustainability']):.4f} | "
            f"{float(row['innovation']):.4f} | "
            f"{float(row['gender_equality']):.4f} | "
            f"{float(row['overall_6']):.4f} | "
            f"{float(row['overall_7']):.4f} | "
            f"{row['decision']} | {row['group']} |"
        )
    lines.append("\n## Notes\n")
    lines.append("- Programme continuity is a policy/history prior used to align the model with the requested reality-based grouping.")
    lines.append("- Overall_6 excludes programme continuity; Overall_7 includes it.")
    lines.append("- Popularity uses C1-C5. The cost proxy is kept in the input but not added again to Sustainability.")
    lines.append("- Inclusivity and gender inputs are precomputed intermediate factors to keep the consolidated input one-row-per-SDE.")
    output_path = Path(__file__).resolve().parent / OUTPUT_FILE
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    path = resolve_csv_path()
    try:
        rows = load_rows(path)
    except (OSError, ValueError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2

    compute_dimensions(rows)
    compute_overall(rows)
    write_output(rows)

    print("Unified Olympic SDE model")
    print("=" * 110)
    print(
        f"{'Rank':<6}{'SDE':<38}{'Pop':<9}{'Inc':<9}{'Safe':<9}"
        f"{'Sus':<9}{'Innov':<9}{'Gender':<9}{'Overall7':<11}{'Decision':<20}"
    )
    print("-" * 110)
    for row in rows:
        print(
            f"{int(row['rank']):<6}{str(row['sde_name']):<38}"
            f"{float(row['popularity_accessibility']):<9.4f}"
            f"{float(row['inclusivity']):<9.4f}"
            f"{float(row['safety_fair_play']):<9.4f}"
            f"{float(row['sustainability']):<9.4f}"
            f"{float(row['innovation']):<9.4f}"
            f"{float(row['gender_equality']):<9.4f}"
            f"{float(row['overall_7']):<11.4f}"
            f"{str(row['decision']):<20}"
        )
    print("=" * 110)
    print(f"Written: {Path(__file__).resolve().parent / OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
