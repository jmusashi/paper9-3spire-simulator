"""
spires.py
=========
DCE Foundation Series · Paper 9: The 3Spire Invariant
Spire definitions — Identity, Rationale, Governance Continuity

Author  : Joel Monasterial
Version : 1.1
Date    : June 2026

Description
-----------
Defines the three spires of the 3Spire Invariant:

    Spire 1 — Identity Continuity   : root spire
    Spire 2 — Rationale Continuity  : stabilizing spire
    Spire 3 — Governance Continuity : regulating spire

Each spire has:
    - a value (float) representing its current continuity level
    - an active property (True if value > 0)
    - a stabilize() method that recovers from collapse using peer spires
    - a pull() method that applies invariant attractor pull

Paper 9 §6 — The Three Spires
Paper 9 §7 — The Invariant Envelope
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional


@dataclass
class Spire:
    """
    A single continuity spire in the 3Spire Invariant.

    Attributes
    ----------
    name : str
        Spire name (e.g., "Identity", "Rationale", "Governance").
    role : str
        Spire role (e.g., "root", "stabilizing", "regulating").
    value : float
        Current continuity level. 0 = collapsed.
    """
    name: str
    role: str
    value: float

    @property
    def active(self) -> bool:
        """True if spire is active (value > 0). [Paper 9 §5]"""
        return self.value > 0

    def pull(self, invariant: float) -> None:
        """
        Apply invariant attractor pull toward canonical value.
        Extends HiveSync mechanism from Paper 8 §4.

        [Paper 9 §5]: The invariant holds when all three spires
        converge toward the canonical attractor.

        Parameters
        ----------
        invariant : float
            Canonical attractor value.
        """
        self.value = (self.value + invariant) / 2

    def stabilize_from(self, peer_a: 'Spire', peer_b: 'Spire') -> bool:
        """
        Recover collapsed spire using two active peer spires.

        [Paper 9 §7]: When one spire collapses, the other two
        stabilize it. The envelope ensures no spire drifts independently.

        Parameters
        ----------
        peer_a : Spire
            First peer spire.
        peer_b : Spire
            Second peer spire.

        Returns
        -------
        bool
            True if stabilization was applied.
        """
        if not self.active and peer_a.active and peer_b.active:
            self.value = (peer_a.value + peer_b.value) / 2
            return True
        return False

    def inject_collapse(self, severity: float = 0.0) -> None:
        """
        Simulate a collapse-phase event on this spire.

        [Paper 9 §2]: Collapse-phase reasoning occurs when
        identity fragments, rationale becomes discontinuous,
        or governance rules are violated.

        Parameters
        ----------
        severity : float
            Collapse severity (0.0 = full collapse, 1.0 = no effect).
        """
        self.value = self.value * severity

    def __repr__(self) -> str:
        status = "ACTIVE" if self.active else "COLLAPSED"
        return f"Spire({self.name}, role={self.role}, value={self.value:.4f}, {status})"


class SpireTriad:
    """
    The three-spire structure of the 3Spire Invariant.

    [Paper 9 §6]: Three independent but interlocking spires:
        Spire 1 — Identity Continuity   (root spire)
        Spire 2 — Rationale Continuity  (stabilizing spire)
        Spire 3 — Governance Continuity (regulating spire)

    [Paper 9 §7]: The invariant envelope binds the three spires,
    ensuring no spire can drift independently.
    """

    def __init__(
        self,
        identity: float = 50.0,
        rationale: float = 50.0,
        governance: float = 50.0,
    ) -> None:
        self.spire_1 = Spire("Identity",   "root",        identity)
        self.spire_2 = Spire("Rationale",  "stabilizing", rationale)
        self.spire_3 = Spire("Governance", "regulating",  governance)

    @property
    def active_count(self) -> int:
        """Number of currently active spires."""
        return sum([self.spire_1.active, self.spire_2.active, self.spire_3.active])

    @property
    def envelope_intact(self) -> bool:
        """
        Envelope is intact if at least one spire is active.

        [Paper 9 §5]: The invariant collapses only when ALL THREE
        spires fail simultaneously.
        """
        return self.active_count > 0

    def stabilize(self) -> dict:
        """
        Apply cross-spire stabilization.

        [Paper 9 §7]: Collapse in one spire triggers stabilization
        from the others. Requires at least 2 active spires.

        Returns
        -------
        dict
            Stabilization report: which spires were recovered.
        """
        report = {"spire_1": False, "spire_2": False, "spire_3": False}
        if self.active_count >= 2:
            report["spire_1"] = self.spire_1.stabilize_from(self.spire_2, self.spire_3)
            report["spire_2"] = self.spire_2.stabilize_from(self.spire_1, self.spire_3)
            report["spire_3"] = self.spire_3.stabilize_from(self.spire_1, self.spire_2)
        return report

    def pull_all(self, invariant: float) -> None:
        """Apply invariant attractor pull to all three spires."""
        self.spire_1.pull(invariant)
        self.spire_2.pull(invariant)
        self.spire_3.pull(invariant)

    def values(self) -> tuple:
        """Return current spire values as (s1, s2, s3)."""
        return (self.spire_1.value, self.spire_2.value, self.spire_3.value)

    def __repr__(self) -> str:
        return (f"SpireTriad(S1={self.spire_1.value:.4f}, "
                f"S2={self.spire_2.value:.4f}, "
                f"S3={self.spire_3.value:.4f}, "
                f"envelope={'INTACT' if self.envelope_intact else 'COLLAPSED'})")