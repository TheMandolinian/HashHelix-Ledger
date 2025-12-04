import math
import matplotlib.pyplot as plt
from datetime import datetime

MAX_N = 10
COLOR = "#00ff00"
today = datetime.now().strftime("%b %d %Y")

a = 1.0
xs = []
ys = []

for n in range(1, MAX_N + 1):
    phase = (a + math.pi / n) % (2.0 * math.pi)
    a = math.floor(n * math.sin(phase)) + 1
    xs.append(n)
    ys.append(a)

fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
ax.set_facecolor("black")
ax.scatter(xs, ys, s=80, c=COLOR)
ax.axis("off")

fig.suptitle(
    f"HashHelix π/n Spiral — WDTP + NER — {MAX_N} records — {today}",
    fontsize=18, color="white", y=0.94
)

fig.text(
    0.5, 0.89,
    "First 10 steps: WDTP + NER forming the initial expansion seed.",
    ha="center", color="white", fontsize=10
)

fig.savefig("spiral_ner_10.png", bbox_inches="tight", pad_inches=0.2, facecolor="black")
print("Saved spiral_ner_10.png")

