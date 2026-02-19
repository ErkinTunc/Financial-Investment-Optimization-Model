# Optimal Investment Strategy via DAG Dynamic Programming

This problem arises in discrete-time capital allocation under interval-constrained investment options.  
Each investment decision corresponds to a transition in time, forming a directed acyclic decision graph.  
The objective is to compute the globally optimal policy without enumerating exponentially many strategies.

## One-line

Deterministic investment optimization reduced to a maximum-multiplicative path problem on a time-indexed DAG, solved by dynamic programming with path reconstruction in **O(n + m)** after indexing products by end time.

## Problem

We consider a discrete time horizon **T = {0, …, n}**. An investor starts with capital **C₀** and may choose:

- **Base placement** on each interval **[t, t+1]** with constant rate **τ₀**
- **Specific products** **Pₖ = (dₖ, fₖ, τₖ)** available only on **[dₖ, fₖ]** (usable at most once)

Goal: maximize the final capital multiplier at time **n**.

## Graph reduction

Construct a **Directed Acyclic Graph (DAG)** **D = (V, A)**:

- **V = {0, 1, …, n}** (time points)
- **A** contains:
  - base arcs **(t, t+1)** with weight **c(t, t+1) = 1 + τ₀**
  - product arcs **(dₖ, fₖ)** with weight **c(dₖ, fₖ) = 1 + τₖ**

Any path **P : 0 → n** encodes a feasible investment policy, with multiplicative gain:

- **C(P) = ∏ c(a)** for arcs **a ∈ P**

We want:

- **P\* = argmax C(P)**

The graph is acyclic (time strictly increases), so optimal values can be computed in topological order (**0 → n**).

## Dynamic programming

Define:

- **Coef(t)** = maximum achievable capital multiplier at time **t**  
  with **Coef(0) = 1**.

For **t ≥ 1**:

- **Coef(t) = max( Coef(t−1)(1+τ₀), max\_{k: fₖ=t} Coef(dₖ)(1+τₖ) )**

### Path reconstruction

Maintain a predecessor array **prev[t]** storing the time index that achieved the max for **Coef(t)**.  
Backtrack from **t = n** to **0** to recover the optimal policy.

## Correctness sketch

Optimal substructure on a DAG:

- Any optimal path to **t** ends either with a base arc **(t−1 → t)** or a product arc **(dₖ → t)** for some **k** with **fₖ = t**.
- The prefix to **t−1** (or **dₖ**) must be optimal, otherwise replacing it yields a better path to **t** (contradiction).

Acyclicity ensures all subproblems needed for **Coef(t)** are solved before **t**.

## Complexity

Let **n** be the horizon length and **m** the number of products.

- **Indexing step:** group products by end time **fₖ** in **O(m)**
- **DP pass:** for each **t**, only scan products ending at **t** (total **O(m)** across all t)

Overall:

- **Time:** **O(n + m)**
- **Space:** **O(n + m)** (including indexed buckets)

## Additive equivalent

Since all arc weights are positive:

- maximize **∏ c(a)** ⇔ maximize **∑ log(c(a))**

This becomes a longest-path problem on a DAG in log-space; the DP above is the natural solution.

## Implementation

- `main.py`: reads an Excel instance, builds indexed buckets, runs DP, prints Coef(t), the optimal path, and Coef(n)
- `utils.py`:
  - `lecture_donnees`: Excel → (n, τ0, placements)
  - `index_placements_by_end_time`: placements → buckets by f_k
  - `optimiz_coef_indexed`: computes Coef(t) using only products ending at t, stores predecessor
  - `reconstruct_path`: backtracks `prev[]` to output the policy

## Input format (Excel)

Interpreted as:

- Row 1, Col 1: **n**
- Row 2, Col 1: **τ₀** (percent)
- Rows 3+: **(τₖ, dₖ, fₖ)** where **τₖ** is percent

---

## Run

#### Windows

```bash
py -m pip install openpyxl
py src\main.py
```

#### macOS / Linux

```bash
python3 -m pip install openpyxl
python3 src/main.py
```

---

## What this project demonstrates

- Reduction of an applied optimization problem to a clean **DAG** model
- Dynamic programming derivation (recurrence + invariants)
- Proof-aware reasoning (optimal substructure, acyclicity)
- Tight complexity bounds (**O(n+m)** with indexing)
- Recovering both the optimum value and the **optimal policy** (path reconstruction)
