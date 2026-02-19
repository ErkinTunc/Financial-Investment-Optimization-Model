from pathlib import Path

from utils import (
    lecture_donnees,
    index_placements_by_end_time,
    optimiz_coef_indexed,
    reconstruct_path,
)


def main():
    # === Step 1: Load data from Excel ===
    project_root = Path(__file__).resolve().parents[1]  # .../src -> project root
    file_path = project_root / 'data-folder' / 'data-exemple' / 'exemple.xlsx' # or: data-folder/Données_groupe_13.xlsx

    n, tau0, placements = lecture_donnees(file_path)
    ending_at = index_placements_by_end_time(n, placements)

    # === Step 2: Pre-index products by end time (O(m)) ===
    ending_at = index_placements_by_end_time(n, placements)

    # === Step 3: Initialize coefficient and predecessor arrays ===
    coef = [0.0] * (n + 1)
    prev = [None] * (n + 1)

    coef[0] = 1.0
    if n >= 1:
        coef[1] = coef[0] * (1.0 + tau0)
        prev[1] = 0

    # === Step 4: Dynamic programming (O(n+m)) ===
    for t in range(2, n + 1):
        coef[t] = optimiz_coef_indexed(t, coef, tau0, ending_at, prev)

    # === Step 5: Reconstruct optimal path ===
    path = reconstruct_path(prev, n)

    # === Step 6: Display results ===
    print("\nOptimal capital coefficients:")
    for t in range(n + 1):
        print(f"Coef({t}) = {coef[t]:.5f}")

    print("\nOptimal path (from -> to):")
    for step_from, step_to in path:
        print(f"{step_from} -> {step_to}")

    print(f"\nFinal capital coefficient: {coef[n]:.5f}")


if __name__ == "__main__":
    main()
