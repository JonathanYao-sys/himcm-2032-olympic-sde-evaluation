#!/usr/bin/env python3
"""HiMCM Inclusivity submodel.

Change CSV_FILE below, or pass a CSV path on the command line:
    python3 inclusivity_model.py /path/to/data.csv

The script only prints results to the terminal and does not create output files.
"""
from __future__ import annotations

import csv
import math
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Iterable

# =============================================================================
# 1. CSV FILE TO RUN
# =============================================================================
# Edit this path directly, or override it with: python3 inclusivity_model.py FILE
CSV_FILE = "inclusivity_data.csv"

# =============================================================================
# 2. MODEL CONSTANTS
# =============================================================================
CONTINENTS = ("Africa", "Americas", "Asia", "Europe", "Oceania")

REQUIRED_COLUMNS = {
    "sde_id",
    "sde_name",
    "period_order",
    "period_label",
    "country_code",
    "country_name",
    "continent",
    "m49_subregion",
    "unit_type",
    "activity_status",
    "coverage_status",
    "source",
    "notes",
}

ACTIVITY_ALIASES = {
    "active": "active",
    "1": "active",
    "yes": "active",
    "y": "active",
    "true": "active",
    "inactive": "inactive",
    "0": "inactive",
    "no": "inactive",
    "n": "inactive",
    "false": "inactive",
    "unknown": "unknown",
    "not_applicable": "not_applicable",
    "n/a": "not_applicable",
    "na": "not_applicable",
}

COVERAGE_ALIASES = {
    "complete": "complete",
    "full": "complete",
    "partial": "partial",
    "unknown": "unknown",
    "not_applicable": "not_applicable",
    "n/a": "not_applicable",
    "na": "not_applicable",
}

GATE_N = 75
GATE_K = 4
WORLD_REFERENCE_N = 206
CONTINENT_DEPTH_REFERENCE = 15
SUBREGION_COUNT = 22
QUALITY_THRESHOLD = 0.75

WEIGHTS = {
    "P": 0.35,
    "D": 0.25,
    "B": 0.20,
    "R": 0.10,
    "T": 0.10,
}


# =============================================================================
# 3. BASIC HELPERS
# =============================================================================
def normalize_activity(value: str) -> str:
    key = value.strip().casefold().replace(" ", "_")
    if key not in ACTIVITY_ALIASES:
        raise ValueError(
            "activity_status must be active/inactive/unknown/not_applicable "
            f"(received: {value!r})"
        )
    return ACTIVITY_ALIASES[key]


def normalize_coverage(value: str) -> str:
    key = value.strip().casefold().replace(" ", "_")
    if key not in COVERAGE_ALIASES:
        raise ValueError(
            "coverage_status must be complete/partial/unknown/not_applicable "
            f"(received: {value!r})"
        )
    return COVERAGE_ALIASES[key]


def entropy_normalized(counts: Iterable[int], total_categories: int) -> float:
    """Normalized Shannon entropy on [0, 1]."""
    values = [count for count in counts if count > 0]
    total = sum(values)
    if total == 0 or total_categories <= 1:
        return 0.0
    entropy = -sum((count / total) * math.log(count / total) for count in values)
    return entropy / math.log(total_categories)


def reach_score(n: int) -> float:
    """Saturating breadth score P on [0, 1]."""
    n = max(0, min(n, WORLD_REFERENCE_N))
    if n < GATE_N:
        return 0.70 * n / GATE_N
    if WORLD_REFERENCE_N <= GATE_N:
        return 1.0
    numerator = 1.0 - math.exp(-(n - GATE_N) / 50.0)
    denominator = 1.0 - math.exp(
        -(WORLD_REFERENCE_N - GATE_N) / 50.0
    )
    return 0.70 + 0.30 * numerator / denominator


