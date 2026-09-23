---
task: unsupported
engine: pyscf
error_class: none
outcome: success
n_atoms: 2
method: B3LYP
basis: 6-31G(d)
cores: 1
mode: slurm
---
Result: The HD Gibbs free energy calculation completed successfully on Slurm node8 using one CPU core. The geometry optimization converged in three cycles.

Context: MAESTRO does not currently provide isotope-aware thermochemistry, so a raw PySCF plus geomeTRIC workflow was used. The electronic calculation used two hydrogen nuclei; the thermochemistry applied H and D isotope masses and the HD rotational symmetry number of one at 298.15 K and 1 atm.

Output: `hd_gibbs_results.txt` reports G = -1.179682133244 Eh (-3097.254993 kJ/mol).
