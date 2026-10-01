#!/usr/bin/env python3
"""HiMCM Sustainability submodel.

Two sustainability factors:
1. Resource consumption.
2. Carbon emissions.

Supported data modes:
A. Raw mode:
   energy_kwh_per_athlete_day
   water_m3_per_athlete_day
   carbon_kgco2e_per_athlete_day

B. Proxy-index mode (0-1 impact indices):
   resource_consumption_index
   carbon_emissions_index
   where 0 = very low impact and 1 = very high impact.

All final model outputs are on a 0-1 scale.
The script prints results to the terminal and does not create output files.
"""
from __future__ import annotations

import csv
import math
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

# =============================================================================
# 1. CSV FILE TO RUN
# =============================================================================
CSV_FILE = "sustainability_data.csv"

# =============================================================================
# 2. MODEL SETTINGS
# =============================================================================
# "fixed"   -> use FIXED_WEIGHTS
# "entropy" -> use entropy weights
# "hybrid"  -> combine fixed and entropy weights
WEIGHT_MODE = "hybrid"
FIXED_WEIGHTS = {"resource": 0.50, "carbon": 0.50}
HYBRID_ALPHA = 0.50
SUSTAINABILITY_THRESHOLD = 0.60

BASE_COLUMNS = {
    "sde_id",
    "sde_name",
    "period_order",
    "period_label",
    "coverage_status",
    "source",
    "notes",
}
RAW_COLUMNS = {
    "energy_kwh_per_athlete_day",
    "water_m3_per_athlete_day",
    "carbon_kgco2e_per_athlete_day",
}
INDEX_COLUMNS = {
    "resource_consumption_index",
    "carbon_emissions_index",
}
MISSING_VALUES = {"", "na", "n/a", "null", "none", "nan", "-"}


# =============================================================================
# 3. HELPERS
# =============================================================================
def parse_number(value: str | None) -> float | None:
    cleaned = (value or "").strip()
    if cleaned.casefold() in MISSING_VALUES:
        return None
    try:
        number = float(cleaned)
    except ValueError as exc:
        raise ValueError(f"Expected a number or blank/NA, received {value!r}") from exc
    if number < 0:
        raise ValueError(f"Values cannot be negative: {value!r}")
    return number


def minmax_lower_is_better(values: list[float], value: float) -> float:
    """Normalize a lower-is-better raw indicator to [0, 1], where 1 is best."""
    low = min(values)
    high = max(values)
    if abs(high - low) <= 1e-12:
        return 0.5
    return (high - value) / (high - low)


def entropy_weights(score_matrix: list[dict[str, float]]) -> dict[str, float]:
    """Compute entropy weights for resource and carbon scores."""
    keys = ("resource", "carbon")
    count = len(score_matrix)
    if count <= 1:
        return dict(FIXED_WEIGHTS)

    entropies: dict[str, float] = {}
    for key in keys:
        column = [max(row[key], 1e-12) for row in score_matrix]
        total = sum(column)
        if total <= 0:
            return dict(FIXED_WEIGHTS)
        probabilities = [value / total for value in column]
        entropy = -sum(p * math.log(p) for p in probabilities if p > 0)
        entropies[key] = entropy / math.log(count)

    redundancy = {key: max(0.0, 1.0 - entropies[key]) for key in keys}
    total_redundancy = sum(redundancy.values())
    if total_redundancy <= 1e-12:
        return dict(FIXED_WEIGHTS)
    return {key: redundancy[key] / total_redundancy for key in keys}


def combined_weights(
    score_matrix: list[dict[str, float]],
) -> tuple[dict[str, float], dict[str, float]]:
    if len(score_matrix) < 3:
        entropy = dict(FIXED_WEIGHTS)
    else:
        entropy = entropy_weights(score_matrix)

    if WEIGHT_MODE == "fixed":
        final = dict(FIXED_WEIGHTS)
    elif WEIGHT_MODE == "entropy":
        final = dict(entropy)
    elif WEIGHT_MODE == "hybrid":
        final = {
            key: HYBRID_ALPHA * FIXED_WEIGHTS[key]
            + (1.0 - HYBRID_ALPHA) * entropy[key]
            for key in FIXED_WEIGHTS
        }
        total = sum(final.values())
        final = {key: value / total for key, value in final.items()}
    else:
        raise ValueError("WEIGHT_MODE must be fixed, entropy, or hybrid.")
    return entropy, final


