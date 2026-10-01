#!/usr/bin/env python3
"""Relevance and Innovation submodel.

Indicators:
1. R1_YoungAppeal
2. R2_YearScore

Method: entropy weighting followed by a 0-1 weighted score.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

# =============================================================================
# 1. CSV FILE TO RUN
# =============================================================================
CSV_FILE = "innovation_data.csv"

# =============================================================================
# 2. MODEL SETTINGS
# =============================================================================
INDICATORS = ("R1_YoungAppeal", "R2_YearScore")
EPSILON = 1e-12
REQUIRED_COLUMNS = {
    "sde_id",
    "sde_name",
    "R1_YoungAppeal",
    "R2_YearScore",
    "source",
    "notes",
}


# =============================================================================
# 3. CSV LOADING AND VALIDATION
# =============================================================================
def resolve_csv_path() -> Path:
    raw = sys.argv[1] if len(sys.argv) > 1 else CSV_FILE
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    return path


def load_rows(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        raise ValueError(f"CSV file not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS.difference(fieldnames)
        if missing:
            raise ValueError("CSV is missing columns: " + ", ".join(sorted(missing)))
        raw_rows = list(reader)

    if not raw_rows:
        return []

    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    for line_number, raw in enumerate(raw_rows, start=2):
        row = {key: (value or "").strip() for key, value in raw.items()}
        for field in ("sde_id", "sde_name", "source", "notes"):
            if not row[field]:
                raise ValueError(f"Line {line_number}: {field} cannot be empty.")
        if row["sde_id"] in seen:
            raise ValueError(f"Line {line_number}: duplicate sde_id: {row['sde_id']}")
        seen.add(row["sde_id"])

        parsed: dict[str, object] = {
            "sde_id": row["sde_id"],
            "sde_name": row["sde_name"],
            "source": row["source"],
            "notes": row["notes"],
        }
        for field in INDICATORS:
            try:
                value = float(row[field])
            except ValueError as exc:
                raise ValueError(f"Line {line_number}: {field} must be numeric.") from exc
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Line {line_number}: {field} must be between 0 and 1."
                )
            parsed[field] = value
        rows.append(parsed)
    return rows


# =============================================================================
# 4. ENTROPY WEIGHTING
# =============================================================================
def entropy_metrics(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    count = len(rows)
    if count <= 1:
        equal_weight = 1.0 / len(INDICATORS)
        return {
            field: {
                "entropy": 0.0,
                "divergence": 1.0,
                "weight": equal_weight,
            }
            for field in INDICATORS
        }

    metrics: dict[str, dict[str, float]] = {}
    for field in INDICATORS:
        values = [float(row[field]) for row in rows]
        total = sum(values)
        if total <= EPSILON:
            metrics[field] = {"entropy": 1.0, "divergence": 0.0, "weight": 0.0}
            continue

        probabilities = [max(value, 0.0) / total for value in values]
        entropy = -sum(
            p * math.log(p) for p in probabilities if p > EPSILON
        ) / math.log(count)
        entropy = min(1.0, max(0.0, entropy))
        metrics[field] = {
            "entropy": entropy,
            "divergence": 1.0 - entropy,
            "weight": 0.0,
        }

    total_divergence = sum(metrics[field]["divergence"] for field in INDICATORS)
    if total_divergence <= EPSILON:
        equal_weight = 1.0 / len(INDICATORS)
        for field in INDICATORS:
            metrics[field]["weight"] = equal_weight
    else:
        for field in INDICATORS:
            metrics[field]["weight"] = metrics[field]["divergence"] / total_divergence
    return metrics


# =============================================================================
# 5. SCORING
# =============================================================================
def evaluate(
    rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, dict[str, float]]]:
    metrics = entropy_metrics(rows)
    results: list[dict[str, object]] = []
    for row in rows:
        score = sum(float(row[field]) * metrics[field]["weight"] for field in INDICATORS)
        results.append({**row, "score": score})

    results.sort(key=lambda row: float(row["score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank
    return results, metrics


# =============================================================================
# 6. OUTPUT
# =============================================================================
def print_report(
    results: list[dict[str, object]],
    metrics: dict[str, dict[str, float]],
) -> None:
    print("\nRelevance and Innovation Submodel")
    print("=" * 92)
    print(f"{'Indicator':<25}{'Entropy':>14}{'Divergence':>16}{'Weight':>14}")
    print("-" * 92)
    for field in INDICATORS:
        item = metrics[field]
        print(
            f"{field:<25}{item['entropy']:>14.6f}"
            f"{item['divergence']:>16.6f}{item['weight']:>14.6f}"
        )
    print("-" * 92)
    print(
        f"{'Total':<25}{'':>14}"
        f"{sum(metrics[field]['divergence'] for field in INDICATORS):>16.6f}"
        f"{sum(metrics[field]['weight'] for field in INDICATORS):>14.6f}"
    )

    print("\n" + "-" * 92)
    print(
        f"{'Rank':<6}{'SDE':<38}{'R1_YoungAppeal':<18}"
        f"{'R2_YearScore':<16}{'Score_0_1':<12}"
    )
    print("-" * 92)
    for row in results:
        print(
            f"{int(row['rank']):<6}"
            f"{str(row['sde_name']):<38}"
            f"{float(row['R1_YoungAppeal']):<18.6f}"
            f"{float(row['R2_YearScore']):<16.6f}"
            f"{float(row['score']):<12.6f}"
        )
    print("=" * 92)


def main() -> int:
    path = resolve_csv_path()
    try:
        rows = load_rows(path)
    except (OSError, ValueError) as error:
        print(f"CSV input error: {error}", file=sys.stderr)
        return 2

    if not rows:
        print(
            f"No data rows found in {path}.\n"
            "Fill innovation_data.csv using the schema in README.md."
        )
        return 0

    results, metrics = evaluate(rows)
    print_report(results, metrics)
    print(f"\nCalculation complete. CSV used: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
