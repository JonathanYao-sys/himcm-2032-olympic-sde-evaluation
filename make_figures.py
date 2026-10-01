"""Generate publication-quality figures for the HiMCM Olympic SDE paper.

Usage:
    python3 make_figures.py

Outputs are written to ./figures/ at 300 DPI.
"""

import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# ----------------------------------------------------------------------
# Global style
# ----------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 10.5,
    "axes.edgecolor": "#444444",
    "axes.linewidth": 0.9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------
# Data (from output.md, 21-SDE validation set)
# ----------------------------------------------------------------------
NAMES = [
    "Athletics", "Swimming", "Football", "Basketball", "Tennis",
    "Cycling Track", "Badminton", "Judo", "Shooting", "Fencing",
    "Field Hockey", "Diving", "Modern Pentathlon", "Weightlifting",
    "Flag Football", "Cricket T20", "Lacrosse Sixes", "Squash",
    "Boxing", "Karate", "Breaking",
]
DIMS = ["Popularity", "Inclusivity", "Safety", "Sustainability",
        "Innovation", "Gender Equity"]
M = np.array([
    [0.8608, 0.9815, 0.8765, 0.2500, 0.5254, 0.9971],
    [0.7273, 0.9905, 0.9851, 0.0563, 0.5203, 0.9524],
    [0.7498, 0.9570, 0.6670, 0.2543, 0.4099, 0.9077],
    [0.7258, 0.9722, 0.6334, 0.1730, 0.6016, 0.9953],
    [0.6065, 0.9817, 0.8242, 0.2688, 0.3642, 0.9980],
    [0.4387, 0.9721, 0.9327, 0.1000, 0.3084, 0.8787],
    [0.3790, 0.9698, 0.8129, 0.2212, 0.5305, 0.9780],
    [0.3654, 0.9927, 0.7494, 0.1960, 0.2982, 0.9652],
    [0.1478, 0.9362, 1.0000, 0.3361, 0.4289, 0.9374],
    [0.1844, 0.9301, 0.9476, 0.2922, 0.2932, 0.9967],
    [0.2040, 0.9137, 0.7231, 0.3737, 0.2830, 0.9867],
    [0.4175, 0.9703, 0.4153, 0.0584, 0.3135, 0.9760],
    [0.0475, 0.8740, 0.8541, 0.3030, 0.4492, 1.0000],
    [0.2263, 0.9883, 0.2320, 0.2482, 0.4365, 0.9403],
    [0.2461, 0.8210, 0.8616, 0.6097, 0.7678, 1.0000],
    [0.4716, 0.8963, 0.5511, 0.4259, 0.1726, 1.0000],
    [0.1043, 0.8374, 0.8803, 0.5595, 0.8858, 1.0000],
    [0.1574, 0.8878, 0.7344, 0.3406, 0.1016, 1.0000],
    [0.4256, 0.9886, 0.7045, 0.2378, 0.3693, 0.8112],
    [0.2639, 0.9724, 0.7606, 0.2106, 0.4873, 0.9753],
    [0.1939, 0.7048, 0.3509, 0.5075, 0.8008, 0.9798],
])
O6 = np.array([0.7875, 0.7337, 0.6817, 0.6759, 0.6703, 0.5955, 0.5836,
               0.5470, 0.5379, 0.5284, 0.4927, 0.4734, 0.4607, 0.3925,
               0.5927, 0.5540, 0.5467, 0.4583, 0.5590, 0.5239, 0.4316])
O7 = np.array([0.8484, 0.8094, 0.7732, 0.7690, 0.7645, 0.7106, 0.7022,
               0.6763, 0.6689, 0.6623, 0.6375, 0.6247, 0.6139, 0.5672,
               0.5216, 0.4953, 0.4885, 0.4260, 0.3978, 0.3722, 0.3072])
DECISION = (["RETAIN"] * 14 + ["CONDITIONAL"] * 4 + ["REMOVE"] * 3)
GROUP = (["continuous"] * 14 + ["new"] * 4 + ["removed"] * 3)

C_RETAIN = "#2C6E8F"
C_COND = "#E2A03F"
C_REMOVE = "#B84A44"
DEC_COLOR = {"RETAIN": C_RETAIN, "CONDITIONAL": C_COND, "REMOVE": C_REMOVE}