# =============================================================================
# 4. LOAD AND VALIDATE CSV
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
        if not fieldnames:
            raise ValueError("CSV has no header row.")
        missing = BASE_COLUMNS.difference(fieldnames)
        if missing:
            raise ValueError("CSV is missing columns: " + ", ".join(sorted(missing)))
        raw_rows = list(reader)

    if not raw_rows:
        return []

    rows: list[dict[str, object]] = []
    seen: set[tuple[str, int]] = set()

    for line_number, raw in enumerate(raw_rows, start=2):
        row = {key: (value or "").strip() for key, value in raw.items()}
        for field in BASE_COLUMNS:
            if not row.get(field):
                raise ValueError(f"Line {line_number}: {field} cannot be empty.")

        try:
            period_order = int(row["period_order"])
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: period_order must be an integer.") from exc
        if period_order < 1:
            raise ValueError(f"Line {line_number}: period_order must be at least 1.")

        coverage = row["coverage_status"].casefold()
        if coverage not in {"complete", "partial", "unknown"}:
            raise ValueError(
                f"Line {line_number}: coverage_status must be complete, partial, or unknown."
            )

        key = (row["sde_id"], period_order)
        if key in seen:
            raise ValueError(f"Line {line_number}: duplicate sde_id/period: {key}")
        seen.add(key)

        energy = parse_number(row.get("energy_kwh_per_athlete_day"))
        water = parse_number(row.get("water_m3_per_athlete_day"))
        carbon = parse_number(row.get("carbon_kgco2e_per_athlete_day"))
        resource_index = parse_number(row.get("resource_consumption_index"))
        carbon_index = parse_number(row.get("carbon_emissions_index"))

        for label, value in (
            ("resource_consumption_index", resource_index),
            ("carbon_emissions_index", carbon_index),
        ):
            if value is not None and not 0.0 <= value <= 1.0:
                raise ValueError(f"Line {line_number}: {label} must be between 0 and 1.")

        values_present = (
            energy is not None
            or water is not None
            or carbon is not None
            or resource_index is not None
            or carbon_index is not None
        )
        if values_present and not row["source"]:
            raise ValueError(f"Line {line_number}: source is required when values are present.")

        resource_available = (
            resource_index is not None or energy is not None or water is not None
        )
        carbon_available = carbon_index is not None or carbon is not None
        if not resource_available or not carbon_available:
            raise ValueError(
                f"Line {line_number}: each row needs a resource indicator "
                "and a carbon indicator."
            )

        rows.append(
            {
                "sde_id": row["sde_id"],
                "sde_name": row["sde_name"],
                "period_order": period_order,
                "period_label": row["period_label"],
                "energy": energy,
                "water": water,
                "carbon": carbon,
                "resource_index": resource_index,
                "carbon_index": carbon_index,
                "resource_available": resource_available,
                "carbon_available": carbon_available,
                "coverage_status": coverage,
                "source": row["source"],
                "notes": row["notes"],
            }
        )
    return rows


# =============================================================================
# 5. SELECT LATEST ROW PER SDE
# =============================================================================
def select_latest_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["sde_id"])].append(row)

    selected: list[dict[str, object]] = []
    for group in grouped.values():
        candidates = [
            row
            for row in group
            if bool(row["resource_available"]) and bool(row["carbon_available"])
        ]
        if candidates:
            candidates.sort(key=lambda row: int(row["period_order"]), reverse=True)
            selected.append(candidates[0])
    return selected