# =============================================================================
# 4. CSV LOADING AND VALIDATION
# =============================================================================
def resolve_csv_path() -> Path:
    raw = sys.argv[1] if len(sys.argv) > 1 else CSV_FILE
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    return path


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise ValueError(f"CSV file not found: {path}")

    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row.")
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
        if missing:
            raise ValueError(
                "CSV is missing required columns: " + ", ".join(sorted(missing))
            )
        rows = list(reader)

    if not rows:
        return []

    normalized_rows: list[dict[str, str]] = []
    duplicates: set[tuple[str, int, str]] = set()

    for line_number, row in enumerate(rows, start=2):
        cleaned = {
            key: (value or "").strip()
            for key, value in row.items()
        }

        for field in (
            "sde_id",
            "sde_name",
            "period_order",
            "period_label",
            "country_code",
            "country_name",
            "continent",
            "m49_subregion",
            "unit_type",
            "activity_status",
            "coverage_status",
        ):
            if not cleaned[field]:
                raise ValueError(f"Line {line_number}: {field} cannot be empty.")

        try:
            cleaned["period_order"] = int(cleaned["period_order"])
        except ValueError as exc:
            raise ValueError(
                f"Line {line_number}: period_order must be an integer."
            ) from exc

        if cleaned["period_order"] < 1:
            raise ValueError(
                f"Line {line_number}: period_order must be at least 1."
            )

        if cleaned["continent"] not in CONTINENTS:
            raise ValueError(
                f"Line {line_number}: continent must be one of "
                + ", ".join(CONTINENTS)
            )

        cleaned["activity_status"] = normalize_activity(cleaned["activity_status"])
        cleaned["coverage_status"] = normalize_coverage(cleaned["coverage_status"])

        if cleaned["activity_status"] == "active" and not cleaned["source"]:
            raise ValueError(
                f"Line {line_number}: an active row must have a source."
            )

        key = (
            cleaned["sde_id"],
            cleaned["period_order"],
            cleaned["country_code"],
        )
        if key in duplicates:
            raise ValueError(
                f"Line {line_number}: duplicate sde_id/period/country: {key}"
            )
        duplicates.add(key)
        normalized_rows.append(cleaned)

    return normalized_rows


# =============================================================================
# 5. PERIOD METRICS
# =============================================================================
def period_metrics(rows: list[dict[str, str]]) -> dict[str, object]:
    active = [row for row in rows if row["activity_status"] == "active"]

    continent_counts = {continent: 0 for continent in CONTINENTS}
    subregion_counts: dict[str, int] = defaultdict(int)
    for row in active:
        continent_counts[row["continent"]] += 1
        subregion_counts[row["m49_subregion"]] += 1

    n = len(active)
    k = sum(value > 0 for value in continent_counts.values())

    return {
        "N": n,
        "K": k,
        "continent_counts": continent_counts,
        "subregion_counts": dict(subregion_counts),
    }


def period_coverage(rows: list[dict[str, str]]) -> str:
    statuses = {
        row["coverage_status"]
        for row in rows
        if row["coverage_status"] != "not_applicable"
    }
    if not statuses:
        return "not_applicable"
    if statuses == {"complete"}:
        return "complete"
    if statuses == {"partial"}:
        return "partial"
    if statuses == {"unknown"}:
        return "unknown"
    return "mixed"


def is_period_assessable(rows: list[dict[str, str]]) -> bool:
    coverage = period_coverage(rows)
    has_active = any(row["activity_status"] == "active" for row in rows)
    return has_active or coverage in {"complete", "partial"}


# =============================================================================
# 6. INCLUSIVITY MODEL
# =============================================================================
def calculate_sde(
    sde_id: str,
    sde_name: str,
    periods: dict[int, list[dict[str, str]]],
    period_labels: dict[int, str],
) -> dict[str, object]:
    ordered_periods = sorted(periods)
    current_order = ordered_periods[-1]
    current_rows = periods[current_order]
    current = period_metrics(current_rows)

    n_current = int(current["N"])
    k_current = int(current["K"])
    continent_counts = dict(current["continent_counts"])
    subregion_counts = dict(current["subregion_counts"])

    p = reach_score(n_current)
    d = sum(
        min(count / CONTINENT_DEPTH_REFERENCE, 1.0)
        for count in continent_counts.values()
    ) / len(CONTINENTS)
    b = entropy_normalized(continent_counts.values(), len(CONTINENTS))
    r = entropy_normalized(subregion_counts.values(), SUBREGION_COUNT)

    period_scores: list[float] = []
    periods_used: list[int] = []
    period_summary: list[dict[str, object]] = []

    for order in ordered_periods:
        rows = periods[order]
        metrics = period_metrics(rows)
        coverage = period_coverage(rows)
        assessable = is_period_assessable(rows)

        period_summary.append(
            {
                "period_order": order,
                "period_label": period_labels.get(order, f"Period {order}"),
                "N": metrics["N"],
                "K": metrics["K"],
                "coverage": coverage,
                "assessable": assessable,
            }
        )

        if not assessable:
            continue

        period_score = 0.5 * min(int(metrics["N"]) / GATE_N, 1.0) + 0.5 * min(
            int(metrics["K"]) / GATE_K, 1.0
        )
        period_scores.append(period_score)
        periods_used.append(order)

    t = mean(period_scores) if period_scores else 0.0

    i_score = (
        WEIGHTS["P"] * p
        + WEIGHTS["D"] * d
        + WEIGHTS["B"] * b
        + WEIGHTS["R"] * r
        + WEIGHTS["T"] * t
    )

    gate_pass = n_current >= GATE_N and k_current >= GATE_K
    quality_pass = i_score >= QUALITY_THRESHOLD
    final_pass = gate_pass and quality_pass

    return {
        "sde_id": sde_id,
        "sde_name": sde_name,
        "current_order": current_order,
        "current_label": period_labels.get(current_order, f"Period {current_order}"),
        "current_coverage": period_coverage(current_rows),
        "N_current": n_current,
        "K_current": k_current,
        "continent_counts": continent_counts,
        "subregion_counts": subregion_counts,
        "P": p,
        "D": d,
        "B": b,
        "R": r,
        "T": t,
        "I": i_score,
        "gate_pass": gate_pass,
        "quality_pass": quality_pass,
        "final_pass": final_pass,
        "period_summary": period_summary,
        "periods_used_for_T": periods_used,
    }


