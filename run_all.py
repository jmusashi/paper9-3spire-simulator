"""
run_all.py
==========
DCE Foundation Series · Paper 9: The 3Spire Invariant
Master simulation runner — executes all scenarios

Author  : Joel Monasterial
Version : 1.1
Date    : June 2026

Usage
-----
    python run_all.py

Runs:
    1. Paper 8 baseline simulation
    2. Paper 9 standard simulation
    3. Paper 9 collapse scenarios (A–E from §14)
    4. Paper 8 vs Paper 9 comparison
    5. Epistemic validation suite
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from paper8_baseline.paper8_sim import run_paper8_simulation
from paper9_invariant.simulation import run_paper9_simulation
from comparison.compare_p8_p9 import run_comparison


def run_all():
    print("=" * 70)
    print("DCE Foundation Series — Paper 9: The 3Spire Invariant")
    print("3Spire Invariant Specification v1.1")
    print("Author: Joel Monasterial · June 2026")
    print("=" * 70)

    # ── 1. Paper 8 Baseline ───────────────────────────────────────────────────
    print("\n[1/5] Paper 8 Baseline Simulation (3Sync Architecture)")
    print("-" * 50)
    p8 = run_paper8_simulation(steps=10)
    for t in range(p8.steps):
        states = [round(p8.trajectories[i][t], 3) for i in range(p8.num_agents)]
        print(f"  t={t+1:2d} | States: {states}")
    print(f"  Final convergence error: "
          f"{max(abs(p8.trajectories[i][-1] - p8.invariant) for i in range(p8.num_agents)):.4f}")

    # ── 2. Paper 9 Standard ───────────────────────────────────────────────────
    print("\n[2/5] Paper 9 Standard Simulation (3Spire Invariant)")
    print("-" * 50)
    p9 = run_paper9_simulation(steps=10)
    for t in range(p9.steps):
        row = []
        for i in range(p9.num_agents):
            s1, s2, s3 = p9.spire_trajectories[i][t]
            row.append(f"A{i}=({s1:.2f},{s2:.2f},{s3:.2f})")
        print(f"  t={t+1:2d} | {' | '.join(row)}")
    print(f"  Epistemic verdict: {p9.ev_summary.get('overall', {}).get('verdict', 'N/A')}")

    # ── 3. Collapse Scenarios (§14) ───────────────────────────────────────────
    print("\n[3/5] Collapse Scenarios — Paper 9 §14")
    print("-" * 50)

    scenarios = {
        "A — Identity spire collapse (t=3)":
            {3: {"agent": 0, "spire": "identity",   "severity": 0.0}},
        "B — Rationale spire collapse (t=3)":
            {3: {"agent": 1, "spire": "rationale",  "severity": 0.0}},
        "C — Governance spire collapse (t=3)":
            {3: {"agent": 2, "spire": "governance", "severity": 0.0}},
        "D — Dual-spire stress (t=3, identity+rationale)":
            {3: {"agent": 0, "spire": "identity",   "severity": 0.1},
             4: {"agent": 0, "spire": "rationale",  "severity": 0.1}},
        "E — Full envelope test (t=2, all agents)":
            {2: {"agent": 0, "spire": "identity",   "severity": 0.05},
             3: {"agent": 1, "spire": "rationale",  "severity": 0.05},
             4: {"agent": 2, "spire": "governance", "severity": 0.05}},
    }

    for name, schedule in scenarios.items():
        result = run_paper9_simulation(steps=10, collapse_schedule=schedule)
        orch = result.orchestrator_summary
        verdict = result.ev_summary.get("overall", {}).get("verdict", "N/A")
        print(f"  Scenario {name}")
        print(f"    Collapses: {orch.get('total_collapse_events',0)} | "
              f"Stabilized: {orch.get('total_stabilizations',0)} | "
              f"Verdict: {verdict}")

    # ── 4. Comparison ─────────────────────────────────────────────────────────
    print("\n[4/5] Paper 8 vs Paper 9 Comparison")
    print("-" * 50)
    run_comparison(verbose=True)

    # ── 5. Epistemic Validation ───────────────────────────────────────────────
    print("\n[5/5] Epistemic Validation Suite — Paper 9 §15")
    print("-" * 50)
    p9_ev = run_paper9_simulation(steps=20, run_epistemic_validation=True)
    for key in ["EV-1", "EV-2", "EV-3"]:
        ev = p9_ev.ev_summary.get(key, {})
        status = "PASS ✓" if ev.get("passed") else "FAIL ✗"
        print(f"  {key}: [{status}] {ev.get('criterion', '')}")
    print(f"\n  Final Verdict: {p9_ev.ev_summary.get('overall', {}).get('verdict', 'N/A')}")

    print("\n" + "=" * 70)
    print("All simulations complete.")
    print("Paper 9 is the moment the DCE universe becomes structurally complete.")
    print("=" * 70)


if __name__ == "__main__":
    run_all()