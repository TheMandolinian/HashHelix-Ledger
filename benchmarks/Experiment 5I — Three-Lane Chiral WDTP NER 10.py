import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 10
COLOR = "#00ff00"
today = datetime.now().strftime("%b %d %Y")

# -------------------------------------------------------------
# TRUE 3-LANE WDTP+NER (no mirroring)
# Lane A: a1 = 1  → right side
# Lane B: a1 = 2  → left side
# Lane C: a1 = 3  → center (x = 0)
# -------------------------------------------------------------
a = 1.0   # Lane A state
b = 2.0   # Lane B state
c = 3.0   # Lane C state

xs_A, ys_A = [], []
xs_B, ys_B = [], []
xs_C, ys_C = [], []

for n in range(1, MAX_N + 1):
    # Lane A (right)
    phase_a = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase_a)) + 1
    xs_A.append(n)
    ys_A.append(a)

    # Lane B (left)
    phase_b = (b + math.pi / n) % (2.0 * math.pi)
    b = math.floor(n * math.sin(phase_b)) + 1
    xs_B.append(-n)
    ys_B.append(b)

    # Lane C (center)
    phase_c = (c + math.pi / n) % (2.0 * math.pi)
    c = math.floor(n * math.sin(phase_c)) + 1
    xs_C.append(0)    # vertical column at x = 0
    ys_C.append(c)

# -------------------------------------------------------------
# PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
ax.set_facecolor("black")

ax.scatter(xs_A, ys_A, s=80, c=COLOR)  # right
ax.scatter(xs_B, ys_B, s=80, c=COLOR)  # left
ax.scatter(xs_C, ys_C, s=80, c=COLOR)  # center

ax.axis("off")

fig.suptitle(
    f"HashHelix π/n Spiral — True 3-Lane Chirality (WDTP+NER) — {MAX_N} steps — {today}",
    fontsize=18, color="white", y=0.94
)

fig.text(
    0.5, 0.89,
    "Lane A (a₁=1) → right   |   Lane B (a₁=2) → left   |   Lane C (a₁=3) → center. All independent, no mirroring.",
    ha="center", fontsize=10, color="white"
)

fig.savefig(
    "spiral_ner_3lane_10.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black"
)

print("Saved spiral_ner_3lane_10.png")
