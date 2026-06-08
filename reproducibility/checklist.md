# Reproducibility Checklist
## DCE Foundation Series · Paper 9: The 3Spire Invariant (v1.2)

**Author**: Joel Monasterial  
**ORCID**: 0009-0000-7620-645X  
**DOI**: PLACEHOLDER  
**Date**: June 2026  

---

## Simulation Environment

| Item | Specification |
|------|--------------|
| **Python version** | 3.8 or higher (tested on 3.8, 3.10, 3.12) |
| **External dependencies** | None (standard library only) |
| **Operating system** | Any (Linux, macOS, Windows) |
| **Hardware** | Any — no GPU or special hardware required |
| **Memory** | < 50 MB for all scenarios |
| **Runtime** | < 5 seconds for full suite |

---

## Steps to Reproduce

### Step 1: Clone the Repository
```bash
git clone https://github.com/jmusashi/paper9-3spire-simulator.git
cd paper9-3spire-simulator
```

### Step 2: Verify Python Version
```bash
python --version
# Expected: Python 3.8.x or higher
```

### Step 3: Run All Simulations
```bash
python run_all.py
```

### Step 4: Run Individual Components
```bash
# Paper 8 baseline only
python paper8_baseline/paper8_sim.py

# Paper 9 simulator only
python paper9_invariant/simulation.py

# Comparison harness only
python comparison/compare_p8_p9.py
```

### Step 5: Run Epistemic Validation
```python
from paper9_invariant.simulation import run_paper9_simulation

result = run_paper9_simulation(run_epistemic_validation=True)
print(result.ev_summary["overall"]["verdict"])
# Expected: CANONICAL COMPLIANT
```

---

## Expected Outputs

### Paper 8 Baseline (10 steps, 3 agents, invariant=50)

| Step | Agent 0 | Agent 1 | Agent 2 |
|------|---------|---------|---------|
| t=1  | 25.000  | 30.000  | 35.000  |
| t=5  | 42.090  | 43.672  | 45.254  |
| t=10 | 48.123  | 48.498  | 48.874  |

**Final convergence error (max)**: 1.8771

### Paper 9 Standard Simulation (10 steps, 3 agents, invariant=50)

| Step | Agent 0 (S1,S2,S3) | Agent 1 (S1,S2,S3) | Agent 2 (S1,S2,S3) |
|------|-------------------|-------------------|-------------------|
| t=1  | (25.00,25.00,25.00) | (30.00,29.00,28.00) | (35.00,33.00,31.00) |
| t=5  | (48.44,48.44,48.44) | (48.75,48.69,48.62) | (49.06,48.94,48.81) |
| t=10 | (49.95,49.95,49.95) | (49.96,49.96,49.96) | (49.97,49.97,49.96) |

**Final convergence error (max)**: 0.0488

### Epistemic Validation Results

| Criterion | Expected Result |
|-----------|----------------|
| EV-1 (Identity stability) | PASS |
| EV-2 (Rationale integrity) | PASS |
| EV-3 (Governance consistency) | PASS |
| Overall verdict | CANONICAL COMPLIANT |

### Collapse Scenarios (Paper 9 §14)

| Scenario | Collapses | Stabilized | Expected Verdict |
|----------|-----------|-----------|-----------------|
| A — Identity collapse | 1 | 1 | CANONICAL COMPLIANT |
| B — Rationale collapse | 1 | 1 | CANONICAL COMPLIANT |
| C — Governance collapse | 1 | 1 | CANONICAL COMPLIANT |
| D — Dual-spire stress | 2 | 0 | CANONICAL COMPLIANT |
| E — Full envelope test | 3 | 0 | CANONICAL COMPLIANT |

---

## Verification Commands

```bash
# Quick verification (Python one-liner)
python -c "
from paper9_invariant.simulation import run_paper9_simulation
r = run_paper9_simulation()
verdict = r.ev_summary['overall']['verdict']
print(f'Verdict: {verdict}')
assert verdict == 'CANONICAL COMPLIANT', 'Verification failed!'
print('Verification PASSED.')
"
```

Expected output:
```
Verdict: CANONICAL COMPLIANT
Verification PASSED.
```

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| `ModuleNotFoundError` | Run from repo root: `cd paper9-3spire-simulator && python run_all.py` |
| `Python 3.7 or lower` | Upgrade to Python 3.8+ (uses `from __future__ import annotations`) |
| Different numeric results | Floating-point differences < 0.001 are acceptable |
| `NON-COMPLIANT` verdict | Check Python version; ensure no file modifications |

---

## Citation

If you use this simulation suite, please cite:

```
Monasterial, J. (2026). Paper 9: The 3Spire Invariant — A Triadic Architecture
for Decision Continuity. DCE Foundation Series, v1.2 (Regenerated Edition).
DOI: PLACEHOLDER
GitHub: https://github.com/jmusashi/paper9-3spire-simulator
```

---

*This checklist is part of the canonical reproducibility package for Paper 9.*  
*DCE Foundation Series · 3Spire Invariant Specification v1.2 · Joel Monasterial · June 2026*