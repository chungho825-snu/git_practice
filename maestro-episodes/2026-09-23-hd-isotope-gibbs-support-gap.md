---
task: unsupported
engine: none
error_class: support_gap
outcome: support_gap
---
Symptom: The requested HD Gibbs free energy cannot be represented by ThermoTask because its SystemQM geometry parser rejects the deuterium element label `D`.

Attempts: Queried MAESTRO for free energy, thermochemistry, Gibbs, and isotope capabilities. ThermoTask produces `gibbs_free_energy`, while IsotopeShiftTask produces only `isotope_frequencies` from a Hessian after mass substitution.

Result: No MAESTRO task found that combines isotopic mass substitution with thermochemistry to produce the Gibbs free energy of HD. No calculation was submitted, preventing an incorrect H2 result from being reported as HD.

Context: Requested reaction context was H2 + D2 -> 2 HD at the default thermochemistry conditions, using DFT B3LYP/6-31G(d), PySCF plus Geometric, Slurm on idle with one core.