# =============================================================================
# 6. EVALUATE
# =============================================================================
def evaluate(
    rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, float], dict[str, float]]:
    selected = select_latest_rows(rows)
    if not selected:
        return [], dict(FIXED_WEIGHTS), dict(FIXED_WEIGHTS)

    resource_index_flags = [row["resource_index"] is not None for row in selected]
    carbon_index_flags = [row["carbon_index"] is not None for row in selected]

    if any(resource_index_flags) and not all(resource_index_flags):
        raise ValueError(
            "Do not mix resource_consumption_index and raw resource values "
            "across selected rows for the same factor."
        )
    if any(carbon_index_flags) and not all(carbon_index_flags):
        raise ValueError(
            "Do not mix carbon_emissions_index and raw carbon values "
            "across selected rows for the same factor."
        )

    resource_index_mode = all(resource_index_flags)
    carbon_index_mode = all(carbon_index_flags)

    energy_values = [
        float(row["energy"])
        for row in selected
        if row["energy"] is not None and not resource_index_mode
    ]
    water_values = [
        float(row["water"])
        for row in selected
        if row["water"] is not None and not resource_index_mode
    ]
    carbon_values = [
        float(row["carbon"])
        for row in selected
        if row["carbon"] is not None and not carbon_index_mode
    ]

    working: list[dict[str, object]] = []
    for row in selected:
        if resource_index_mode:
            resource_score = 1.0 - float(row["resource_index"])
            energy_score = None
            water_score = None
        else:
            energy_score = (
                minmax_lower_is_better(energy_values, float(row["energy"]))
                if row["energy"] is not None
                else None
            )
            water_score = (
                minmax_lower_is_better(water_values, float(row["water"]))
                if row["water"] is not None
                else None
            )
            parts = [score for score in (energy_score, water_score) if score is not None]
            resource_score = mean(parts) if parts else 0.0

        if carbon_index_mode:
            carbon_score = 1.0 - float(row["carbon_index"])
        else:
            carbon_score = minmax_lower_is_better(
                carbon_values, float(row["carbon"])
            )

        working.append(
            {
                **row,
                "energy_score": energy_score,
                "water_score": water_score,
                "resource": resource_score,
                "carbon": carbon_score,
            }
        )

    score_matrix = [
        {"resource": float(row["resource"]), "carbon": float(row["carbon"])}
        for row in working
    ]
    entropy, final_weights = combined_weights(score_matrix)

    for row in working:
        row["S"] = (
            final_weights["resource"] * float(row["resource"])
            + final_weights["carbon"] * float(row["carbon"])
        )
        row["pass"] = float(row["S"]) >= SUSTAINABILITY_THRESHOLD

    ordered = sorted(working, key=lambda row: float(row["S"]), reverse=True)
    for rank, row in enumerate(ordered, start=1):
        row["rank"] = rank
    return ordered, entropy, final_weights


# =============================================================================
# 7. PRINT
# =============================================================================
def format_number(value: object) -> str:
    return "NA" if value is None else f"{float(value):.6g}"


def print_report(
    ordered: list[dict[str, object]],
    entropy: dict[str, float],
    final_weights: dict[str, float],
) -> None:
    print("\nHiMCM Sustainability Submodel")
    print("=" * 78)
    print(f"Weight mode: {WEIGHT_MODE}")
    print(
        f"Entropy weights (0-1): resource={entropy['resource']:.4f}, "
        f"carbon={entropy['carbon']:.4f}"
    )
    print(
        f"Final weights (0-1): resource={final_weights['resource']:.4f}, "
        f"carbon={final_weights['carbon']:.4f}"
    )
    print(f"Threshold: S >= {SUSTAINABILITY_THRESHOLD:.2f} (0-1)")

    for row in ordered:
        print("\n" + "-" * 78)
        print(f"SDE: {row['sde_id']} | {row['sde_name']}")
        print(
            f"Period used: {row['period_order']} | {row['period_label']} | "
            f"coverage={row['coverage_status']}"
        )
        print(
            "Raw intensities: "
            f"energy={format_number(row['energy'])} kWh/athlete-day, "
            f"water={format_number(row['water'])} m3/athlete-day, "
            f"carbon={format_number(row['carbon'])} kgCO2e/athlete-day"
        )
        if row["resource_index"] is not None or row["carbon_index"] is not None:
            print(
                "Proxy impact indices (0-1): "
                f"resource_index={format_number(row['resource_index'])}, "
                f"carbon_index={format_number(row['carbon_index'])}"
            )
        print(
            f"Factor scores (0-1): resource={float(row['resource']):.6f}, "
            f"carbon={float(row['carbon']):.6f}"
        )
        print(f"Sustainability score S (0-1) = {float(row['S']):.6f}")
        print(f"Rank = {row['rank']} | Pass = {bool(row['pass'])}")
        if row["source"]:
            print(f"Source: {row['source']}")
        if row["notes"]:
            print(f"Notes: {row['notes']}")


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
            "Fill sustainability_data.csv using the schema in README.md, "
            "then run this script again."
        )
        return 0

    try:
        ordered, entropy, final_weights = evaluate(rows)
    except ValueError as error:
        print(f"CSV input error: {error}", file=sys.stderr)
        return 2

    if not ordered:
        print("No SDE can be assessed with the current data.")
        return 0

    print_report(ordered, entropy, final_weights)
    print("\nCalculation complete. Results are printed to the terminal only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
