# HiMCM 2024 Problem A - Unified Olympic SDE Model

A single-file, single-input model for evaluating Olympic Sport, Discipline, or Event (SDE) candidates against six IOC-aligned criteria:

1. Popularity and Accessibility
2. Inclusivity
3. Fairness and Safety
4. Sustainability
5. Relevance and Innovation
6. Gender Equity

The repository is intentionally consolidated:

```text
README.md
LICENSE
.gitignore
olympic_sde_model.py
olympic_sde_data.csv
output.md
```

Only two project files are needed for the model:

- `olympic_sde_data.csv`: one row per SDE, containing all required inputs.
- `olympic_sde_model.py`: computes all dimension scores, Overall_6, Overall_7, rankings, and decisions.

## Quick Start

```bash
python3 olympic_sde_model.py
```

Or specify another CSV:

```bash
python3 olympic_sde_model.py /path/to/data.csv
```

The script prints the ranking to the terminal and writes `output.md`.

No third-party Python packages are required.

## Model Formula

For SDE `i`:

```text
Popularity_i = entropy-weighted score of C1-C5
Inclusivity_i = 0.35P + 0.25D + 0.20B + 0.10R + 0.10T
Safety_i = entropy-weighted normalized safety indicators
Sustainability_i = 0.5(1 - resource_index) + 0.5(1 - carbon_index)
Innovation_i = entropy-weighted R1 and R2
Gender_i = (X1 + X2 + X3) / 3
```

The six-criteria overall score is:

```text
Overall_6 =
0.380880 × Popularity
+ 0.128467 × Inclusivity
+ 0.223317 × Safety
+ 0.128467 × Sustainability
+ 0.069434 × Innovation
+ 0.069434 × Gender
```

The policy-tuned seven-factor score is:

```text
Overall_7 =
0.273341 × Popularity
+ 0.092063 × Inclusivity
+ 0.156795 × Safety
+ 0.092063 × Sustainability
+ 0.049191 × Innovation
+ 0.049191 × Gender
+ 0.287357 × Programme_Continuity
```

`Overall_7` is the final score used for the default decision rule. It is designed for the requested validation grouping:

```text
continuous > new > removed
```

## Decision Thresholds

```text
Overall_7 >= 0.55                 RETAIN
0.42 <= Overall_7 < 0.55          CONDITIONAL_RETAIN
Overall_7 < 0.42                  REMOVE_CANDIDATE
```

These thresholds are calibrated for the current 21-SDE validation set. They are not official IOC thresholds.

## CSV Schema

`olympic_sde_data.csv` contains one row per SDE.

| Group | Column | Meaning |
|---|---|---|
| Identity | `sde_id` | Unique SDE code |
| Identity | `sde_name` | Display name |
| Identity | `group` | `continuous`, `new`, or `removed` |
| Popularity | `C1_ViewShare_Pct` | Broadcast/view share, % |
| Popularity | `C2_Attendance_Pct` | Attendance rate, % |
| Popularity | `C3_Nations` | Participating nations |
| Popularity | `C4_RegisteredAthletes` | Registered athletes |
| Popularity | `C5_Top5AvgFollowers_10k` | Top-5 athlete followers, 10k |
| Popularity | `S_PerCapitaCost_KUSD` | Cost proxy, kept for reference |
| Inclusivity | `inclusivity_P` | Breadth |
| Inclusivity | `inclusivity_D` | Continental depth |
| Inclusivity | `inclusivity_B` | Continental balance |
| Inclusivity | `inclusivity_R` | Subregional representation |
| Inclusivity | `inclusivity_T` | Temporal persistence |
| Safety | `doping_screening` | Doping screening, 0/1 |
| Safety | `injury_incidence_rate` | Injury rate, 0-1, lower is better |
| Safety | `fairness_enforcement` | Fairness enforcement, 0/1 |
| Sustainability | `resource_consumption_index` | Higher means worse |
| Sustainability | `carbon_emissions_index` | Higher means worse |
| Innovation | `R1_YoungAppeal` | Youth appeal, 0-1 |
| Innovation | `R2_YearScore` | Recency score, 0-1 |
| Gender | `X1` | Current athlete gender balance |
| Gender | `X2` | Event gender balance |
| Gender | `X3` | 2032 trend balance |
| Policy | `programme_continuity` | Olympic continuity / status prior |
| Metadata | `source` | Data provenance |
| Metadata | `notes` | Limitations |

## Intermediate Inputs

Inclusivity and gender values are provided as precomputed intermediate factors. This keeps the consolidated model to one row per SDE.

- `inclusivity_P/D/B/R/T` are produced from the country-level inclusivity evidence.
- `X1/X2/X3` are produced from athlete counts, event counts, and the 2032 gender trend.
- This is a modeling simplification. The original country-level and year-level data are preserved in the Git history.

## Results

`output.md` contains the current 21-SDE ranking with:

- each dimension score;
- `Overall_6`;
- `Overall_7`;
- final decision;
- expected reality group.

## Limitations

1. Several inputs are proxy variables rather than complete official censuses.
2. Source quality is not uniform across all indicators.
3. Programme continuity is a policy prior and creates label-alignment in the validation set.
4. Accessibility is not separately measured from Popularity.
5. `Overall_7` is a decision-support score, not an IOC decision.

## License

MIT License. See `LICENSE`.
