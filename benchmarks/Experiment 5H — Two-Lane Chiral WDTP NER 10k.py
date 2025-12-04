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
# TRUE 2-LANE WDTP + NER (no mirroring)
# Lane A: a1 = 1  → plotted on +x side
# Lane B: a1 = 2  → plotted on -x side
# -------------------------------------------------------------
a = 1.0   # Lane A state
b = 2.0   # Lane B state

xs_A, ys_A = [], []
xs_B, ys_B = [], []

for n in range(1, MAX_N + 1):
    # Lane A
    phase_a = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase_a)) + 1
    xs_A.append(n)
    ys_A.append(a)

    # Lane B
    phase_b = (b + math.pi / n) % (2.0 * math.pi)
    b = math.floor(n * math.sin(phase_b)) + 1
    xs_B.append(-n)   # negative x for left-hand lane
    ys_B.append(b)

# -------------------------------------------------------------
# PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor("black")

# Lane A (right)
ax.scatter(xs_A, ys_A, s=1.5, c=COLOR, alpha=0.9)

# Lane B (left)
ax.scatter(xs_B, ys_B, s=1.5, c=COLOR, alpha=0.9)

ax.axis("off")

fig.suptitle(
    f"HashHelix π/n Spiral — True 2-Lane Chirality (WDTP + NER) — {MAX_N:,} steps — {today}",
    fontsize=18, color="white", y=0.95
)

fig.text(
    0.5, 0.91,
    "Lane A (a₁=1) → right wedge   |   Lane B (a₁=2) → left wedge. Both lanes computed independently; no mirroring.",
    ha="center", color="white", fontsize=10
)

plt.tight_layout()
fig.savefig(
    "spiral_ner_2lane_10k.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black"
)

print("Saved spiral_ner_2lane_10k.png")
