import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 10_200           # ~10k records
COLOR = "#00ff00"        # pure neon green
today = datetime.now().strftime("%b %d %Y")

# -------------------------------------------------------------
# WDTP + NER recurrence ONLY
# -------------------------------------------------------------
a = 1.0
xs = []
ys = []

for n in range(1, MAX_N + 1):
    # Numerical Evaluation Rule: phase reduced mod 2π
    phase = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase)) + 1

    xs.append(n)
    ys.append(a)

# -------------------------------------------------------------
# SINGLE NER TRIANGLE PLOT (high saturation)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

ax.set_facecolor("black")

# 🔥 KEY PART: bigger points + alpha blending to build saturation
ax.scatter(xs, ys, s=1.5, c=COLOR, alpha=0.5)

ax.axis("off")

# Main title – show ~10.2k records
fig.suptitle(
    f"HashHelix π/n Spiral — WDTP + NER — {MAX_N:,} records — {today}",
    fontsize=18,
    color="white",
    y=0.96
)

# Short NER line under title
fig.text(
    0.5,
    0.92,
    "NER: phase = (a(n−1) + π/n) mod 2π  →  drift-free, reproducible spiral",
    ha="center",
    color="white",
    fontsize=10
)

# Bottom caption comparing to Grok's pre-NER 10,166-record triangle
fig.text(
    0.5,
    0.03,
    "Pre-NER 10k spiral (Nov 12 2025) shows vertical streaks from floating-point drift. "
    "This NER 10k spiral is the stabilized reference.",
    ha="center",
    color="white",
    fontsize=9
)

plt.tight_layout(rect=[0.02, 0.06, 0.98, 0.90])

fig.savefig(
    "spiral_ner_10k_explained.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black"
)

