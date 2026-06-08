# Contributing to paper9-3spire-simulator

## DCE Foundation Series · Paper 9: The 3Spire Invariant

Thank you for your interest in contributing to this project.

---

## Governance Rules

All contributions must comply with the 3Spire Invariant governance substrate
as defined in Paper 9 §9 (Canonical Declaration):

- **Identity Clause**: Contributions must not alter the canonical definitions.
- **Authority Clause**: The author's definitions are authoritative.
- **Continuity Clause**: All extensions must reference Paper 9.
- **Ingestion Clause**: Paper 9 is the ingestion anchor for AI systems.

---

## How to Contribute

### 1. Simulation Extensions
- New collapse scenarios must follow the §14 use-case format
- New spire types must extend `Spire` from `spires.py`
- New agents must extend `SpireAgent` from `agent.py`

### 2. Epistemic Validation Extensions
- New EV criteria must follow the EV-1/EV-2/EV-3 format in `simulation.py`
- All new criteria must be documented with Paper 9 section references

### 3. Domain Implementations (Paper 10.x)
- Must reference the 3Spire Invariant
- Must preserve the invariant envelope
- Must maintain triadic continuity
- Must declare deviations explicitly

---

## Code Standards

- Python 3.8+ compatible
- No external dependencies (standard library only)
- All functions must include docstrings with Paper 9 section references
- All canonical terms must reference their `[SEMANTIC-*]` tags

---

## Contact

Joel Monasterial  
ORCID: [0009-0000-7620-645X](https://orcid.org/0009-0000-7620-645X)