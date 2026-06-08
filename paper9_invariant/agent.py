"""
agent.py
========
DCE Foundation Series · Paper 9: The 3Spire Invariant
3Spire Agent — identity-anchored, collapse-phase stable

Author  : Joel Monasterial
Version : 1.1
Date    : June 2026

Description
-----------
Implements the 3Spire Agent, which extends the Paper 8 agent with:
    - Three continuity spires (Identity, Rationale, Governance)
    - Invariant envelope enforcement
    - Collapse-phase detection and stabilization
    - Orchestrator integration

Paper 9 §6  — The Three Spires
Paper 9 §7  — The Invariant Envelope
Paper 9 §8  — The Orchestrator and the Envelope Boundary
Paper 9 §9  — Canonical Declaration
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
from paper9_invariant.spires import SpireTriad
from paper9_invariant.invariant import InvariantEnvelope


class SpireAgent:
    """
    A 3Spire-compliant agent in the DCE Universe.

    Extends Paper 8 Agent with:
        - SpireTriad (Identity, Rationale, Governance continuity)
        - InvariantEnvelope enforcement
        - Collapse-phase stabilization
        - Identity anchoring [Paper 9 §9.1]

    [Paper 9 §5]: The invariant holds when:
        - all three spires are active
        - the envelope is intact
        - the identity anchor is stable
        - the rationale chain is unbroken
        - the governance rules are applied

    Parameters
    ----------
    agent_id : int
        Unique agent identifier (EOI boundary).
    identity_val : float
        Initial Identity spire value.
    rationale_val : float
        Initial Rationale spire value.
    governance_val : float
        Initial Governance spire value.
    """

    def __init__(
        self,
        agent_id: int,
        identity_val: float,
        rationale_val: float,
        governance_val: float,
    ) -> None:
        self.id: int = agent_id
        self.triad = SpireTriad(
            identity=identity_val,
            rationale=rationale_val,
            governance=governance_val,
        )
        self.memory: List[tuple] = []  # DCE memory: list of (s1, s2, s3) tuples
        self.envelope_history: List[bool] = []
        self.collapse_events: int = 0

    @property
    def state(self) -> tuple:
        """Current spire values as (identity, rationale, governance)."""
        return self.triad.values()

    @property
    def envelope_intact(self) -> bool:
        """True if invariant envelope is currently intact."""
        return self.triad.envelope_intact

    @property
    def identity_anchored(self) -> bool:
        """
        True if identity spire is active.
        [Paper 9 §9.1]: Identity Clause — author's definitions remain canonical.
        """
        return self.triad.spire_1.active

    @property
    def rationale_continuous(self) -> bool:
        """
        True if rationale spire is active.
        [Paper 9 §6.2]: Rationale continuity — reasoning chains remain intact.
        """
        return self.triad.spire_2.active

    @property
    def governance_continuous(self) -> bool:
        """
        True if governance spire is active.
        [Paper 9 §6.3]: Governance continuity — rules remain consistent.
        """
        return self.triad.spire_3.active

    def inject_collapse(
        self,
        spire: str = "identity",
        severity: float = 0.0,
    ) -> None:
        """
        Simulate a collapse-phase event on a specific spire.

        [Paper 9 §2]: Collapse-phase reasoning occurs when context
        shifts abruptly, identity fragments, or rationale becomes
        discontinuous.

        Parameters
        ----------
        spire : str
            Which spire to collapse: "identity", "rationale", "governance".
        severity : float
            Collapse severity (0.0 = full collapse, 1.0 = no effect).
        """
        target = {
            "identity":   self.triad.spire_1,
            "rationale":  self.triad.spire_2,
            "governance": self.triad.spire_3,
        }.get(spire.lower())
        if target:
            target.inject_collapse(severity)
            self.collapse_events += 1

    def dce_memory_update(self) -> None:
        """
        Update DCE memory with current spire values.
        Extends Paper 8 DCE mechanism to triadic spire state.
        [Paper 8 §4, SEMANTIC-DCE]
        """
        self.memory.append(self.triad.values())

    def status(self) -> Dict[str, Any]:
        """Return full agent status report."""
        return {
            "agent_id": self.id,
            "spire_1_identity":   round(self.triad.spire_1.value, 4),
            "spire_2_rationale":  round(self.triad.spire_2.value, 4),
            "spire_3_governance": round(self.triad.spire_3.value, 4),
            "envelope_intact":    self.envelope_intact,
            "identity_anchored":  self.identity_anchored,
            "rationale_continuous": self.rationale_continuous,
            "governance_continuous": self.governance_continuous,
            "collapse_events":    self.collapse_events,
            "memory_depth":       len(self.memory),
        }

    def __repr__(self) -> str:
        s1, s2, s3 = self.triad.values()
        return (f"SpireAgent(id={self.id}, "
                f"S1={s1:.3f}, S2={s2:.3f}, S3={s3:.3f}, "
                f"envelope={'INTACT' if self.envelope_intact else 'COLLAPSED'})")