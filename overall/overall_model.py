#!/usr/bin/env python3
"""Overall IOC criteria model.

Combines six 0-1 dimension scores:
popularity_accessibility, inclusivity, safety_fair_play,
sustainability, innovation, gender_equality.

Formula:
    Overall = sum_k w_k * D_k
Weights use a hybrid of equal fixed weights and entropy weights.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

# =============================================================================
# 1. FILE SETTINGS
# =============================================================================
CSV_FILE = "overall_data.csv"
OUTPUT_FILE = "output.md"

# =============================================================================
# 2. MODEL SETTINGS
# =============================================================================
DIMENSIONS = (
    "popularity_accessibility",
    "inclusivity",
    "safety_fair_play",
    "sustainability",
    "innovation",
    "gender_equality",
)
DIMENSION_LABELS = {
    "popularity_accessibility": "Popularity & Accessibility",
    "inclusivity": "Inclusivity",
    "safety_fair_play": "Fairness & Safety",
    "sustainability": "Sustainability",
    "innovation": "Relevance & Innovation",
    "gender_equality": "Gender Equity",
}
FIXED_WEIGHTS = {dimension: 1.0 / len(DIMENSIONS) for dimension in DIMENSIONS}
HYBRID_ALPHA = 0.50
EPSILON = 1e-12
REQUIRED_COLUMNS = {"sde_id", "sde_name", *DIMENSIONS, "source", "notes"}


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

        parsed: dict[str, object] = {
            "sde_id": row["sde_id"],
            "sde_name": row["sde_name"],
            "source": row["source"],
            "notes": row["notes"],
        }
        for dimension in DIMENSIONS:
            try:
                value = float(row[dimension])
            except ValueError as exc:
                raise ValueError(
                    f"Line {line_number}: {dimension} must be numeric."
                ) from exc
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Line {line_number}: {dimension} must be between 0 and 1."
                )
            parsed[dimension] = value
        rows.append(parsed)
    return rows


# =============================================================================
# 4. WEIGHTS
# =============================================================================
def entropy_weights(rows: list[dict[str, object]]) -> dict[str, float]:
    count = len(rows)
    if count <= 1:
        return {dimension: 1.0 / len(DIMENSIONS) for dimension in DIMENSIONS}

    divergences: dict[str, float] = {}
    for dimension in DIMENSIONS:
        values = [float(row[dimension]) for row in rows]
        total = sum(values)
        if total <= EPSILON:
            divergences[dimension] = 0.0
            continue
        probabilities = [max(value, 0.0) / total for value in values]
        entropy = -sum(
            probability * math.log(probability)
            for probability in probabilities
            if probability > EPSILON
        ) / math.log(count)
        entropy = min(1.0, max(0.0, entropy))
        divergences[dimension] = 1.0 - entropy

    total_divergence = sum(divergences.values())
    if total_divergence <= EPSILON:
        return {dimension: 1.0 / len(DIMENSIONS) for dimension in DIMENSIONS}
    return {
        dimension: divergences[dimension] / total_divergence
        for dimension in DIMENSIONS
    }


def hybrid_weights(entropy: dict[str, float]) -> dict[str, float]:
    return {
        dimension: (
            HYBRID_ALPHA * FIXED_WEIGHTS[dimension]
            + (1.0 - HYBRID_ALPHA) * entropy[dimension]
        )
        for dimension in DIMENSIONS
    }


# =============================================================================
# 5. SCORING
# =============================================================================
def score_rows(
    rows: list[dict[str, object]],
    weights: dict[str, float],
) -> list[dict[str, object]]:
    scored: list[dict[str, object]] = []
    for row in rows:
        overall = sum(
            weights[dimension] * float(row[dimension])
            for dimension in DIMENSIONS
        )
        scored.append({**row, "overall": overall})
    scored.sort(key=lambda row: float(row["overall"]), reverse=True)
    for rank, row in enumerate(scored, start=1):
        row["rank"] = rank
    return scored


def rank_map(rows: list[dict[str, object]]) -> dict[str, int]:
    return {str(row["sde_id"]): int(row["rank"]) for row in rows}


# =============================================================================
# 6. REPORT
# =============================================================================
def write_output(
    rows: list[dict[str, object]],
    entropy: dict[str, float],
    weights: dict[str, float],
) -> None:
    equal = score_rows(rows, FIXED_WEIGHTS)
    entropy_ranked = score_rows(rows, entropy)
    hybrid = score_rows(rows, weights)
    equal_ranks = rank_map(equal)
    entropy_ranks = rank_map(entropy_ranked)

    lines: list[str] = []
    lines.append("# Overall IOC Criteria Model Results\n")
    lines.append("## Formula\n")
    lines.append("```text")
    lines.append("Overall = sum_k w_k * D_k")
    lines.append("w_k = alpha * w_fixed + (1-alpha) * w_entropy")
    lines.append("alpha = 0.50")
    lines.append("w_fixed = 1/6 for each of six dimensions")
    lines.append("```\n")
    lines.append("## Final weights (hybrid, 0-1)\n")
    lines.append("| Dimension | Fixed | Entropy | Hybrid final |")
    lines.append("|---|---:|---:|---:|")
    for dimension in DIMENSIONS:
        lines.append(
            f"| {DIMENSION_LABELS[dimension]} | {FIXED_WEIGHTS[dimension]:.4f} | "
            f"{entropy[dimension]:.4f} | {weights[dimension]:.4f} |"
        )
    lines.append("\n## Overall ranking\n")
    lines.append(
        "| Rank | SDE | Popularity | Inclusivity | Safety | Sustainability | "
        "Innovation | Gender | Overall | Equal rank | Entropy rank |"
    )
    lines.append("|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in hybrid:
        sde_id = str(row["sde_id"])
        values = [float(row[dimension]) for dimension in DIMENSIONS]
        lines.append(
            f"| {int(row['rank'])} | {row['sde_name']} | "
            + " | ".join(f"{value:.4f}" for value in values)
            + f" | {float(row['overall']):.4f} | {equal_ranks[sde_id]} | "
            + f"{entropy_ranks[sde_id]} |"
        )
    lines.append("\n## Interpretation notes\n")
    lines.append("- The overall score is a weighted multi-criteria ranking, not a direct measurement of popularity.")
    lines.append("- The hybrid weights use an equal prior because IOC does not specify official weights for the six criteria.")
    lines.append("- The entropy component adjusts weights according to dispersion in the available 21-SDE sample.")
    lines.append("- Popularity & Accessibility is based on the attached image's popularity score; Accessibility is not separately measured in the input data.")
    lines.append("- Sustainability uses the latest Sustainability submodel score S.")
    lines.append("- The result should be accompanied by weight sensitivity analysis in the paper.\n")

    output_path = Path(__file__).resolve().parent / OUTPUT_FILE
    output_path.write_text("\n".join(lines), encoding="utf-8")

    print("Overall IOC criteria model")
    print("=" * 96)
    print("Hybrid weights (0-1):")
    for dimension in DIMENSIONS:
        print(f"  {dimension:<28} {weights[dimension]:.6f}")
    print("\nOverall ranking:")
    print(f"{'Rank':<6}{'SDE':<40}{'Overall':<12}{'Eq':<6}{'Ent':<6}")
    print("-" * 96)
    for row in hybrid:
        sde_id = str(row["sde_id"])
        print(
            f"{int(row['rank']):<6}{str(row['sde_name']):<40}"
            f"{float(row['overall']):<12.6f}{equal_ranks[sde_id]:<6}{entropy_ranks[sde_id]:<6}"
        )
    print("=" * 96)
    print(f"Written: {output_path}")


def main() -> int:
    path = resolve_csv_path()
    try:
        rows = load_rows(path)
    except (OSError, ValueError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2
    if not rows:
        print(f"No data rows found in {path}.")
        return 0

    entropy = entropy_weights(rows)
    weights = hybrid_weights(entropy)
    write_output(rows, entropy, weights)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
