"""
paper9_invariant — DCE Foundation Series · Paper 9: The 3Spire Invariant
=========================================================================
3Spire Invariant Specification v1.1
Author: Joel Monasterial · June 2026

Modules
-------
spires      : SpireTriad, Spire — three continuity spires
invariant   : InvariantEnvelope, Orchestrator — envelope enforcement
agent       : SpireAgent — identity-anchored, collapse-phase stable agent
simulation  : run_paper9_simulation, EpistemicValidator, Paper9Result
"""

from paper9_invariant.spires import Spire, SpireTriad
from paper9_invariant.invariant import InvariantEnvelope, Orchestrator, CollapseEvent
from paper9_invariant.agent import SpireAgent
from paper9_invariant.simulation import (
    run_paper9_simulation,
    EpistemicValidator,
    Paper9Result,
)

__all__ = [
    "Spire", "SpireTriad",
    "InvariantEnvelope", "Orchestrator", "CollapseEvent",
    "SpireAgent",
    "run_paper9_simulation", "EpistemicValidator", "Paper9Result",
]