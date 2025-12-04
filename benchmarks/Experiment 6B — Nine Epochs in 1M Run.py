import math
import random
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------------------------------------
# PARAMETERS
# -------------------------------------------------------------
MAX_N = 1_000_000

BACKGROUND_SUBSAMPLE = 10    # keep every 10th point for the full lane
EPOCH_COUNT = 9
EPOCH_WIDTH = 2_000          # steps per epoch window

COLOR_ALL = "#00aa00"        # faint green background

today = datetime.now().strftime("%b %d %Y")

# Reproducible random epoch centers
random.seed(42)
margin = EPOCH_WIDTH  # keep epochs away from extreme edges
epoch_centers = sorted(random.sample(
    range(margin, MAX_N - margin),
    EPOCH_COUNT
))

epochs = []
for center in epoch_centers:
    start = center - EPOCH_WIDTH // 2
    end = center + EPOCH_WIDTH // 2
    epochs.append({
        "center": center,
        "start": start,
        "end": end,
        "xs": [],
        "ys": [],
    })

# Some distinct colors for epochs (will cycle if needed)
epoch_colors = [
    "#ff00ff", "#00ffff", "#ffff00",
    "#ff8800", "#00ff88", "#ff4444",
    "#4488ff", "#bb33ff", "#33ffbb",
]

# -------------------------------------------------------------
# RUN WDTP + NER TO 1,000,000
# -------------------------------------------------------------
a = 1.0
xs_all = []
ys_all = []

for n in range(1, MAX_N + 1):
    phase = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase)) + 1

    # Background subsample
    if n % BACKGROUND_SUBSAMPLE == 0:
        xs_all.append(n)
        ys_all.append(a)

    # Check each epoch window
    for e in epochs:
        if e["start"] <= n <= e["end"]:
            e["xs"].append(n)
            e["ys"].append(a)

# -------------------------------------------------------------
# PLOT
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
ax.set_facecolor("black")

# Full lane (subsampled)
ax.scatter(xs_all, ys_all, s=0.3, c=COLOR_ALL, alpha=0.35)

# Epoch overlays
for idx, e in enumerate(epochs):
    color = epoch_colors[idx % len(epoch_colors)]
    ax.scatter(e["xs"], e["ys"], s=4.0, c=color, alpha=0.9)

ax.axis("off")

centers_str = ", ".join(f"{c:,}" for c in epoch_centers)

fig.suptitle(
    f"HashHelix π/n Spiral — WDTP+NER — 1,000,000 steps with 9 random epochs highlighted",
    fontsize=18,
    color="white",
    y=0.95,
)

fig.text(
    0.5,
    0.91,
    f"Epoch windows (width {EPOCH_WIDTH:,}) centered at n = {centers_str}. "
    "Background lane subsampled every 10 steps.",
    ha="center",
    fontsize=9,
    color="white",
)

fig.savefig(
    "spiral_ner_9epochs_in_1M.png",
    bbox_inches="tight",
    pad_inches=0.2,
    facecolor="black",
)

print("Saved spiral_ner_9epochs_in_1M.png")
