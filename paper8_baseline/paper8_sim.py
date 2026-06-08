"""
paper8_sim.py
=============
DCE Foundation Series · Paper 8: The 3Sync Architecture
Baseline Simulator — for comparison with Paper 9 (3Spire Invariant)

DOI     : 10.5281/zenodo.20406312
GitHub  : https://github.com/jmusashi/paper-8-substrate
Author  : Joel Monasterial
Version : 1.0

Description
-----------
Implements the minimal 3Sync simulation exactly as described in
Paper 8 §4, Listing 1. Three agents with divergent initial states
converge toward invariant = 50 via:

    Axis 1 — Stigmergy   : environmental coordination
    Axis 2 — HiveSync    : invariant attractor pull
    Axis 3 — DCE         : temporal continuity via memory

This module is used as the Paper 8 baseline in the Paper 8 vs Paper 9
comparison harness (see comparison/compare_p8_p9.py).

Canonical References
--------------------
[SEMANTIC-3SYNC]     : tri-axis coherence architecture
[SEMANTIC-HIVESYNC]  : synchronization invariant / shared attractor
[SEMANTIC-DCE]       : decision continuity via weighted memory
[SEMANTIC-STIGMERGY] : indirect coordination via shared environment
[SEMANTIC-EOI]       : identity boundary
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


# ── Environment ───────────────────────────────────────────────────────────────

class Environment:
    """
    Shared stigmergic environment [SEMANTIC-STIGMERGY].
    Agents coordinate exclusively through this shared trace.
    No direct agent-to-agent communication.
    """

    def __init__(self) -> None:
        self.trace: List[float] = []

    def write(self, signal: float) -> None:
        """Deposit agent state signal into environment."""
        self.trace.append(signal)

    def read(self) -> List[float]:
        """Read full accumulated trace."""
        return self.trace


# ── Agent ─────────────────────────────────────────────────────────────────────

class Agent:
    """
    3Sync agent [SEMANTIC-EOI].
    Maintains unique identity boundary throughout simulation.
    """

    def __init__(self, agent_id: int, initial_state: float) -> None:
        self.id: int = agent_id
        self.state: float = initial_state
        self.memory: List[float] = []

    def stigmergy_write(self, env: Environment) -> None:
        """Write state to shared environment [SEMANTIC-STIGMERGY]."""
        env.write(self.state)

    def stigmergy_read(self, env: Environment) -> List[float]:
        """Read accumulated trace [SEMANTIC-STIGMERGY]."""
        return env.read()

    def hivesync(self, invariant: float) -> None:
        """Converge toward shared attractor [SEMANTIC-HIVESYNC]."""
        self.state = (self.state + invariant) / 2

    def dce(self) -> None:
        """Preserve temporal continuity via memory [SEMANTIC-DCE]."""
        if self.memory:
            self.state = (self.state + self.memory[-1]) / 2
        self.memory.append(self.state)


# ── Simulation Result ─────────────────────────────────────────────────────────

@dataclass
class Paper8Result:
    """Container for Paper 8 simulation output."""
    agent_ids: List[int]
    trajectories: List[List[float]]
    memories: List[List[float]]
    environment_trace: List[float]
    invariant: float
    num_agents: int
    steps: int
    # Paper 8 has no collapse-phase stabilization
    collapse_phase_stable: bool = False
    identity_anchored: bool = False
    governance_continuous: bool = False


# ── Simulation ────────────────────────────────────────────────────────────────

def run_paper8_simulation(
    num_agents: int = 3,
    initial_states: Optional[List[float]] = None,
    invariant: float = 50.0,
    steps: int = 10,
) -> Paper8Result:
    """
    Run Paper 8 minimal 3Sync simulation.

    Implements Paper 8 §4, Listing 1 exactly:
        for t in range(steps):
            for agent in agents:
                agent.stigmergy_write(env)
                agent.stigmergy_read(env)
                agent.hivesync(invariant)
                agent.dce()

    Parameters
    ----------
    num_agents : int
        Number of agents (default: 3).
    initial_states : list of float, optional
        Initial states. Defaults to [i*10 for i in range(n)].
    invariant : float
        HiveSync attractor (default: 50).
    steps : int
        Simulation steps (default: 10).

    Returns
    -------
    Paper8Result
        Full simulation output.
    """
    if initial_states is None:
        initial_states = [i * 10.0 for i in range(num_agents)]

    env = Environment()
    agents = [Agent(agent_id=i, initial_state=initial_states[i])
              for i in range(num_agents)]
    trajectories: List[List[float]] = [[] for _ in range(num_agents)]

    for _t in range(steps):
        for i, agent in enumerate(agents):
            agent.stigmergy_write(env)
            agent.stigmergy_read(env)
            agent.hivesync(invariant)
            agent.dce()
            trajectories[i].append(agent.state)

    return Paper8Result(
        agent_ids=[a.id for a in agents],
        trajectories=trajectories,
        memories=[list(a.memory) for a in agents],
        environment_trace=list(env.trace),
        invariant=invariant,
        num_agents=num_agents,
        steps=steps,
        collapse_phase_stable=False,
        identity_anchored=False,
        governance_continuous=False,
    )


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Paper 8 Baseline Simulator — 3Sync Architecture")
    print("DOI: 10.5281/zenodo.20406312")
    print("=" * 60)

    result = run_paper8_simulation()

    print(f"Invariant: {result.invariant} | Agents: {result.num_agents} | Steps: {result.steps}")
    print(f"Initial states: [0.0, 10.0, 20.0]")
    print("-" * 60)

    for t in range(result.steps):
        states = [round(result.trajectories[i][t], 4) for i in range(result.num_agents)]
        print(f"t={t+1:2d} | States: {states}")

    print("-" * 60)
    print("Paper 8 Capabilities:")
    print(f"  Collapse-phase stable : {result.collapse_phase_stable}")
    print(f"  Identity anchored     : {result.identity_anchored}")
    print(f"  Governance continuous : {result.governance_continuous}")
    print("\nNote: Paper 8 lacks collapse-phase stabilization.")
    print("      See Paper 9 (3Spire Invariant) for the architectural solution.")