# =============================================================================
# 7. REPORTING
# =============================================================================
def print_sde_report(result: dict[str, object]) -> None:
    print("\n" + "=" * 78)
    print(f"SDE: {result['sde_id']} | {result['sde_name']}")
    print("=" * 78)
    print(
        f"Current period: {result['current_order']} | "
        f"{result['current_label']}"
    )
    print(
        f"Current coverage: {result['current_coverage']} | "
        f"N = {result['N_current']} | K = {result['K_current']}"
    )

    print("\nPeriod summary")
    for item in result["period_summary"]:
        print(
            f"  {item['period_order']}: {item['period_label']} | "
            f"N={item['N']} K={item['K']} | "
            f"coverage={item['coverage']} | "
            f"included_in_T={item['assessable']}"
        )

    continents = result["continent_counts"]
    print("\nContinental distribution (current period)")
    print(
        "  "
        + " | ".join(f"{continent}: {continents[continent]}" for continent in CONTINENTS)
    )

    print("\nSubregion count (current period)")
    print(f"  represented_subregions = {len(result['subregion_counts'])}")

    print("\nFactor values (all on 0-1 scale)")
    print(f"  P (breadth)                 = {result['P']:.6f}")
    print(f"  D (continental depth)       = {result['D']:.6f}")
    print(f"  B (continental balance)     = {result['B']:.6f}")
    print(f"  R (subregional coverage)    = {result['R']:.6f}")
    print(f"  T (temporal persistence)    = {result['T']:.6f}")
    print(
        "\nWeights: "
        f"P={WEIGHTS['P']:.2f}, D={WEIGHTS['D']:.2f}, "
        f"B={WEIGHTS['B']:.2f}, R={WEIGHTS['R']:.2f}, "
        f"T={WEIGHTS['T']:.2f}"
    )
    print(f"I = 0.35P + 0.25D + 0.20B + 0.10R + 0.10T")
    print(f"I (inclusivity quality)     = {result['I']:.6f}")

    print("\nDecision")
    print(f"  Quality threshold: {QUALITY_THRESHOLD:.2f}")
    print(f"  Gate_pass   = {result['gate_pass']}")
    print(f"  Quality_pass= {result['quality_pass']}")
    print(f"  Final_pass  = {result['final_pass']}")
    print(
        "  Note: Gate uses current N>=75 and K>=4; "
        "Quality_pass is I>=threshold."
    )


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
            "Fill inclusivity_data.csv using the schema in README.md, "
            "then run this script again."
        )
        return 0

    grouped: dict[str, dict[int, list[dict[str, str]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    sde_names: dict[str, str] = {}
    period_labels: dict[tuple[str, int], str] = {}

    for row in rows:
        sde_id = row["sde_id"]
        order = int(row["period_order"])
        grouped[sde_id][order].append(row)
        sde_names[sde_id] = row["sde_name"]
        period_labels[(sde_id, order)] = row["period_label"]

    for sde_id in sorted(grouped):
        result = calculate_sde(
            sde_id=sde_id,
            sde_name=sde_names[sde_id],
            periods=dict(grouped[sde_id]),
            period_labels={
                order: period_labels[(sde_id, order)]
                for order in grouped[sde_id]
            },
        )
        print_sde_report(result)

    print(f"\nCalculation complete. CSV used: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