AHP7 = [("Popularity &\nAccessibility", 0.273341),
        ("Programme\nContinuity", 0.287357),
        ("Fairness &\nSafety", 0.156795),
        ("Inclusivity", 0.092063),
        ("Sustainability", 0.092063),
        ("Relevance &\nInnovation", 0.049191),
        ("Gender\nEquity", 0.049191)]
W6 = [0.380880, 0.128467, 0.223317, 0.128467, 0.069434, 0.069434]

ENT_POP = [("C1 View Share", 0.423525), ("C5 Followers", 0.242221),
           ("C2 Attendance", 0.132669), ("C3 Nations", 0.114611),
           ("C4 Athletes", 0.086975)]
ENT_SAFE = [("Fairness Enf.", 0.551061), ("Injury Rate", 0.448939),
            ("Doping Screen", 0.0)]
ENT_INNO = [("R2 Recency", 0.746116), ("R1 Youth Appeal", 0.253884)]


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)


# ----------------------------------------------------------------------
# Figure 1 — Model framework flowchart
# ----------------------------------------------------------------------
def fig_framework():
    fig, ax = plt.subplots(figsize=(11.5, 6.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.axis("off")

    def box(x, y, w, h, text, fc, ec="#3a3a3a", fs=9.5, tc="white",
            weight="bold", lw=1.2):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
            fc=fc, ec=ec, lw=lw, zorder=2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=fs, color=tc, fontweight=weight, zorder=3,
                linespacing=1.35)

    def arrow(x1, y1, x2, y2, color="#555555", lw=1.6, style="-|>"):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
            color=color, lw=lw, zorder=1,
            connectionstyle="arc3,rad=0.0"))

    # Stage labels on top
    for x, t in [(9, "INPUT"), (38, "DIMENSION LAYER"),
                 (68, "AGGREGATION"), (90, "DECISION")]:
        ax.text(x, 59.5, t, ha="center", fontsize=10.5, color="#666666",
                fontweight="bold")

    # Input boxes
    box(2, 40, 15, 12, "21 Candidate\nSDEs\n(14 continuous,\n4 new, 3 removed)", "#4C5B6B", fs=8.5)
    box(2, 22, 15, 12, "25 Raw\nIndicators\n(broadcast, IOC,\nfederation data)", "#4C5B6B", fs=8.5)
    box(2, 6, 15, 9, "Preprocessing\nlog transform +\nmin–max norm.", "#7A8B99", fs=8)

    dims = [
        ("Popularity &\nAccessibility", "entropy weight\nC1–C5", "#2C6E8F"),
        ("Inclusivity", "P·D·B·R·T\nfixed weights", "#3E7CB1"),
        ("Fairness &\nSafety", "entropy weight\n3 indicators", "#2C6E8F"),
        ("Sustainability", "1 − resource,\n1 − carbon", "#3E7CB1"),
        ("Relevance &\nInnovation", "entropy weight\nR1, R2", "#2C6E8F"),
        ("Gender\nEquity", "(X1+X2+X3)/3", "#3E7CB1"),
    ]
    ys = [51, 41, 31, 21, 11, 1]
    for (name, sub, c), y in zip(dims, ys):
        box(30, y, 17, 7.5, name, c, fs=9)
        ax.text(56.5, y + 3.75, sub, ha="center", va="center",
                fontsize=7.8, color="#444444", style="italic")
        arrow(47.5, y + 3.75, 53, y + 3.75, color="#999999", lw=1.1)

    # Arrows input -> dims
    for y in ys:
        arrow(17.5, 34, 29.5, y + 3.75, color="#bbbbbb", lw=0.9)

    # Aggregation
    box(64, 30, 14, 13, "AHP\nWeights\n(CR < 0.1)", "#8A6FA8", fs=9.5)
    box(64, 14, 14, 11, "Overall₇\nweighted sum\nof 7 factors", "#6B4E8E", fs=9)
    box(64, 44.5, 14, 8, "Overall₆\n(sensitivity:\nno continuity)", "#A68CC4", fs=8)

    for y in ys:
        arrow(58.5, y + 3.75, 63.5, 30, color="#bbbbbb", lw=0.9)
    arrow(71, 30, 71, 25.5, color="#555555")

    # Decision
    box(84, 32, 14, 9, "RETAIN\nOverall₇ ≥ 0.55", "#2C6E8F", fs=8.5)
    box(84, 20, 14, 9, "CONDITIONAL\n0.42 ≤ Overall₇\n< 0.55", "#E2A03F", fs=8)
    box(84, 8, 14, 9, "REMOVE\nOverall₇ < 0.42", "#B84A44", fs=8.5)
    arrow(78.5, 19.5, 83.5, 24.5, color="#555555")
    arrow(78.5, 19.5, 83.5, 36.5, color="#555555")
    arrow(78.5, 19.5, 83.5, 12.5, color="#555555")

    ax.set_title("Unified Olympic SDE Evaluation Framework",
                 fontsize=14, fontweight="bold", pad=14)
    save(fig, "fig1_framework.png")


