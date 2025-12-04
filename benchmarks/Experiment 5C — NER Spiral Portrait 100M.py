import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 100_000_000      # 100 million iterations
SAMPLE_EVERY = 500       # only plot every 500th point
COLOR = "#00ff00"        # bright neon green
today = datetime.now().strftime("%b %d %Y")

# -------------------------------------------------------------
# WDTP + NER recurrence
# -------------------------------------------------------------
a = 1.0
xs = []
ys = []

print(f"Running WDTP + NER up to n = {MAX_N:,} (plotting every {SAMPLE_EVERY}th point)")

for n in range(1, MAX_N + 1):
    # Numerical Evaluation Rule: phase reduced mod 2π
    phase = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase)) + 1

    # Subsample for plotting so we don't blow memory
    if n % SAMPLE_EVERY == 0:
        xs.append(n)
        ys.append(a)

# -------------------------------------------------------------
# PLOT: 100M NER TRIANGLE
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

ax.set_facecolor("black")
ax.scatter(xs, ys, s=0.8, c=COLOR, alpha=0.45)
ax.axis("off")

fig.suptitle(
    f"HashHelix π/n Spiral — WDTP + NER — {MAX_N:,} records (subsampled) — {today}",
    fontsize=16,
    color="white",
    y=0.96
)

fig.text(
    0.5,
    0.92,
    "NER: phase = (a(n−1) + π/n) mod 2π  →  drift-free expansion out to 100M steps",
    ha="center",
    color="white",
    fontsize=10
)

fig.text(
    0.5,
    0.03,
    f"Plotted ~{MAX_N // SAMPLE_EVERY:,} points (every {SAMPLE_EVERY}th step) for a stable high-N portrait.",
    ha="center",
    color="white",
    fontsize=9
)

plt.tight_layout(rect=[0.02, 0.06, 0.98, 0.90])

fig.savefig(
    "spiral_ner_100M.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black"
)

print("Done. Saved image as spiral_ner_100M.png")
