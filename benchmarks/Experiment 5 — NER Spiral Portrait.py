import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 150_000          # same ballpark as Grok's pre-NER triangle
COLOR = "#39ff14"        # neon green
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
# SINGLE NER TRIANGLE PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

ax.set_facecolor("black")
ax.scatter(xs, ys, s=0.1, c=COLOR)
ax.axis("off")

# Main title – matches Grok style, but clearly says NER
fig.suptitle(
    f"HashHelix π/n Spiral — WDTP + NER — {MAX_N:,} records — {today}",
    fontsize=18,
    color="white",
    y=0.96
)

# Short NER line just under the title
fig.text(
    0.5,
    0.92,
    "NER: phase = (a(n−1) + π/n) mod 2π  →  drift-free, reproducible spiral",
    ha="center",
    color="white",
    fontsize=10
)

# Bottom caption explaining why Grok's older triangle looks different
fig.text(
    0.5,
    0.03,
    "Pre-NER spiral (Nov 12 2025) accumulates floating-point drift, causing vertical streaks and artifacts. "
    "NER version removes that drift, yielding a clean, uniform interior.",
    ha="center",
    color="white",
    fontsize=9
)

plt.tight_layout(rect=[0.02, 0.06, 0.98, 0.90])

fig.savefig(
    "spiral_ner_explained.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black"
)

