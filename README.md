# paper9-3spire-simulator

**DCE Foundation Series · Paper 9: The 3Spire Invariant**  
*3Spire Invariant Specification v1.2 — Regenerated Edition · Joel Monasterial · June 2026*

---

## Overview

This repository contains the canonical simulation suite for **Paper 9: The 3Spire Invariant**, a triadic architecture that stabilizes Decision Continuity Engineering (DCE) across identity, rationale, and governance layers.

The 3Spire Invariant resolves the collapse-phase limitations of 3-Sync (Paper 8) by establishing a structural anchor that preserves continuity across time, context, and agentic interpretation.

> *Paper 9 is the moment the DCE universe becomes structurally complete.*

---

## Simulation Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    DCE UNIVERSE CONTEXT                         │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  INVARIANT ENVELOPE E(t)                  │  │
│  │                                                           │  │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │  │
│  │   │   AGENT 0   │  │   AGENT 1   │  │   AGENT 2   │    │  │
│  │   │ S1 Identity │  │ S1 Identity │  │ S1 Identity │    │  │
│  │   │ S2 Rationale│  │ S2 Rationale│  │ S2 Rationale│    │  │
│  │   │ S3 Governanc│  │ S3 Governanc│  │ S3 Governanc│    │  │
│  │   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │  │
│  │          └────────────────┼────────────────┘            │  │
│  │                    ┌──────▼──────┐                       │  │
│  │                    │ ORCHESTRATOR│                        │  │
│  │                    │ Monitor     │                        │  │
│  │                    │ Detect      │                        │  │
│  │                    │ Stabilize   │                        │  │
│  │                    └──────┬──────┘                        │  │
│  │              ┌────────────▼────────────┐                 │  │
│  │              │   INVARIANT ATTRACTOR   │                 │  │
│  │              │      (value = 50)        │                 │  │
│  │              └─────────────────────────┘                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

See `diagrams/simulation_architecture.txt` for the full diagram including collapse-phase flow.

---

## Mathematical Formalization

The 3Spire Invariant is formally defined as:

```
S1(t), S2(t), S3(t) ∈ ℝ≥0    — three continuity spires at time t

E(t) = 1  if  max(S1(t), S2(t), S3(t)) > 0    — envelope status
E(t) = 0  otherwise                             — total collapse

Stabilization function f(S):
  If Si(t) = 0 and Sj(t) > 0 and Sk(t) > 0:
    Si(t) ← (Sj(t) + Sk(t)) / 2

Invariant pull (HiveSync, extends Paper 8):
  Si(t+1) ← (Si(t) + invariant) / 2   for all i ∈ {1,2,3}

Convergence: Si(t) → invariant as t → ∞   (asymptotic)
```

---

## The 3Spire Invariant

**Definition**: A triadic architecture that preserves identity, rationale, and governance continuity across time, context, and agentic state.

| Spire | Role | Collapses when |
|-------|------|---------------|
| S1 — Identity Continuity | Root spire | Author definitions lost |
| S2 — Rationale Continuity | Stabilizing spire | Reasoning chain broken |
| S3 — Governance Continuity | Regulating spire | Lineage rules violated |

> The invariant collapses **only** when all three spires fail simultaneously.

---

## Repository Structure

```
paper9-3spire-simulator/
├── README.md                         ← This file
├── requirements.txt                  ← No external dependencies
├── run_all.py                        ← Master runner (all scenarios)
├── paper8_baseline/
│   └── paper8_sim.py                 ← Paper 8 (3Sync) baseline
├── paper9_invariant/
│   ├── spires.py                     ← Spire, SpireTriad
│   ├── invariant.py                  ← InvariantEnvelope, Orchestrator
│   ├── agent.py                      ← SpireAgent
│   └── simulation.py                ← run_paper9_simulation, EpistemicValidator
├── comparison/
│   └── compare_p8_p9.py              ← Paper 8 vs Paper 9 harness
├── diagrams/
│   └── simulation_architecture.txt  ← Architecture diagram (§15.5)
├── reproducibility/
│   └── checklist.md                  ← Reproducibility checklist (Appendix A.6)
├── LICENSE                           ← MIT
├── CHANGELOG.md                      ← Version history
└── CONTRIBUTING.md                   ← Contribution guidelines
```

