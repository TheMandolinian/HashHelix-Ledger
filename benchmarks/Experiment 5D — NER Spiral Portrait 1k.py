import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 1_000
COLOR = "#00ff00"
today = datetime.now().strftime("%b %d %Y")

# -------------------------------------------------------------
# WDTP + NER recurrence
# -------------------------------------------------------------
a = 1.0
xs = []
ys = []

for n in range(1, MAX_N + 1):
    # Numerical Evaluation Rule (NER)
    phase = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase)) + 1

    xs.append(n)
    ys.append(a)

# -------------------------------------------------------------
# PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

ax.set_facecolor("black")
ax.scatter(xs, ys, s=5, c=COLOR)  # bigger dots for 1k
ax.axis("off")

fig.suptitle(
    f"HashHelix π/n Spiral — WDTP + NER — {MAX_N:,} records — {today}",
    fontsize=18, color="white", y=0.94
)

fig.text(
    0.5,
    0.89,
    "NER: phase = (a(n−1) + π/n) mod 2π  →  drift-free early-stage spiral",
    ha="center",
    color="white",
    fontsize=10
)

fig.text(
    0.5,
    0.03,
    "This 1k NER spiral shows the early expansion before the wedge saturates.",
    ha="center",
    color="white",
    fontsize=9
)

plt.tight_layout(rect=[0.02, 0.06, 0.98, 0.88])

fig.savefig(
    "spiral_ner_1k.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black"
)

print("Saved spiral_ner_1k.png")

