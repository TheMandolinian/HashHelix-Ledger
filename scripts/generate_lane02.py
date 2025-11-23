# generate_lane02.py
# HashHelix Entropy Dataset — Lane 02
# Generates 2,000,000-step recurrence sequence
# a₁ = 1, aₙ = floor(n * sin(aₙ₋₁ + π/n)) + 1

from core.wdtp import wdtp_next

N = 2_000_000
OUT = "hh_entropy_lane02.txt"

def generate():
    with open(OUT, "w") as f:
        a = 2.0     # 🚨 Lane 02 starts at a₁ = 2 (different seed)
        f.write("2\n")
        for n in range(2, N + 1):
            a = wdtp_next(a, n)
            f.write(f"{int(a)}\n")

    print(f"[Lane 02] Generated {N:,} steps → {OUT}")

if __name__ == "__main__":
    generate()