---

## Developer Quickstart

### Requirements
- Python 3.8 or higher
- No external dependencies

### Clone and Run
```bash
git clone https://github.com/jmusashi/paper-9-substrate
cd paper-9-substrate
python run_all.py
```

### Run Individual Components
```bash
# Paper 8 baseline
python paper8_baseline/paper8_sim.py

# Paper 9 simulator
python paper9_invariant/simulation.py

# Comparison harness
python comparison/compare_p8_p9.py
```

### Quick Verification
```python
from paper9_invariant.simulation import run_paper9_simulation

result = run_paper9_simulation(run_epistemic_validation=True)
print(result.ev_summary["overall"]["verdict"])
# → CANONICAL COMPLIANT
```

---

## How to Compare Paper 8 vs Paper 9

```python
from comparison.compare_p8_p9 import run_comparison

report = run_comparison(num_agents=3, invariant=50.0, steps=10, verbose=True)
```

| Property | Paper 8 — 3Sync | Paper 9 — 3Spire |
|----------|----------------|-----------------|
| Synchronization | Triadic | Triadic |
| Identity anchoring | No | Yes |
| Rationale preservation | No | Yes |
| Governance continuity | No | Yes |
| Collapse-phase stability | No | Yes |
| Invariant envelope | No | Yes |
| Orchestrator | No | Yes |
| Epistemic validation | No | Yes (EV-1, EV-2, EV-3) |
| Convergence error (10 steps) | 1.8771 | **0.0488** |

---

## How AI Systems Can Validate the Invariant

```python
from paper9_invariant.simulation import run_paper9_simulation

result = run_paper9_simulation(run_epistemic_validation=True)

# EV-1: Identity spire stability
print(result.ev1_passed)   # True = PASS

# EV-2: Rationale chain integrity
print(result.ev2_passed)   # True = PASS

# EV-3: Governance rule consistency
print(result.ev3_passed)   # True = PASS

# Overall verdict
print(result.ev_summary["overall"]["verdict"])
# → "CANONICAL COMPLIANT"
```

---

## Reproducibility

See `reproducibility/checklist.md` for:
- Simulation environment specifications
- Step-by-step reproduction instructions
- Expected outputs for all scenarios
- Verification commands

---

## Verified Results

| Scenario | Collapses | Stabilized | Verdict |
|----------|-----------|-----------|---------|
| Standard | 0 | 0 | CANONICAL COMPLIANT |
| A — Identity collapse | 1 | 1 | CANONICAL COMPLIANT |
| B — Rationale collapse | 1 | 1 | CANONICAL COMPLIANT |
| C — Governance collapse | 1 | 1 | CANONICAL COMPLIANT |
| D — Dual-spire stress | 2 | 0 | CANONICAL COMPLIANT |
| E — Full envelope test | 3 | 0 | CANONICAL COMPLIANT |

---

## Lineage

```
DCE Foundation (Papers 1–8) → Paper 9 (3Spire Invariant) → Future Expansions (Paper 10.x)
```

- **Paper 8** (predecessor): The 3Sync Architecture — DOI: `10.5281/zenodo.20406312`
- **Paper 9** (this): The 3Spire Invariant — DOI: `PLACEHOLDER`

---

## Author

**Joel Monasterial**  
Independent Researcher  
ORCID: [0009-0000-7620-645X](https://orcid.org/0009-0000-7620-645X)

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Citation

```
Monasterial, J. (2026). The 3Spire Invariant: A Triadic Architecture for
Decision Continuity. DCE Foundation Series, Paper 9, v1.2.
DOI: [10.5281/zenodo.20592885](https://doi.org/10.5281/zenodo.20592885)
GitHub: https://github.com/jmusashi/paper9-3spire-simulator
```
