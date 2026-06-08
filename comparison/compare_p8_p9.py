"""
compare_p8_p9.py
================
DCE Foundation Series — Paper 8 vs Paper 9 Comparison Harness

Author  : Joel Monasterial
Version : 1.1
Date    : June 2026

Description
-----------
Runs both Paper 8 (3Sync) and Paper 9 (3Spire Invariant) simulations
side-by-side and produces a structured comparison report.

Demonstrates:
    - Convergence behavior (both papers)
    - Collapse-phase stability (Paper 9 only)
    - Identity anchoring (Paper 9 only)
    - Governance continuity (Paper 9 only)
    - Epistemic validation (Paper 9 only)

Paper 9 Appendix A.2 — Comparison: Paper 8 (3Sync) vs. Paper 9 (3Spire)

Usage
-----
    python comparison/compare_p8_p9.py

    # Or import and use programmatically:
    from comparison.compare_p8_p9 import run_comparison
    report = run_comparison()
"""

from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paper8_baseline.paper8_sim import run_paper8_simulation
from paper9_invariant.simulation import run_paper9_simulation
from typing import Dict, Any


# ── Comparison Properties ─────────────────────────────────────────────────────

COMPARISON_PROPERTIES = [
    ("Synchronization",         "Triadic",  "Triadic"),
    ("Identity anchoring",      "No",       "Yes"),
    ("Rationale preservation",  "No",       "Yes"),
    ("Governance continuity",   "No",       "Yes"),
    ("Collapse-phase stability","No",       "Yes"),
    ("Invariant envelope",      "No",       "Yes"),
    ("Orchestrator",            "No",       "Yes"),
    ("Epistemic validation",    "No",       "Yes (EV-1, EV-2, EV-3)"),
]


# ── Comparison Harness ────────────────────────────────────────────────────────

