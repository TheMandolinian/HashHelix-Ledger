import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 10
LANES = 21
COLOR = "#00ff00"
today = datetime.now().strftime("%b %d %Y")

# x positions for 21 lanes: -10 .. 0 .. +10
x_positions = list(range(-LANES // 2, LANES // 2 + 1))

# -------------------------------------------------------------
# INITIAL STATES FOR EACH LANE
# Lane k starts with a1 = k+1 (so they are all distinct)
# -------------------------------------------------------------
states = [float(k + 1) for k in range(LANES)]

xs = []
ys = []

for n in range(1, MAX_N + 1):
    for idx in range(LANES):
        a = states[idx]
        phase = (a + math.pi / n) % (2.0 * math.pi)   # NER
        a = math.floor(n * math.sin(phase)) + 1
        states[idx] = a

        xs.append(x_positions[idx])
        ys.append(a)

# -------------------------------------------------------------
# PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor("black")

ax.scatter(xs, ys, s=60, c=COLOR)
ax.axis("off")

fig.suptitle(
    f"HashHelix π/n Spiral — True 21-Lane Chirality (WDTP+NER) — {MAX_N} steps — {today}",
    fontsize=18,
    color="white",
    y=0.94,
)

fig.text(
    0.5,
    0.89,
    "21 independent lanes seeded with a₁ = 1..21, spaced from x = −10..+10. All lanes computed, no mirroring.",
    ha="center",
    fontsize=10,
    color="white",
)

fig.savefig(
    "spiral_ner_21lane_10.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black",
)

print("Saved spiral_ner_21lane_10.png")
