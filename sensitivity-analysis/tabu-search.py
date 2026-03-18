# %% [markdown]
# # Employee Scheduling with Tabu Search
#
# ## Problem Description
#
# We need to schedule **N nurses** over **D days**, with multiple **shifts per day**.
# The constraints are:
# - Every shift every day must be covered by exactly one nurse.
# - Each nurse works at most one shift per day.
# - Each nurse works a minimum and maximum number of shifts per scheduling period.
#
# We use the classic example from Google OR-Tools:
# - **4 Nurses**, **3 Days**, **3 Shifts** (0=Morning, 1=Afternoon, 2=Night)
#
# ---
# ## What is Tabu Search?
#
# Tabu Search is a **metaheuristic** optimization algorithm that:
# 1. Starts from an initial (possibly infeasible) solution.
# 2. Explores **neighbors** of the current solution.
# 3. Moves to the **best neighbor**, even if it's worse than the current (avoids local optima).
# 4. Keeps a **Tabu List** — a memory of recently visited moves — to prevent cycling.
# 5. Uses **aspiration criteria** to override the tabu list if a move leads to a global best.
# 6. Repeats until a stopping criterion (max iterations or no improvement).

# %% [markdown]
# ## Step 1: Init random seed

# %%
import numpy as np
import random
import copy
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import product

random.seed(42)
np.random.seed(42)

# %% [markdown]
# ## Step 2: Define the Problem Parameters

# %%
NUM_NURSES = 4
NUM_DAYS   = 3
NUM_SHIFTS = 3   # 0=Morning, 1=Afternoon, 2=Night

SHIFT_NAMES  = ["Morning", "Afternoon", "Night"]
NURSE_NAMES  = [f"Nurse {i}" for i in range(NUM_NURSES)]

# Constraints
MIN_SHIFTS_PER_NURSE = (NUM_SHIFTS * NUM_DAYS) // NUM_NURSES   # each nurse works at least this many shifts
MAX_SHIFTS_PER_NURSE = 5   # each nurse works at most this many shifts
if NUM_SHIFTS * NUM_DAYS % NUM_NURSES == 0:
    MAX_SHIFTS_PER_NURSE = MIN_SHIFTS_PER_NURSE
else:
    MAX_SHIFTS_PER_NURSE = MIN_SHIFTS_PER_NURSE + 1


# Penalty weights (used to turn hard constraints into a penalized objective)
PENALTY_UNCOVERED_SHIFT   = 100   # a shift not covered by exactly 1 nurse
PENALTY_DOUBLE_SHIFT      = 50    # nurse assigned more than 1 shift/day
PENALTY_MIN_SHIFTS        = 10    # nurse works fewer than MIN_SHIFTS
PENALTY_MAX_SHIFTS        = 10    # nurse works more than MAX_SHIFTS

print(f"Problem: {NUM_NURSES} nurses, {NUM_DAYS} days, {NUM_SHIFTS} shifts/day")
print(f"Total shift slots: {NUM_DAYS * NUM_SHIFTS}")
print(f"Each nurse should work between {MIN_SHIFTS_PER_NURSE} and {MAX_SHIFTS_PER_NURSE} shifts")

# %% [markdown]
# ## Step 3: Solution Representation
#
# `schedule[nurse][day][shift] = 1` means that nurse is assigned to that shift.

# %%
def create_random_solution():
    """
    Create a random feasible-ish solution by assigning exactly one nurse
    to each (day, shift) slot.
    """
    schedule = np.zeros((NUM_NURSES, NUM_DAYS, NUM_SHIFTS), dtype=int)
    for d in range(NUM_DAYS):
        for s in range(NUM_SHIFTS):
            nurse = random.randint(0, NUM_NURSES - 1)
            schedule[nurse][d][s] = 1
    return schedule

