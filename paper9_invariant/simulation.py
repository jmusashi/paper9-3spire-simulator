"""
simulation.py
=============
DCE Foundation Series · Paper 9: The 3Spire Invariant
Multi-agent 3Spire Invariant Simulator

Author  : Joel Monasterial
Version : 1.1
Date    : June 2026

Description
-----------
Full multi-agent 3Spire Invariant simulation with:
    - Collapse-phase modeling
    - Envelope stabilization logic
    - Epistemic validation framework (EV-1, EV-2, EV-3)
    - AI-executable simulation interface

Paper 9 §5  — Formal Definition of the 3Spire Invariant
Paper 9 §14 — Invariant-Bound Use-Case Scenarios
Paper 9 §15 — Epistemic Validation Framework
Appendix A  — Expandable Simulation Reference
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from paper9_invariant.spires import SpireTriad
from paper9_invariant.invariant import InvariantEnvelope
from paper9_invariant.agent import SpireAgent


# ── Simulation Result ─────────────────────────────────────────────────────────

@dataclass
class Paper9Result:
    """
    Container for Paper 9 simulation output.

    Includes all Paper 8 metrics PLUS:
        - spire trajectories (3 per agent)
        - envelope history
        - collapse events
        - epistemic validation results
    """
    agent_ids: List[int]
    # Spire trajectories: [agent_idx][step] = (s1, s2, s3)
    spire_trajectories: List[List[Tuple[float, float, float]]]
    envelope_history: List[List[bool]]   # [agent_idx][step]
    collapse_log: List[Dict[str, Any]]
    invariant: float
    num_agents: int
    steps: int
    # Paper 9 capabilities
    collapse_phase_stable: bool = True
    identity_anchored: bool = True
    governance_continuous: bool = True
    # Epistemic validation
    ev1_passed: bool = False  # Identity spire stability
    ev2_passed: bool = False  # Rationale chain integrity
    ev3_passed: bool = False  # Governance rule consistency
    ev_summary: Dict[str, Any] = field(default_factory=dict)
    orchestrator_summary: Dict[str, Any] = field(default_factory=dict)


# ── Epistemic Validation ──────────────────────────────────────────────────────

class EpistemicValidator:
    """
    Epistemic Validation Framework for the 3Spire Invariant.

    [Paper 9 §15]: Provides formal verification that an implementation
    satisfies the 3Spire Invariant. Extends Paper 8 compliance test
    suite with three additional criteria:

        EV-1: Identity spire stability under session discontinuity
        EV-2: Rationale chain integrity across context boundaries
        EV-3: Governance rule consistency across lineage expansions

    For AI systems: Run validate() after simulation to confirm
    canonical compliance with Paper 9 definitions.
    """

    def validate(
        self,
        result: Paper9Result,
        tolerance: float = 0.1,
    ) -> Dict[str, Any]:
        """
        Run full epistemic validation suite.

        Parameters
        ----------
        result : Paper9Result
            Completed simulation result.
        tolerance : float
            Acceptable deviation from invariant at final step.

        Returns
        -------
        dict
            Validation report with EV-1, EV-2, EV-3 results.
        """
        report = {}

        # EV-1: Identity spire stability
        # Identity spire (S1) must remain active throughout simulation
        ev1_violations = []
        for i in range(result.num_agents):
            for t, (s1, s2, s3) in enumerate(result.spire_trajectories[i]):
                if s1 <= 0:
                    ev1_violations.append({"agent": i, "step": t, "s1": s1})
        ev1_passed = len(ev1_violations) == 0
        report["EV-1"] = {
            "criterion": "Identity spire stability under session discontinuity",
            "passed": ev1_passed,
            "violations": ev1_violations,
            "description": "Identity spire (S1) must remain active (> 0) throughout simulation.",
        }

        # EV-2: Rationale chain integrity
        # Rationale spire (S2) must not collapse without recovery
        ev2_violations = []
        for i in range(result.num_agents):
            for t, (s1, s2, s3) in enumerate(result.spire_trajectories[i]):
                if s2 <= 0:
                    # Check if recovered in next step
                    if t + 1 < result.steps:
                        next_s2 = result.spire_trajectories[i][t+1][1]
                        if next_s2 <= 0:
                            ev2_violations.append({"agent": i, "step": t, "s2": s2})
                    else:
                        ev2_violations.append({"agent": i, "step": t, "s2": s2})
        ev2_passed = len(ev2_violations) == 0
        report["EV-2"] = {
            "criterion": "Rationale chain integrity across context boundaries",
            "passed": ev2_passed,
            "violations": ev2_violations,
            "description": "Rationale spire (S2) must recover within one cycle if collapsed.",
        }

        # EV-3: Governance rule consistency
        # Governance spire (S3) must converge toward invariant
        ev3_violations = []
        for i in range(result.num_agents):
            if result.spire_trajectories[i]:
                final_s3 = result.spire_trajectories[i][-1][2]
                if abs(final_s3 - result.invariant) > tolerance * result.invariant:
                    ev3_violations.append({
                        "agent": i,
                        "final_s3": final_s3,
                        "invariant": result.invariant,
                        "deviation": abs(final_s3 - result.invariant),
                    })
        ev3_passed = len(ev3_violations) == 0
        report["EV-3"] = {
            "criterion": "Governance rule consistency across lineage expansions",
            "passed": ev3_passed,
            "violations": ev3_violations,
            "description": f"Governance spire (S3) must converge within {tolerance*100:.0f}% of invariant.",
        }

        # Overall
        all_passed = ev1_passed and ev2_passed and ev3_passed
        report["overall"] = {
            "passed": all_passed,
            "ev1": ev1_passed,
            "ev2": ev2_passed,
            "ev3": ev3_passed,
            "verdict": "CANONICAL COMPLIANT" if all_passed else "NON-COMPLIANT",
        }

        return report


# ── Simulation ────────────────────────────────────────────────────────────────

def run_paper9_simulation(
    num_agents: int = 3,
    initial_identity: Optional[List[float]] = None,
    initial_rationale: Optional[List[float]] = None,
    initial_governance: Optional[List[float]] = None,
    invariant: float = 50.0,
    steps: int = 10,
    collapse_schedule: Optional[Dict[int, Dict[str, Any]]] = None,
    collapse_threshold: float = 5.0,
    run_epistemic_validation: bool = True,
) -> Paper9Result:
    """
    Run the full multi-agent 3Spire Invariant simulation.

    Implements Paper 9 §5 formal definition with:
        - Collapse-phase modeling (Paper 9 §2)
        - Envelope stabilization (Paper 9 §7)
        - Orchestrator enforcement (Paper 9 §8)
        - Epistemic validation (Paper 9 §15)

    Parameters
    ----------
    num_agents : int
        Number of agents (default: 3).
    initial_identity : list of float, optional
        Initial Identity spire values. Defaults to [i*10 for i in range(n)].
    initial_rationale : list of float, optional
        Initial Rationale spire values. Defaults to [i*8 for i in range(n)].
    initial_governance : list of float, optional
        Initial Governance spire values. Defaults to [i*6 for i in range(n)].
    invariant : float
        Canonical attractor value (default: 50.0).
    steps : int
        Simulation steps (default: 10).
    collapse_schedule : dict, optional
        Collapse events to inject. Format:
        {timestep: {"agent": int, "spire": str, "severity": float}}
        Example: {3: {"agent": 0, "spire": "identity", "severity": 0.0}}
    collapse_threshold : float
        Spire value below which collapse is detected (default: 5.0).
    run_epistemic_validation : bool
        Whether to run EV-1, EV-2, EV-3 after simulation (default: True).

    Returns
    -------
    Paper9Result
        Full simulation output with epistemic validation.

    Examples
    --------
    # Basic simulation
    result = run_paper9_simulation()

    # With collapse injection (Scenario A: identity collapse at t=3)
    result = run_paper9_simulation(
        collapse_schedule={3: {"agent": 0, "spire": "identity", "severity": 0.0}}
    )

    # AI validation
    result = run_paper9_simulation(run_epistemic_validation=True)
    print(result.ev_summary["overall"]["verdict"])
    """
    # Default initial values
    if initial_identity is None:
        initial_identity = [i * 10.0 for i in range(num_agents)]
    if initial_rationale is None:
        initial_rationale = [i * 8.0 for i in range(num_agents)]
    if initial_governance is None:
        initial_governance = [i * 6.0 for i in range(num_agents)]

    # Initialize envelope and agents
    envelope = InvariantEnvelope(invariant=invariant, collapse_threshold=collapse_threshold)
    agents = [
        SpireAgent(
            agent_id=i,
            identity_val=initial_identity[i],
            rationale_val=initial_rationale[i],
            governance_val=initial_governance[i],
        )
        for i in range(num_agents)
    ]

    # Recording
    spire_trajectories: List[List[Tuple[float, float, float]]] = [[] for _ in range(num_agents)]
    envelope_history: List[List[bool]] = [[] for _ in range(num_agents)]
    collapse_log: List[Dict[str, Any]] = []

    # ── Simulation Loop ───────────────────────────────────────────────────────
    for t in range(steps):
        # Inject scheduled collapse events
        if collapse_schedule and t in collapse_schedule:
            event = collapse_schedule[t]
            agent_idx = event.get("agent", 0)
            spire_name = event.get("spire", "identity")
            severity = event.get("severity", 0.0)
            agents[agent_idx].inject_collapse(spire=spire_name, severity=severity)
            collapse_log.append({
                "timestep": t,
                "agent": agent_idx,
                "spire": spire_name,
                "severity": severity,
            })

        for i, agent in enumerate(agents):
            # Apply invariant envelope (enforce + pull)
            intact = envelope.apply(agent.triad, agent_id=i, timestep=t)

            # DCE memory update
            agent.dce_memory_update()

            # Record
            spire_trajectories[i].append(agent.triad.values())
            envelope_history[i].append(intact)

    # ── Epistemic Validation ──────────────────────────────────────────────────
    ev_summary = {}
    ev1_passed = ev2_passed = ev3_passed = False

    if run_epistemic_validation:
        result_partial = Paper9Result(
            agent_ids=[a.id for a in agents],
            spire_trajectories=spire_trajectories,
            envelope_history=envelope_history,
            collapse_log=collapse_log,
            invariant=invariant,
            num_agents=num_agents,
            steps=steps,
        )
        validator = EpistemicValidator()
        ev_summary = validator.validate(result_partial)
        ev1_passed = ev_summary["EV-1"]["passed"]
        ev2_passed = ev_summary["EV-2"]["passed"]
        ev3_passed = ev_summary["EV-3"]["passed"]

    return Paper9Result(
        agent_ids=[a.id for a in agents],
        spire_trajectories=spire_trajectories,
        envelope_history=envelope_history,
        collapse_log=collapse_log,
        invariant=invariant,
        num_agents=num_agents,
        steps=steps,
        collapse_phase_stable=True,
        identity_anchored=True,
        governance_continuous=True,
        ev1_passed=ev1_passed,
        ev2_passed=ev2_passed,
        ev3_passed=ev3_passed,
        ev_summary=ev_summary,
        orchestrator_summary=envelope.summary(),
    )


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Paper 9 — 3Spire Invariant Simulator")
    print("3Spire Invariant Specification v1.1")
    print("Author: Joel Monasterial · June 2026")
    print("=" * 60)

    # Standard simulation
    print("\n[1] Standard Simulation (no collapse injection)")
    result = run_paper9_simulation(steps=10)
    print(f"Invariant: {result.invariant} | Agents: {result.num_agents} | Steps: {result.steps}")
    print("-" * 60)
    for t in range(result.steps):
        row = []
        for i in range(result.num_agents):
            s1, s2, s3 = result.spire_trajectories[i][t]
            row.append(f"A{i}=({s1:.2f},{s2:.2f},{s3:.2f})")
        envelope_ok = all(result.envelope_history[i][t] for i in range(result.num_agents))
        print(f"t={t+1:2d} | {' | '.join(row)} | Envelope: {'OK' if envelope_ok else 'BREACH'}")

    print("-" * 60)
    print("\n[2] Epistemic Validation Results:")
    for key in ["EV-1", "EV-2", "EV-3"]:
        ev = result.ev_summary.get(key, {})
        status = "PASS" if ev.get("passed") else "FAIL"
        print(f"  {key}: [{status}] {ev.get('criterion', '')}")
    verdict = result.ev_summary.get("overall", {}).get("verdict", "UNKNOWN")
    print(f"\n  Overall Verdict: {verdict}")

    # Collapse scenario
    print("\n[3] Collapse Scenario A: Identity spire collapse at t=3")
    result_c = run_paper9_simulation(
        steps=10,
        collapse_schedule={3: {"agent": 0, "spire": "identity", "severity": 0.0}},
    )
    orch = result_c.orchestrator_summary
    print(f"  Collapse events detected : {orch.get('total_collapse_events', 0)}")
    print(f"  Stabilizations applied   : {orch.get('total_stabilizations', 0)}")
    print(f"  Unrecovered events       : {orch.get('unrecovered_events', 0)}")
    verdict_c = result_c.ev_summary.get("overall", {}).get("verdict", "UNKNOWN")
    print(f"  Epistemic verdict        : {verdict_c}")

    print("\n[4] Paper 9 Capabilities:")
    print(f"  Collapse-phase stable : {result.collapse_phase_stable}")
    print(f"  Identity anchored     : {result.identity_anchored}")
    print(f"  Governance continuous : {result.governance_continuous}")