import numpy as np
import pandas as pd

# ==========================================
# 1. Input your collected data for the 3 indicators
# ==========================================
# Note: injury_rate values are from "normalized" column.
# fairness_enforcement values are from "has_tech(1/0)" column.
# doping_screening is all 1 based on your input.
data = pd.DataFrame({
    "entity": [
        "Boxing",
        "Breaking",
        "Karate",
        "Cricket",
        "Flag football",
        "Squash",
        "Lacrosse Sixes",
        "Cycling track",
        "Athletics",
        "Fencing",
        "Swimming",
        "Judo",
        "Modern Pentathlon",
        "Shooting",
        "Badminton",
        "Weightlifting",
        "Tennis",
        "Football",
        "Basketball",
        "Diving",
        "Field Hockey"
    ],
    "doping_screening": [
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
    ],
    "injury_rate": [
        0.6583,  # Boxing
        0.2183,  # Breaking
        0.5333,  # Karate
        1.0000,  # Cricket
        0.3083,  # Flag football
        0.5917,  # Squash
        0.2667,  # Lacrosse Sixes
        0.1500,  # Cycling track
        0.2750,  # Athletics
        0.1167,  # Fencing
        0.0333,  # Swimming
        0.5583,  # Judo
        0.3250,  # Modern Pentathlon
        0.0000,  # Shooting
        0.4167,  # Badminton
        0.4833,  # Weightlifting
        0.3917,  # Tennis
        0.7417,  # Football
        0.8167,  # Basketball
        0.0750,  # Diving
        0.6167  # Field Hockey
    ],
    "fairness_enforcement": [
        1,  # Boxing
        0,  # Breaking
        1,  # Karate
        1,  # Cricket
        1,  # Flag football
        1,  # Squash
        1,  # Lacrosse Sixes
        1,  # Cycling track
        1,  # Athletics
        1,  # Fencing
        1,  # Swimming
        1,  # Judo
        1,  # Modern Pentathlon
        1,  # Shooting
        1,  # Badminton
        0,  # Weightlifting
        1,  # Tennis
        1,  # Football
        1,  # Basketball
        0,  # Diving
        1  # Field Hockey
    ]
})

# ==========================================
# 2. Indicator Direction Setting (1 = Positive, -1 = Negative)
# ==========================================
direction = {
    "doping_screening": 1,
    "injury_rate": -1,
    "fairness_enforcement": 1
}

# ==========================================
# 3. Data Normalization (Min-Max Normalization)
# ==========================================
X = data[list(direction.keys())].astype(float).copy()
X_norm = pd.DataFrame(index=X.index, columns=X.columns)

for col in X.columns:
    x = X[col]
    xmin, xmax = x.min(), x.max()

    # Prevent division by zero if all values are the same
    if xmax == xmin:
        X_norm[col] = 1.0
    else:
        if direction[col] == 1:
            X_norm[col] = (x - xmin) / (xmax - xmin)
        else:
            X_norm[col] = (xmax - x) / (xmax - xmin)

# Add a tiny value to avoid log(0) errors later
X_norm = X_norm + 1e-12

# ==========================================
# 4. Entropy Weight Method Calculation
# ==========================================
n, m = X_norm.shape

# (1) Calculate proportion p_ij
P = X_norm / X_norm.sum(axis=0)

# (2) Calculate entropy e_j
k = 1 / np.log(n)
E = -k * (P * np.log(P)).sum(axis=0)

# (3) Calculate divergence factor d_j
D = 1 - E

# (4) Calculate final weights w_j
W = D / D.sum()

# ==========================================
# 5. Output Results
# ==========================================
print("=" * 40)
print("Entropy Weight Method Results:")
print("=" * 40)
for col, w in zip(X_norm.columns, W):
    print(f"Weight for {col}: {w:.4f}")

print("\nSum of Weights Verification:", round(W.sum(), 4))
print("=" * 40)