def print_schedule(schedule, title="Schedule"):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    header = f"{'Nurse':<12}" + "".join(
        f"Day{d}-{SHIFT_NAMES[s][0]:<5}" for d in range(NUM_DAYS) for s in range(NUM_SHIFTS)
    )
    print(header)
    print("-" * len(header))
    for n in range(NUM_NURSES):
        row = f"{NURSE_NAMES[n]:<12}"
        for d in range(NUM_DAYS):
            for s in range(NUM_SHIFTS):
                row += f"{'✓':<10}" if schedule[n][d][s] == 1 else f"{'.':<10}"
        shifts_worked = schedule[n].sum()
        row += f"| Total: {shifts_worked}"
        print(row)

sol = create_random_solution()
print_schedule(sol, "Example Random Solution")

# %% [markdown]
# ## Step 4: Define the Objective / Cost Function
#
# Since this is a constraint satisfaction problem, we convert all constraints
# to **penalty terms**. The goal is to minimize total penalty

# %%
def cost(schedule):
    """
    Compute total penalty of a schedule.
    Lower is better. Zero = fully feasible solution.
    """
    penalty = 0

    # Constraint 1: Every (day, shift) must be covered by exactly 1 nurse
    for d in range(NUM_DAYS):
        for s in range(NUM_SHIFTS):
            coverage = sum(schedule[n][d][s] for n in range(NUM_NURSES))
            if coverage != 1:
                penalty += PENALTY_UNCOVERED_SHIFT * abs(coverage - 1)

    # Constraint 2: Each nurse works at most 1 shift per day
    for n in range(NUM_NURSES):
        for d in range(NUM_DAYS):
            daily_shifts = sum(schedule[n][d][s] for s in range(NUM_SHIFTS))
            if daily_shifts > 1:
                penalty += PENALTY_DOUBLE_SHIFT * (daily_shifts - 1)

    # Constraint 3: Min/Max shifts per nurse over the period
    for n in range(NUM_NURSES):
        total = schedule[n].sum()
        if total < MIN_SHIFTS_PER_NURSE:
            penalty += PENALTY_MIN_SHIFTS * (MIN_SHIFTS_PER_NURSE - total)
        if total > MAX_SHIFTS_PER_NURSE:
            penalty += PENALTY_MAX_SHIFTS * (total - MAX_SHIFTS_PER_NURSE)

    return penalty

print(f"Cost of random solution: {cost(sol)}")

# %% [markdown]
# ## Step 5: Define the Neighborhood (Move Operators)
#
# Here we demonstrate only 1 strategy to generate **neighbor**:
# - **Reassign**: Reassign a (day, shift) slot from one nurse to another.

# %%
def get_neighbors(schedule):
    """
    Generate all neighbors via 'reassign' moves:
    For each (day, shift), try assigning it to each possible nurse.
    Returns list of (new_schedule, move_description).
    A move is described as (nurse_from, nurse_to, day, shift).
    """
    neighbors = []
    for d in range(NUM_DAYS):
        for s in range(NUM_SHIFTS):
            # Find who currently holds this slot (could be 0 or multiple)
            current_holders = [n for n in range(NUM_NURSES) if schedule[n][d][s] == 1]
            for n_to in range(NUM_NURSES):
                if n_to not in current_holders:
                    new_sched = copy.deepcopy(schedule)
                    # Remove from current holders
                    for n_from in current_holders:
                        new_sched[n_from][d][s] = 0
                    # Assign to new nurse
                    new_sched[n_to][d][s] = 1
                    move = (tuple(current_holders), n_to, d, s)
                    neighbors.append((new_sched, move))
    return neighbors

neighbors = get_neighbors(sol)
print(f"Number of neighbors for the initial solution: {len(neighbors)}")

# %% [markdown]
# ## Step 6: Tabu Search Algorithm
#
# ```
# 1. Initialize: Generate an initial solution S. Set S_best = S.
# 2. Initialize Tabu List (a fixed-size queue of forbidden moves).
# 3. Repeat for max_iterations:
#    a. Generate all neighbors of current solution S.
#    b. For each neighbor, compute its cost.
#    c. Select the BEST neighbor that is:
#       - NOT in the Tabu List, OR
#       - Passes the Aspiration Criterion (better than S_best).
#    d. Apply the move → S = best_neighbor.
#    e. Add the move to the Tabu List (evict oldest if list is full).
#    f. If cost(S) < cost(S_best): update S_best.
# 4. Return S_best.
# ```