# ----------------------------------------------------------------------
# Figure 2 — Overall_7 ranking with decision zones
# ----------------------------------------------------------------------
def fig_ranking():
    order = np.argsort(O7)
    fig, ax = plt.subplots(figsize=(9.5, 8.2))
    y = np.arange(len(NAMES))
    colors = [DEC_COLOR[DECISION[i]] for i in order]
    ax.barh(y, O7[order], color=colors, height=0.68, zorder=3,
            edgecolor="white", linewidth=0.6)

    for yi, i in zip(y, order):
        ax.text(O7[i] + 0.008, yi, f"{O7[i]:.3f}", va="center",
                fontsize=8.6, color="#333333")

    ax.axvline(0.55, color="#444444", ls="--", lw=1.4, zorder=4)
    ax.axvline(0.42, color="#444444", ls="--", lw=1.4, zorder=4)
    ax.annotate("RETAIN threshold ≥ 0.55", xy=(0.55, 5.6),
                xytext=(0.575, 5.6), fontsize=8.8, color="#333333",
                va="center", zorder=5,
                arrowprops=dict(arrowstyle="-", color="#333333", lw=0.9))
    ax.annotate("REMOVE < 0.42", xy=(0.42, 2.5),
                xytext=(0.44, 2.5), fontsize=8.8, color="#333333",
                va="center", zorder=5,
                arrowprops=dict(arrowstyle="-", color="#333333", lw=0.9))

    ax.set_yticks(y)
    ax.set_yticklabels([NAMES[i] for i in order], fontsize=9.5)
    ax.set_xlabel("Overall$_7$ Score")
    ax.set_xlim(0, 0.95)
    ax.set_title("Final Ranking of 21 Candidate SDEs by Overall$_7$ Score")
    ax.grid(axis="x", color="#dddddd", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    handles = [Line2D([0], [0], marker="s", color="none", markerfacecolor=c,
                      markersize=11, label=l)
               for l, c in [("RETAIN (continuous sports)", C_RETAIN),
                            ("CONDITIONAL RETAIN (new sports)", C_COND),
                            ("REMOVE CANDIDATE (removed sports)", C_REMOVE)]]
    ax.legend(handles=handles, loc="lower right", frameon=True,
              framealpha=0.95, edgecolor="#cccccc", fontsize=9)
    save(fig, "fig2_ranking.png")


# ----------------------------------------------------------------------
# Figure 3 — Dimension-score heatmap
# ----------------------------------------------------------------------
def fig_heatmap():
    fig, ax = plt.subplots(figsize=(9.2, 9.5))
    im = ax.imshow(M, aspect="auto", cmap="YlGnBu", vmin=0, vmax=1)
    ax.set_xticks(range(6))
    ax.set_xticklabels(DIMS, fontsize=9.5, rotation=18, ha="right")
    ax.set_yticks(range(21))
    ax.set_yticklabels([f"{i+1}. {n}" for i, n in enumerate(NAMES)],
                       fontsize=9)
    for i in range(21):
        for j in range(6):
            v = M[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    fontsize=7.6,
                    color="white" if v > 0.62 else "#1a1a1a")
    ax.set_xticks(np.arange(-0.5, 6, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 21, 1), minor=True)
    ax.grid(which="minor", color="white", lw=1.4)
    ax.tick_params(which="minor", length=0)
    ax.set_title("Dimension Score Matrix (21 SDEs × 6 Criteria)", pad=12)
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label("Normalized score (0–1)", fontsize=9)
    cb.outline.set_visible(False)
    save(fig, "fig3_heatmap.png")


# ----------------------------------------------------------------------
# Figure 4 — Radar chart of representative SDEs
# ----------------------------------------------------------------------
def fig_radar():
    picks = [0, 13, 14, 20]  # Athletics, Weightlifting, Flag Football, Breaking
    labels = ["Athletics (retain)", "Weightlifting (retain)",
              "Flag Football (new)", "Breaking (removed)"]
    colors = ["#2C6E8F", "#3E7CB1", "#E2A03F", "#B84A44"]
    angles = np.linspace(0, 2 * np.pi, 6, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7.6, 7.2),
                           subplot_kw=dict(polar=True))
    for idx, lab, c in zip(picks, labels, colors):
        vals = M[idx].tolist() + M[idx][:1].tolist()
        ax.plot(angles, vals, color=c, lw=2.0, label=lab, zorder=3)
        ax.fill(angles, vals, color=c, alpha=0.10, zorder=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMS, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=8,
                       color="#777777")
    ax.grid(color="#cccccc", lw=0.8)
    ax.spines["polar"].set_color("#bbbbbb")
    ax.set_title("Criterion Profiles of Representative SDEs", pad=26)
    ax.legend(loc="upper right", bbox_to_anchor=(1.42, 1.12),
              frameon=True, edgecolor="#cccccc", fontsize=9)
    save(fig, "fig4_radar.png")


