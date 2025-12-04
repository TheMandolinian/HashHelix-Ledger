import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 10_000
COLOR = "#00ff00"
today = datetime.now().strftime("%b %d %Y")

# -------------------------------------------------------------
# WDTP + NER (positive side only — true recurrence)
# -------------------------------------------------------------
a = 1.0
xs_pos = []
ys_pos = []

for n in range(1, MAX_N + 1):
    # Numerical Evaluation Rule
    phase = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase)) + 1

    xs_pos.append(n)
    ys_pos.append(a)

# -------------------------------------------------------------
# MIRROR (negative side)
# -------------------------------------------------------------
xs_neg = [-x for x in xs_pos]
ys_neg = ys_pos[:]   # same values

# -------------------------------------------------------------
# PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor("black")

ax.scatter(xs_pos, ys_pos, s=1.5, c=COLOR, alpha=0.9)
ax.scatter(xs_neg, ys_neg, s=1.5, c=COLOR, alpha=0.9)

ax.axis("off")

# Title
fig.suptitle(
    f"HashHelix π/n Spiral — Symmetric WDTP + NER — −{MAX_N:,} to +{MAX_N:,} — {today}",
    fontsize=18, color="white", y=0.95
)

# Explanation
fig.text(
    0.5, 0.91,
    "Negative region is a mirrored visualization — WDTP+NER is defined only for n > 0.",
    ha="center", color="white", fontsize=10
)

plt.tight_layout()
fig.savefig(
    "spiral_ner_symmetric_20k.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black"
)

print("Saved spiral_ner_symmetric_20k.png")