# %%
def tabu_search(max_iterations=200, tabu_tenure=10, verbose=True):
    """
    Tabu Search for Employee Scheduling.

    Parameters:
    -----------
    max_iterations : int   - stopping criterion
    tabu_tenure    : int   - how long a move stays tabu (tabu list size)
    verbose        : bool  - print progress

    Returns:
    --------
    best_schedule, best_cost, cost_history
    """
    # ── Step 1: Initialization ──────────────────────────────────────────
    current  = create_random_solution()
    best     = copy.deepcopy(current)
    best_cost   = cost(best)
    current_cost = best_cost

    tabu_list   = []        # stores recently used moves
    cost_history = [best_cost]

    if verbose:
        print(f"Initial cost: {best_cost}")
        print(f"Running Tabu Search for {max_iterations} iterations...\n")

    # ── Step 2: Main Loop ───────────────────────────────────────────────
    for iteration in range(max_iterations):

        # Step 2a: Generate neighbors
        neighbors = get_neighbors(current)

        # Step 2b & 2c: Find best admissible neighbor
        best_neighbor       = None
        best_neighbor_cost  = float('inf')
        best_move           = None

        for neighbor_sched, move in neighbors:
            neighbor_cost = cost(neighbor_sched)

            in_tabu = move in tabu_list

            # Aspiration criterion: override tabu if this is a new global best
            aspiration = (neighbor_cost < best_cost)

            if (not in_tabu) or aspiration:
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor      = neighbor_sched
                    best_neighbor_cost = neighbor_cost
                    best_move          = move

        # If no admissible neighbor found, pick the least bad tabu move
        if best_neighbor is None:
            for neighbor_sched, move in neighbors:
                neighbor_cost = cost(neighbor_sched)
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor      = neighbor_sched
                    best_neighbor_cost = neighbor_cost
                    best_move          = move

        # Step 2d: Move to best neighbor
        current      = best_neighbor
        current_cost = best_neighbor_cost

        # Step 2e: Update Tabu List (FIFO with fixed tenure)
        tabu_list.append(best_move)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        # Step 2f: Update global best
        if current_cost < best_cost:
            best      = copy.deepcopy(current)
            best_cost = current_cost
            if verbose:
                print(f"  Iter {iteration+1:>4}: ✅ New best cost = {best_cost}")

        cost_history.append(best_cost)

        # Early exit if optimal
        if best_cost == 0:
            if verbose:
                print(f"\n🎉 Optimal solution found at iteration {iteration+1}!")
            break

    return best, best_cost, cost_history


# Run the algorithm
best_schedule, best_cost, cost_history = tabu_search(
    max_iterations=300,
    tabu_tenure=8,
    verbose=True
)

# %% [markdown]
# ## Step 7: Results

# %%
print_schedule(best_schedule, f"Best Schedule Found (Cost = {best_cost})")

if best_cost == 0:
    print("\n✅ All constraints satisfied! This is a valid schedule.")
else:
    print(f"\n⚠️  Residual penalty: {best_cost}. Some constraints may be violated.")

# Breakdown of violations
print("\n--- Constraint Check ---")
for d in range(NUM_DAYS):
    for s in range(NUM_SHIFTS):
        coverage = sum(best_schedule[n][d][s] for n in range(NUM_NURSES))
        status = "✅" if coverage == 1 else "❌"
        print(f"  {status} Day {d} | {SHIFT_NAMES[s]:<10}: covered by {coverage} nurse(s)")

print()
for n in range(NUM_NURSES):
    total = best_schedule[n].sum()
    daily = [best_schedule[n][d].sum() for d in range(NUM_DAYS)]
    double = sum(1 for x in daily if x > 1)
    status = "✅" if (MIN_SHIFTS_PER_NURSE <= total <= MAX_SHIFTS_PER_NURSE and double == 0) else "❌"
    print(f"  {status} {NURSE_NAMES[n]}: {total} shifts total, double-shifts: {double}")

# %% [markdown]
# ## Step 8: Convergence Plot

