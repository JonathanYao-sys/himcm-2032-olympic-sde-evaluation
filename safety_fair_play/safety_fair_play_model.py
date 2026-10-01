#!/usr/bin/env python3
"""Safety and Fair Play submodel.

Indicators:
1. doping_screening
2. injury_incidence_rate
3. fairness_enforcement

The model performs Min-Max normalization, entropy weighting, and prints
a 0-1 Safety and Fair Play score for each SDE.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

# =============================================================================
# 1. CSV FILE TO RUN
# =============================================================================
CSV_FILE = "safety_fair_play_data.csv"

# =============================================================================
# 2. MODEL SETTINGS
# =============================================================================
INDICATORS = (
    ("doping_screening", 1),
    ("injury_incidence_rate", -1),
    ("fairness_enforcement", 1),
)
EPSILON = 1e-12
REQUIRED_COLUMNS = {
    "sde_id",
    "sde_name",
    "doping_screening",
    "injury_incidence_rate",
    "fairness_enforcement",
    "source",
    "notes",
}


# =============================================================================
# 3. CSV LOADING
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

        try:
            doping = float(row["doping_screening"])
            injury = float(row["injury_incidence_rate"])
            fairness = float(row["fairness_enforcement"])
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: indicator values must be numeric.") from exc

        if doping not in {0.0, 1.0}:
            raise ValueError(f"Line {line_number}: doping_screening must be 0 or 1.")
        if fairness not in {0.0, 1.0}:
            raise ValueError(f"Line {line_number}: fairness_enforcement must be 0 or 1.")
        if not 0.0 <= injury <= 1.0:
            raise ValueError(
                f"Line {line_number}: injury_incidence_rate must be between 0 and 1."
            )

        rows.append(
            {
                "sde_id": row["sde_id"],
                "sde_name": row["sde_name"],
                "doping_screening": doping,
                "injury_incidence_rate": injury,
                "fairness_enforcement": fairness,
                "source": row["source"],
                "notes": row["notes"],
            }
        )
    return rows


# =============================================================================
# 4. NORMALIZATION AND ENTROPY WEIGHTS
# =============================================================================
def normalize_rows(rows: list[dict[str, object]]) -> list[dict[str, float]]:
    normalized: list[dict[str, float]] = [{} for _ in rows]

    for field, direction in INDICATORS:
        values = [float(row[field]) for row in rows]
        low = min(values)
        high = max(values)

        for index, row in enumerate(rows):
            value = float(row[field])
            if abs(high - low) <= EPSILON:
                score = 1.0
            elif direction == 1:
                score = (value - low) / (high - low)
            else:
                score = (high - value) / (high - low)
            normalized[index][field] = score

    return normalized


def entropy_weights(
    normalized: list[dict[str, float]],
) -> dict[str, float]:
    count = len(normalized)
    if count <= 1:
        return {field: 1.0 / len(INDICATORS) for field, _ in INDICATORS}

    entropies: dict[str, float] = {}
    for field, _ in INDICATORS:
        values = [max(row[field], EPSILON) for row in normalized]
        total = sum(values)
        probabilities = [value / total for value in values]
        entropy = -sum(p * math.log(p) for p in probabilities if p > 0)
        entropies[field] = entropy / math.log(count)

    divergences = {field: max(0.0, 1.0 - value) for field, value in entropies.items()}
    total_divergence = sum(divergences.values())
    if total_divergence <= EPSILON:
        return {field: 1.0 / len(INDICATORS) for field, _ in INDICATORS}
    return {field: value / total_divergence for field, value in divergences.items()}


# =============================================================================
# 5. SCORING
# =============================================================================
def evaluate(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], dict[str, float]]:
    normalized = normalize_rows(rows)
    weights = entropy_weights(normalized)

    results: list[dict[str, object]] = []
    for row, norm in zip(rows, normalized):
        score = sum(weights[field] * norm[field] for field, _ in INDICATORS)
        results.append(
            {
                **row,
                **{f"normalized_{field}": norm[field] for field, _ in INDICATORS},
                "score": score,
            }
        )

    results.sort(key=lambda row: float(row["score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank
    return results, weights


# =============================================================================
# 6. OUTPUT
# =============================================================================
def print_results(results: list[dict[str, object]], weights: dict[str, float]) -> None:
    print("\nSafety and Fair Play Submodel")
    print("=" * 102)
    print("Entropy weights (0-1):")
    for field, _ in INDICATORS:
        print(f"  {field:<26} = {weights[field]:.6f}")

    print("\n" + "-" * 102)
    print(
        f"{'Rank':<6}{'SDE':<34}{'Doping_norm':<14}"
        f"{'Injury_norm':<14}{'Fairness_norm':<15}{'Score_0_1':<12}"
    )
    print("-" * 102)
    for row in results:
        print(
            f"{int(row['rank']):<6}"
            f"{str(row['sde_name']):<34}"
            f"{float(row['normalized_doping_screening']):<14.6f}"
            f"{float(row['normalized_injury_incidence_rate']):<14.6f}"
            f"{float(row['normalized_fairness_enforcement']):<15.6f}"
            f"{float(row['score']):<12.6f}"
        )
    print("=" * 102)


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
            "Fill safety_fair_play_data.csv using the schema in README.md."
        )
        return 0

    results, weights = evaluate(rows)
    print_results(results, weights)
    print(f"\nCalculation complete. CSV used: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
