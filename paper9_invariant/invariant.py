"""
invariant.py
============
DCE Foundation Series · Paper 9: The 3Spire Invariant
Invariant envelope and orchestrator

Author  : Joel Monasterial
Version : 1.1
Date    : June 2026

Description
-----------
Implements the invariant envelope and orchestrator as defined in
Paper 9 §7 and §8.

The Envelope:
    - Binds the three spires
    - Ensures no spire drifts independently
    - Triggers stabilization when a spire collapses
    - Preserves continuity across discontinuities

The Orchestrator:
    - Monitors spire alignment
    - Detects collapse-phase events
    - Activates stabilizers
    - Enforces the envelope (does NOT replace the invariant)

Paper 9 §7 — The Invariant Envelope
Paper 9 §8 — The Orchestrator and the Envelope Boundary
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any
from paper9_invariant.spires import SpireTriad


# ── Collapse Event ────────────────────────────────────────────────────────────

@dataclass
class CollapseEvent:
    """
    Records a collapse-phase event detected by the orchestrator.

    [Paper 9 §2]: Collapse-phase reasoning occurs when context shifts
    abruptly, identity fragments, or rationale becomes discontinuous.
    """
    timestep: int
    agent_id: int
    spire_name: str
    severity: float
    recovered: bool = False

    def __repr__(self) -> str:
        status = "RECOVERED" if self.recovered else "UNRECOVERED"
        return (f"CollapseEvent(t={self.timestep}, agent={self.agent_id}, "
                f"spire={self.spire_name}, severity={self.severity:.2f}, {status})")


# ── Orchestrator ──────────────────────────────────────────────────────────────

class Orchestrator:
    """
    The orchestrator monitors spire alignment and enforces the envelope.

    [Paper 9 §8]:
        - monitors spire alignment
        - detects collapse-phase events
        - activates stabilizers
        - preserves the envelope

    CRITICAL: The orchestrator does NOT replace the invariant.
              It enforces it.

    Parameters
    ----------
    collapse_threshold : float
        Spire value below which a collapse event is detected (default: 5.0).
    """

    def __init__(self, collapse_threshold: float = 5.0) -> None:
        self.collapse_threshold = collapse_threshold
        self.collapse_log: List[CollapseEvent] = []
        self.stabilization_count: int = 0

    def monitor(self, triad: SpireTriad, agent_id: int, timestep: int) -> List[CollapseEvent]:
        """
        Monitor spire alignment and detect collapse-phase events.

        Parameters
        ----------
        triad : SpireTriad
            The agent's spire triad to monitor.
        agent_id : int
            Agent identifier.
        timestep : int
            Current simulation timestep.

        Returns
        -------
        list of CollapseEvent
            Any collapse events detected this timestep.
        """
        events = []
        for spire in [triad.spire_1, triad.spire_2, triad.spire_3]:
            if spire.value < self.collapse_threshold:
                event = CollapseEvent(
                    timestep=timestep,
                    agent_id=agent_id,
                    spire_name=spire.name,
                    severity=spire.value,
                )
                events.append(event)
                self.collapse_log.append(event)
        return events

    def enforce_envelope(self, triad: SpireTriad, agent_id: int, timestep: int) -> bool:
        """
        Enforce the invariant envelope by activating stabilizers.

        [Paper 9 §7]: Collapse in one spire triggers stabilization
        from the others. The envelope ensures continuity is preserved
        across discontinuities.

        Parameters
        ----------
        triad : SpireTriad
            The agent's spire triad.
        agent_id : int
            Agent identifier.
        timestep : int
            Current simulation timestep.

        Returns
        -------
        bool
            True if envelope is intact after enforcement.
        """
        if not triad.envelope_intact:
            return False

        # Detect and stabilize collapsed spires
        events = self.monitor(triad, agent_id, timestep)
        if events:
            report = triad.stabilize()
            for event in events:
                spire_key = f"spire_{['Identity','Rationale','Governance'].index(event.spire_name)+1}"
                if report.get(spire_key, False):
                    event.recovered = True
                    self.stabilization_count += 1

        return triad.envelope_intact

    def summary(self) -> Dict[str, Any]:
        """Return orchestrator activity summary."""
        return {
            "total_collapse_events": len(self.collapse_log),
            "total_stabilizations": self.stabilization_count,
            "unrecovered_events": sum(1 for e in self.collapse_log if not e.recovered),
            "collapse_log": self.collapse_log,
        }


# ── Invariant Envelope ────────────────────────────────────────────────────────

class InvariantEnvelope:
    """
    The invariant envelope — structural law of the DCE universe.

    [Paper 9 §7]: The envelope is the boundary that binds the three spires.
    It ensures:
        - no spire can drift independently
        - collapse in one spire triggers stabilization from the others
        - continuity is preserved across discontinuities

    The envelope is managed by the Orchestrator, which enforces it
    without replacing the invariant itself.

    Parameters
    ----------
    invariant : float
        Canonical attractor value (default: 50.0).
    collapse_threshold : float
        Collapse detection threshold (default: 5.0).
    """

    def __init__(
        self,
        invariant: float = 50.0,
        collapse_threshold: float = 5.0,
    ) -> None:
        self.invariant = invariant
        self.orchestrator = Orchestrator(collapse_threshold=collapse_threshold)

    def apply(self, triad: SpireTriad, agent_id: int, timestep: int) -> bool:
        """
        Apply the full envelope cycle to a spire triad:
            1. Enforce envelope (detect + stabilize collapses)
            2. Apply invariant attractor pull to all spires

        Parameters
        ----------
        triad : SpireTriad
            Agent's spire triad.
        agent_id : int
            Agent identifier.
        timestep : int
            Current timestep.

        Returns
        -------
        bool
            True if envelope remains intact.
        """
        intact = self.orchestrator.enforce_envelope(triad, agent_id, timestep)
        triad.pull_all(self.invariant)
        return intact

    def summary(self) -> Dict[str, Any]:
        """Return full envelope activity summary."""
        return self.orchestrator.summary()