# %%
plt.figure(figsize=(10, 5))
plt.plot(cost_history, color='steelblue', linewidth=2, label='Best Cost')
plt.axhline(y=0, color='green', linestyle='--', linewidth=1.5, label='Optimal (cost=0)')
plt.xlabel('Iteration', fontsize=13)
plt.ylabel('Penalty Cost', fontsize=13)
plt.title('Tabu Search Convergence — Employee Scheduling', fontsize=15)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('convergence.png', dpi=150)
plt.show()
print("Convergence plot saved as 'convergence.png'")

# %% [markdown]
# ## Step 9: Visualize the Schedule as a Heatmap

# %%
fig, axes = plt.subplots(1, NUM_DAYS, figsize=(4 * NUM_DAYS, 4), sharey=True)
fig.suptitle('Final Employee Schedule', fontsize=16, fontweight='bold')

colors = {0: '#f0f0f0', 1: '#2196F3'}  # 0=off, 1=working

for d, ax in enumerate(axes):
    matrix = best_schedule[:, d, :]   # shape: (nurses, shifts)
    im = ax.imshow(matrix, cmap='Blues', vmin=0, vmax=1, aspect='auto')
    ax.set_title(f'Day {d}', fontsize=13, fontweight='bold')
    ax.set_xticks(range(NUM_SHIFTS))
    ax.set_xticklabels(SHIFT_NAMES, rotation=30, ha='right')
    if d == 0:
        ax.set_yticks(range(NUM_NURSES))
        ax.set_yticklabels(NURSE_NAMES)
    # Annotate cells
    for n in range(NUM_NURSES):
        for s in range(NUM_SHIFTS):
            val = matrix[n, s]
            ax.text(s, n, '✓' if val else '', ha='center', va='center',
                    fontsize=16, color='white' if val else '#ccc')

off_patch  = mpatches.Patch(color='#dce9f5', label='Off')
on_patch   = mpatches.Patch(color='#2196F3', label='Working')
fig.legend(handles=[off_patch, on_patch], loc='lower center', ncol=2, fontsize=12,
           bbox_to_anchor=(0.5, -0.05))
plt.tight_layout()
plt.savefig('schedule_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("Schedule heatmap saved as 'schedule_heatmap.png'")

# %% [markdown]
# ## Step 10: Sensitivity Analysis — Effect of Tabu Tenure

# %%
print("Running sensitivity analysis on Tabu Tenure...")
tenures      = [2, 5, 8, 12, 20]
results      = {}

for tenure in tenures:
    _, fc, hist = tabu_search(max_iterations=300, tabu_tenure=tenure, verbose=False)
    results[tenure] = (fc, hist)
    print(f"  Tenure={tenure:>3}: Final cost = {fc}")

plt.figure(figsize=(10, 5))
for tenure, (_, hist) in results.items():
    plt.plot(hist, label=f'Tenure={tenure}', linewidth=1.8)

plt.xlabel('Iteration', fontsize=13)
plt.ylabel('Best Cost', fontsize=13)
plt.title('Effect of Tabu Tenure on Convergence', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('sensitivity.png', dpi=150)
plt.show()
print("Sensitivity plot saved as 'sensitivity.png'")

# %% [markdown]
# ---
# ## Summary
#
# | Component            | Details                                               |
# |----------------------|-------------------------------------------------------|
# | **Problem**          | Nurse scheduling (4 nurses, 3 days, 3 shifts/day)     |
# | **Solution Rep.**    | 3D binary array `[nurse][day][shift]`                 |
# | **Objective**        | Minimize constraint violations (penalty cost)         |
# | **Neighborhood**     | Reassign a shift slot to a different nurse            |
# | **Tabu List**        | FIFO queue of recent moves (configurable tenure)      |
# | **Aspiration**       | Override tabu if move yields new global best          |
# | **Stopping Rule**    | Max iterations OR cost == 0 (optimal)                 |
#
# ### Key Tabu Search Parameters
# - **Tabu Tenure**: Too small → cycling; Too large → misses good moves. Tune empirically.
# - **Neighborhood Size**: Larger neighborhoods find better solutions but are slower.
# - **Aspiration Criterion**: Prevents the tabu list from blocking globally optimal moves.