# HiMCM 2024 Problem A - Olympic SDE Evaluation

A multi-criteria evaluation framework for assessing whether sports, disciplines, or events (SDEs) should be retained, added, or reconsidered for future Summer Olympic Games.

This repository implements six IOC-aligned dimensions and one overall aggregation model:

1. Popularity and Accessibility
2. Inclusivity
3. Fairness and Safety
4. Sustainability
5. Relevance and Innovation
6. Gender Equity

The project uses transparent CSV inputs and Python scripts based mainly on the standard library. All model scores are normalized to `0-1`.

## Repository Structure

```text
.
├── popularity_accessibility/   # Popularity and Accessibility data and method
├── inclusivity/                # Inclusivity model and country-level evidence
├── safety_fair_play/           # Safety and Fair Play model
├── sustainability/             # Sustainability model
├── innovation/                 # Relevance and Innovation model
├── gender_equality/            # Gender Equity model
├── overall/                    # Overall aggregation and ranking
├── requirements.txt            # Optional dependencies for legacy scripts
└── LICENSE
```

Each submodel keeps its own README, data files, code, and generated outputs where applicable.

## Model Overview

| Dimension | Main Inputs | Output |
|---|---|---|
| Popularity and Accessibility | View share, attendance, nations, registered athletes, followers, cost | `Popularity_Score` |
| Inclusivity | Country activity coverage, continental spread, continuity | `I` |
| Fairness and Safety | Doping screening, injury rate, fairness enforcement | `Safety_Score` |
| Sustainability | Resource impact and carbon impact proxies | `S` |
| Relevance and Innovation | Youth appeal and recency | `Innovation_Score` |
| Gender Equity | Athlete balance, event balance, 2032 trend | `Gender_Score` |

The overall model combines the six dimensions with a hybrid weighting scheme:

```text
Overall = sum_k w_k * D_k
w_k = alpha * w_fixed + (1 - alpha) * w_entropy
```

See `overall/README.md` for the complete aggregation formula.

## Quick Start

Python 3.10 or newer is recommended.

Install optional dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the Inclusivity model:

```bash
cd inclusivity
python3 inclusivity_model.py 篮球.csv
```

Run with the blank template:

```bash
cd inclusivity
python3 inclusivity_model.py
```

Other entry points:

```bash
cd safety_fair_play
python3 safety_fair_play_model.py

cd ../sustainability
python3 sustainability_model.py 篮球.csv

cd ../innovation
python3 innovation_model.py

cd ../gender_equality
python3 gender_equality_model.py

cd ../overall
python3 overall_model.py
```

The Popularity and Accessibility folder currently contains the method description and CSV data. The original calculation script was provided separately by the project team.

## Data Files

- Most CSV files use UTF-8 encoding.
- Chinese project filenames are preserved to match the team's collection workflow.
- Source fields and notes describe the current provenance of each dataset.
- Several indicators are proxy variables because uniform global data are not available for every SDE.

## Methodological Notes

- The IOC's explicit Inclusivity threshold is `N >= 75` countries and `K >= 4` continents.
- Inclusivity uses breadth, continental depth, continental balance, subregional representation, and temporal persistence.
- Safety, Sustainability, and Innovation use entropy weighting where specified in their submodel README files.
- Gender Equity combines current athlete balance, event balance, and a 2032 trend estimate.
- The Overall model applies a hybrid equal-prior and entropy-weight scheme. Weights can be changed in `overall/overall_model.py`.

## Limitations

1. Some datasets are proxies rather than complete global censuses.
2. Source links are not uniformly available for every legacy input.
3. Popularity and Accessibility currently lacks a separate Accessibility indicator.
4. Country membership counts do not perfectly measure active participation.
5. The Overall ranking is a decision-support output, not an IOC decision.

## License

This project is released under the MIT License. See `LICENSE`.

## Author

Created by [JonathanYao-sys](https://github.com/JonathanYao-sys) for HiMCM 2024 Problem A.
