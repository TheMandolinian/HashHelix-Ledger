# generate_lane01.py
# HashHelix Entropy Dataset — Lane 01
# Generates 2,000,000-step recurrence sequence
# a₁ = 1, aₙ = floor(n * sin(aₙ₋₁ + π/n)) + 1

import math

N = 2_000_000
OUT = "hh_entropy_lane01.txt"

def generate():
    with open(OUT, "w") as f:
        a = 1.0
        f.write("1\n")
        for n in range(2, N + 1):
            a = math.floor(n * math.sin(a + math.pi / n)) + 1
            f.write(f"{int(a)}\n")

    print(f"[Lane 01] Generated {N:,} steps → {OUT}")

if __name__ == "__main__":
    generate()
