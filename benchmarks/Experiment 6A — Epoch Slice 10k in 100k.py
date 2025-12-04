import math
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 100_000

# Epoch slice around n = 10,000
EPOCH_CENTER = 10_000
EPOCH_WIDTH  = 1_000          # 1,000-step window
EPOCH_START  = EPOCH_CENTER - EPOCH_WIDTH // 2
EPOCH_END    = EPOCH_CENTER + EPOCH_WIDTH // 2

COLOR_ALL   = "#00aa00"       # faint green for full run
COLOR_EPOCH = "#ff00ff"       # magenta for highlighted epoch

today = datetime.now().strftime("%b %d %Y")

# -------------------------------------------------------------
# RUN WDTP + NER ONCE TO 100,000
# -------------------------------------------------------------
a = 1.0
xs_all = []
ys_all = []

xs_epoch = []
ys_epoch = []

for n in range(1, MAX_N + 1):
    phase = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase)) + 1

    xs_all.append(n)
    ys_all.append(a)

    if EPOCH_START <= n <= EPOCH_END:
        xs_epoch.append(n)
        ys_epoch.append(a)

# -------------------------------------------------------------
# PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_facecolor("black")

# Full 100k run (faint background)
ax.scatter(xs_all, ys_all, s=0.4, c=COLOR_ALL, alpha=0.4)

# Epoch window around n = 10,000 (bright overlay)
ax.scatter(xs_epoch, ys_epoch, s=4.0, c=COLOR_EPOCH, alpha=0.9)

ax.axis("off")

fig.suptitle(
    f"HashHelix π/n Spiral — WDTP+NER — 100,000 steps with 10k Epoch Highlight",
    fontsize=18,
    color="white",
    y=0.95,
)

fig.text(
    0.5,
    0.91,
    f"Full lane: 1..{MAX_N:,} steps (green). Epoch slice: n={EPOCH_START:,}..{EPOCH_END:,} (magenta) around 10k.",
    ha="center",
    fontsize=10,
    color="white",
)

fig.savefig(
    "spiral_ner_epoch_10k_in_100k.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black",
)

print("Saved spiral_ner_epoch_10k_in_100k.png")