# ----------------------------------------------------------------------
# Figure 5 — Weight dashboard: AHP + entropy weights
# ----------------------------------------------------------------------
def fig_weights():
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4),
                             gridspec_kw={"width_ratios": [1.25, 1, 1]})

    # Panel A: AHP weights (Overall_7)
    ax = axes[0]
    labels = [a for a, _ in AHP7]
    vals = [b for _, b in AHP7]
    order = np.argsort(vals)
    cols = ["#8A6FA8" if "Continuity" not in labels[i] else "#6B4E8E"
            for i in order]
    ax.barh(np.arange(len(vals)), [vals[i] for i in order], color=cols,
            height=0.62, zorder=3)
    for k, i in enumerate(order):
        ax.text(vals[i] + 0.005, k, f"{vals[i]:.3f}", va="center",
                fontsize=8.6)
    ax.set_yticks(np.arange(len(vals)))
    ax.set_yticklabels([labels[i] for i in order], fontsize=8.8)
    ax.set_xlim(0, 0.36)
    ax.set_title("A  AHP Weights (Overall$_7$)", loc="left", fontsize=11)
    ax.grid(axis="x", color="#e2e2e2", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    # Panel B: entropy weights within dimensions
    ax = axes[1]
    all_ent = ENT_POP + [("—", np.nan)] + ENT_SAFE + [("—", np.nan)] + ENT_INNO
    ypos = np.arange(len(all_ent))
    colors = (["#2C6E8F"] * 5 + ["none"] + ["#3E9C84"] * 3 + ["none"]
              + ["#C77E4F"] * 2)
    for k, ((lab, v), c) in enumerate(zip(all_ent, colors)):
        if np.isnan(v):
            continue
        ax.barh(k, v, color=c, height=0.62, zorder=3)
        ax.text(v + 0.008, k, f"{v:.3f}", va="center", fontsize=8.2)
    ax.set_yticks(ypos)
    ax.set_yticklabels([lab for lab, _ in all_ent], fontsize=8.4)
    ax.invert_yaxis()
    ax.set_xlim(0, 0.95)
    ax.set_title("B  Entropy Weights by Dimension", loc="left", fontsize=11)
    ax.grid(axis="x", color="#e2e2e2", lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.text(0.86, 2.0, "Popularity", fontsize=8.5, color="#2C6E8F",
            fontweight="bold", va="center")
    ax.text(0.86, 7.0, "Safety", fontsize=8.5, color="#3E9C84",
            fontweight="bold", va="center")
    ax.text(0.86, 10.5, "Innovation", fontsize=8.5, color="#C77E4F",
            fontweight="bold", va="center")

    # Panel C: Overall_6 vs Overall_7 weights comparison
    ax = axes[2]
    dims6 = ["Pop.", "Incl.", "Safety", "Sust.", "Innov.", "Gender"]
    w7_no_cont = [0.273341, 0.092063, 0.156795, 0.092063, 0.049191,
                  0.049191]
    x = np.arange(6)
    ax.bar(x - 0.19, W6, width=0.38, color="#4C5B6B",
           label="Overall$_6$", zorder=3)
    ax.bar(x + 0.19, w7_no_cont, width=0.38, color="#8A6FA8",
           label="Overall$_7$ (excl. continuity)", zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(dims6, fontsize=8.6)
    ax.set_title("C  Weight Shift After Policy Tuning", loc="left",
                 fontsize=11)
    ax.legend(fontsize=8.2, frameon=True, edgecolor="#cccccc")
    ax.grid(axis="y", color="#e2e2e2", lw=0.7, zorder=0)
    ax.set_axisbelow(True)

    fig.suptitle("Weight Structure of the Evaluation Model",
                 fontsize=13, fontweight="bold", y=1.02)
    fig.tight_layout()
    save(fig, "fig5_weights.png")


# ----------------------------------------------------------------------
# Figure 6 — Overall_6 vs Overall_7 validation scatter
# ----------------------------------------------------------------------
def fig_scatter():
    fig, ax = plt.subplots(figsize=(8.6, 6.4))
    gcolor = {"continuous": C_RETAIN, "new": C_COND, "removed": C_REMOVE}
    gmark = {"continuous": "o", "new": "s", "removed": "D"}
    for g in ["continuous", "new", "removed"]:
        idx = [i for i in range(21) if GROUP[i] == g]
        ax.scatter(O6[idx], O7[idx], s=95, c=gcolor[g], marker=gmark[g],
                   edgecolor="white", linewidth=1.0, zorder=3,
                   label={"continuous": "Continuous (14)",
                          "new": "New (4)", "removed": "Removed (3)"}[g])
    offsets = {
        "Athletics": (7, 5, "left"),
        "Swimming": (7, 5, "left"),
        "Football": (-6, 9, "right"),
        "Basketball": (8, -3, "left"),
        "Tennis": (-2, -13, "right"),
        "Cycling Track": (7, 6, "left"),
        "Badminton": (3, -14, "left"),
        "Judo": (6, 9, "left"),
        "Shooting": (9, -3, "left"),
        "Fencing": (-4, -14, "right"),
        "Field Hockey": (-8, -22, "right"),
        "Diving": (9, -4, "left"),
        "Modern Pentathlon": (-6, -14, "right"),
        "Weightlifting": (7, 5, "left"),
        "Flag Football": (7, 5, "left"),
        "Cricket T20": (6, 8, "left"),
        "Lacrosse Sixes": (3, -14, "left"),
        "Squash": (7, 5, "left"),
        "Boxing": (7, 5, "left"),
        "Karate": (-6, -13, "right"),
        "Breaking": (7, 5, "left"),
    }
    for i in range(21):
        dx, dy, ha = offsets[NAMES[i]]
        ax.annotate(NAMES[i], (O6[i], O7[i]),
                    textcoords="offset points", xytext=(dx, dy),
                    ha=ha, fontsize=7.4, color="#555555")

    lim = (0.25, 0.92)
    ax.plot(lim, lim, ls=":", color="#999999", lw=1.2, zorder=1)
    ax.text(0.30, 0.285, "Overall$_7$ = Overall$_6$", fontsize=8.5,
            color="#888888", rotation=24)

    ax.axhline(0.55, color="#444444", ls="--", lw=1.1)
    ax.axhline(0.42, color="#444444", ls="--", lw=1.1)
    ax.text(0.255, 0.558, "RETAIN ≥ 0.55", fontsize=8.2, color="#333333")
    ax.text(0.255, 0.428, "REMOVE < 0.42", fontsize=8.2, color="#333333")

    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("Overall$_6$ (no continuity prior)")
    ax.set_ylabel("Overall$_7$ (final score)")
    ax.set_title("Effect of the Programme-Continuity Factor and\n"
                 "Validation Against IOC Reality Grouping")
    ax.grid(color="#e6e6e6", lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", frameon=True, edgecolor="#cccccc",
              fontsize=9)
    save(fig, "fig6_validation.png")


if __name__ == "__main__":
    fig_framework()
    fig_ranking()
    fig_heatmap()
    fig_radar()
    fig_weights()
    fig_scatter()
    print("All figures generated in", OUT)