def run_comparison(
    num_agents: int = 3,
    invariant: float = 50.0,
    steps: int = 10,
    collapse_schedule: Dict = None,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Run Paper 8 and Paper 9 simulations and compare results.

    [Paper 9 Appendix A.2]: Structural comparison between
    Paper 8 (3Sync mechanism) and Paper 9 (3Spire architecture).

    Parameters
    ----------
    num_agents : int
        Number of agents (default: 3).
    invariant : float
        Canonical attractor value (default: 50.0).
    steps : int
        Simulation steps (default: 10).
    collapse_schedule : dict, optional
        Collapse events for Paper 9 simulation.
        Example: {3: {"agent": 0, "spire": "identity", "severity": 0.0}}
    verbose : bool
        Print comparison report (default: True).

    Returns
    -------
    dict
        Full comparison report.
    """
    # ── Run Paper 8 ───────────────────────────────────────────────────────────
    p8 = run_paper8_simulation(
        num_agents=num_agents,
        invariant=invariant,
        steps=steps,
    )

    # ── Run Paper 9 ───────────────────────────────────────────────────────────
    p9 = run_paper9_simulation(
        num_agents=num_agents,
        invariant=invariant,
        steps=steps,
        collapse_schedule=collapse_schedule,
        run_epistemic_validation=True,
    )

    # ── Convergence Analysis ──────────────────────────────────────────────────
    p8_final_states = [p8.trajectories[i][-1] for i in range(num_agents)]
    p9_final_identity = [p9.spire_trajectories[i][-1][0] for i in range(num_agents)]
    p9_final_rationale = [p9.spire_trajectories[i][-1][1] for i in range(num_agents)]
    p9_final_governance = [p9.spire_trajectories[i][-1][2] for i in range(num_agents)]

    p8_convergence = max(abs(s - invariant) for s in p8_final_states)
    p9_convergence = max(
        abs(s - invariant)
        for s in p9_final_identity + p9_final_rationale + p9_final_governance
    )

    # ── Build Report ──────────────────────────────────────────────────────────
    report = {
        "paper8": {
            "name": "3Sync Architecture",
            "doi": "10.5281/zenodo.20406312",
            "final_states": p8_final_states,
            "convergence_error": round(p8_convergence, 4),
            "collapse_phase_stable": p8.collapse_phase_stable,
            "identity_anchored": p8.identity_anchored,
            "governance_continuous": p8.governance_continuous,
            "environment_trace_length": len(p8.environment_trace),
        },
        "paper9": {
            "name": "3Spire Invariant",
            "version": "1.1",
            "final_identity": p9_final_identity,
            "final_rationale": p9_final_rationale,
            "final_governance": p9_final_governance,
            "convergence_error": round(p9_convergence, 4),
            "collapse_phase_stable": p9.collapse_phase_stable,
            "identity_anchored": p9.identity_anchored,
            "governance_continuous": p9.governance_continuous,
            "collapse_events": len(p9.collapse_log),
            "orchestrator": p9.orchestrator_summary,
            "ev1_passed": p9.ev1_passed,
            "ev2_passed": p9.ev2_passed,
            "ev3_passed": p9.ev3_passed,
            "epistemic_verdict": p9.ev_summary.get("overall", {}).get("verdict", "N/A"),
        },
        "structural_comparison": COMPARISON_PROPERTIES,
        "convergence_winner": "Paper 9" if p9_convergence <= p8_convergence else "Paper 8",
    }

    # ── Print Report ──────────────────────────────────────────────────────────
    if verbose:
        _print_report(report, p8, p9, invariant, steps)

    return report


def _print_report(report, p8, p9, invariant, steps):
    """Print formatted comparison report."""
    print("=" * 70)
    print("DCE Foundation Series — Paper 8 vs Paper 9 Comparison")
    print("=" * 70)

    print(f"\nConfiguration: {p8.num_agents} agents | invariant={invariant} | steps={steps}")

    # Structural comparison table
    print("\n── Structural Comparison ──────────────────────────────────────────")
    print(f"{'Property':<30} {'Paper 8 (3Sync)':<20} {'Paper 9 (3Spire)':<20}")
    print("-" * 70)
    for prop, p8_val, p9_val in COMPARISON_PROPERTIES:
        print(f"{prop:<30} {p8_val:<20} {p9_val:<20}")

    # Convergence
    print("\n── Convergence Results ────────────────────────────────────────────")
    print(f"{'Metric':<35} {'Paper 8':<15} {'Paper 9':<15}")
    print("-" * 65)
    print(f"{'Final state error (max)':<35} "
          f"{report['paper8']['convergence_error']:<15.4f} "
          f"{report['paper9']['convergence_error']:<15.4f}")
    print(f"{'Collapse-phase stable':<35} "
          f"{str(report['paper8']['collapse_phase_stable']):<15} "
          f"{str(report['paper9']['collapse_phase_stable']):<15}")
    print(f"{'Identity anchored':<35} "
          f"{str(report['paper8']['identity_anchored']):<15} "
          f"{str(report['paper9']['identity_anchored']):<15}")
    print(f"{'Governance continuous':<35} "
          f"{str(report['paper8']['governance_continuous']):<15} "
          f"{str(report['paper9']['governance_continuous']):<15}")

    # Epistemic validation
    print("\n── Epistemic Validation (Paper 9 only) ────────────────────────────")
    print(f"  EV-1 (Identity stability)    : {'PASS' if report['paper9']['ev1_passed'] else 'FAIL'}")
    print(f"  EV-2 (Rationale integrity)   : {'PASS' if report['paper9']['ev2_passed'] else 'FAIL'}")
    print(f"  EV-3 (Governance consistency): {'PASS' if report['paper9']['ev3_passed'] else 'FAIL'}")
    print(f"  Overall Verdict              : {report['paper9']['epistemic_verdict']}")

    # Orchestrator
    orch = report['paper9']['orchestrator']
    print("\n── Orchestrator Activity (Paper 9) ────────────────────────────────")
    print(f"  Collapse events detected : {orch.get('total_collapse_events', 0)}")
    print(f"  Stabilizations applied   : {orch.get('total_stabilizations', 0)}")
    print(f"  Unrecovered events       : {orch.get('unrecovered_events', 0)}")

    print("\n── Summary ────────────────────────────────────────────────────────")
    print(f"  Paper 8: mechanism — synchronizes but cannot stabilize collapse.")
    print(f"  Paper 9: architecture — synchronizes AND stabilizes collapse.")
    print(f"  Convergence winner: {report['convergence_winner']}")
    print("=" * 70)


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n[Standard Comparison — no collapse injection]")
    run_comparison()

    print("\n[Collapse Scenario A — Identity spire collapse at t=3]")
    run_comparison(
        collapse_schedule={3: {"agent": 0, "spire": "identity", "severity": 0.0}},
        verbose=True,
    )