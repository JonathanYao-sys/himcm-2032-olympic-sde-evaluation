#!/usr/bin/env python3
"""Gender Equality submodel.

Factors:
X1: current athlete gender balance
X2: current event gender balance
X3: 2032 trend forecast of female athlete ratio

Final Score = (X1 + X2 + X3) / 3, on a 0-1 scale.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

# =============================================================================
# 1. FILE SETTINGS
# =============================================================================
DATA_GLOB = "*.csv"
OUTPUT_FILE = "output.md"

# =============================================================================
# 2. HELPERS
# =============================================================================
def read_csv(name: str) -> list[dict[str, str]]:
    path = Path(__file__).resolve().parent / name
    if not path.exists():
        raise ValueError(f"CSV file not found: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def as_float(value: str) -> float:
    return float(str(value).strip())


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def balance_score(ratio: float) -> float:
    return clamp01(1.0 - 2.0 * abs(ratio - 0.5))


def linear_regression(xs: list[float], ys: list[float]) -> tuple[float, float]:
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("Linear regression requires at least two observations.")
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if denominator == 0:
        raise ValueError("Years must contain at least two distinct values.")
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / denominator
    intercept = y_mean - slope * x_mean
    return intercept, slope


# =============================================================================
# 3. LOAD DATA
# =============================================================================
def load_data() -> tuple[list[dict[str, object]], dict[str, dict[str, float]], dict[str, list[dict[str, float]]]]:
    root = Path(__file__).resolve().parent
    csv_paths = sorted(
        path for path in root.glob(DATA_GLOB)
        if path.name != OUTPUT_FILE
    )
    if not csv_paths:
        raise ValueError("No per-sport CSV files found.")

    current: list[dict[str, object]] = []
    events: dict[str, dict[str, float]] = {}
    history_by_sport: dict[str, list[dict[str, float]]] = {}

    for path in csv_paths:
        with path.open("r", newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            continue

        sport = rows[0]["sport"]
        current_row = None
        for row in rows:
            if str(row.get("is_current", "0")).strip() in {"1", "true", "yes"}:
                current_row = row
            try:
                male = as_float(row["male_athletes"])
                female = as_float(row["female_athletes"])
                year = as_float(row["year"])
            except (KeyError, ValueError) as exc:
                raise ValueError(f"{path.name}: invalid athlete/year row.") from exc
            history_by_sport.setdefault(sport, []).append(
                {"year": year, "male": male, "female": female}
            )

        if current_row is None:
            raise ValueError(f"{path.name}: missing is_current marker.")
        try:
            male = as_float(current_row["male_athletes"])
            female = as_float(current_row["female_athletes"])
            male_events = as_float(current_row["male_events"])
            female_events = as_float(current_row["female_events"])
        except (KeyError, ValueError) as exc:
            raise ValueError(f"{path.name}: current row is incomplete.") from exc

        total = male + female
        if total <= 0:
            raise ValueError(f"{sport}: athlete total must be positive.")
        current.append(
            {
                "sde_id": current_row.get("sde_id", ""),
                "sport": sport,
                "male": male,
                "female": female,
                "female_ratio": female / total,
                "source": current_row.get("source", ""),
            }
        )
        events[sport] = {"male": male_events, "female": female_events}

    return current, events, history_by_sport


# =============================================================================
# 4. EVALUATE
# =============================================================================
def evaluate() -> list[dict[str, object]]:
    current, events, history = load_data()
    results: list[dict[str, object]] = []

    for row in current:
        sport = str(row["sport"])
        female_ratio = float(row["female_ratio"])
        x1 = balance_score(female_ratio)

        event = events.get(sport)
        if not event:
            raise ValueError(f"Missing event data for {sport}")
        em, ef = float(event["male"]), float(event["female"])
        x2 = 0.0 if max(em, ef) == 0 else min(em, ef) / max(em, ef)

        points = sorted(history.get(sport, []), key=lambda item: item["year"])
        ratios = [
            item["female"] / (item["male"] + item["female"])
            for item in points
            if item["male"] + item["female"] > 0
        ]
        years = [item["year"] for item in points if item["male"] + item["female"] > 0]

        if len(set(years)) >= 2:
            intercept, slope = linear_regression(years, ratios)
            predicted_2032 = clamp01(intercept + slope * 2032.0)
            x3 = balance_score(predicted_2032)
            trend_source = "linear regression on available history"
        else:
            predicted_2032 = female_ratio
            x3 = x1
            trend_source = "one available period; current parity used"

        score = (x1 + x2 + x3) / 3.0
        results.append(
            {
                "sde_id": row["sde_id"],
                "sport": sport,
                "male": row["male"],
                "female": row["female"],
                "female_ratio": female_ratio,
                "x1": x1,
                "male_events": em,
                "female_events": ef,
                "x2": x2,
                "predicted_2032": predicted_2032,
                "x3": x3,
                "score": score,
                "source": row["source"],
                "trend_source": trend_source,
            }
        )

    results.sort(key=lambda item: float(item["score"]), reverse=True)
    for rank, row in enumerate(results, start=1):
        row["rank"] = rank
    return results


# =============================================================================
# 5. REPORT
# =============================================================================
def print_report(results: list[dict[str, object]]) -> None:
    print("\nGender Equality Submodel")
    print("=" * 112)
    print(
        f"{'Rank':<6}{'SDE':<38}{'X1':<10}{'X2':<10}"
        f"{'P_2032':<12}{'X3':<10}{'Score_0_1':<12}"
    )
    print("-" * 112)
    for row in results:
        print(
            f"{int(row['rank']):<6}"
            f"{str(row['sport']):<38}"
            f"{float(row['x1']):<10.6f}"
            f"{float(row['x2']):<10.6f}"
            f"{float(row['predicted_2032']):<12.6f}"
            f"{float(row['x3']):<10.6f}"
            f"{float(row['score']):<12.6f}"
        )
    print("=" * 112)


def write_output_md(results: list[dict[str, object]]) -> None:
    path = Path(__file__).resolve().parent / OUTPUT_FILE
    lines: list[str] = []
    lines.append("# Gender Equality Model Results\n")
    lines.append("## 结果口径\n")
    lines.append("- `X1`：当前男女运动员比例平衡。")
    lines.append("- `X2`：当前男女项目比例平衡。")
    lines.append("- `X3`：历史女子参与比例线性回归到 2032 年的平衡预测。")
    lines.append("- 最终得分 `Score = (X1 + X2 + X3) / 3`，范围为 `0–1`。")
    lines.append("- Olympedia 的参赛人数按项目事件汇总，可能对多项目运动员重复计数。")
    lines.append("- 2028 新增项目使用 LA28 计划的男女配额作为代理。\n")
    lines.append("## 汇总表\n")
    lines.append("| 排名 | SDE | 女性比例 | X1 | 男/女项目 | X2 | 2032预测女性比例 | X3 | Score |")
    lines.append("|---:|---|---:|---:|---|---:|---:|---:|---:|")
    for row in results:
        lines.append(
            f"| {int(row['rank'])} | {row['sport']} | {float(row['female_ratio']):.4f} | "
            f"{float(row['x1']):.4f} | {float(row['male_events']):g}/{float(row['female_events']):g} | "
            f"{float(row['x2']):.4f} | {float(row['predicted_2032']):.4f} | "
            f"{float(row['x3']):.4f} | {float(row['score']):.4f} |"
        )
    lines.append("\n## 逐项结果\n")
    for row in results:
        lines.append(f"### {row['sport']}\n")
        lines.append(f"- 当前男运动员：{float(row['male']):.0f}")
        lines.append(f"- 当前女运动员：{float(row['female']):.0f}")
        lines.append(f"- 当前女性比例：{float(row['female_ratio']):.4f}")
        lines.append(f"- X1 = {float(row['x1']):.4f}")
        lines.append(
            f"- 项目数：男子 {float(row['male_events']):g}，女子 {float(row['female_events']):g}"
        )
        lines.append(f"- X2 = {float(row['x2']):.4f}")
        lines.append(f"- 2032 年预测女性比例：{float(row['predicted_2032']):.4f}")
        lines.append(f"- X3 = {float(row['x3']):.4f}")
        lines.append(f"- 最终 Score = {float(row['score']):.4f}")
        lines.append(f"- 趋势来源：{row['trend_source']}\n")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    try:
        results = evaluate()
    except (OSError, ValueError) as error:
        print(f"Input error: {error}")
        return 2
    print_report(results)
    write_output_md(results)
    print(f"\nResults written to: {Path(__file__).resolve().parent / OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
