"""Compute the 298.15 K, 1 atm Gibbs free energy of HD.

MAESTRO currently supports isotope-shifted frequencies but not isotope-aware
thermochemistry.  This PySCF calculation uses the H2 electronic potential,
then applies the physical H and D nuclear masses to the vibrational,
translational, and rotational thermochemistry of HD.
"""

from pathlib import Path

import numpy as np
from pyscf import dft, gto
from pyscf.geomopt.geometric_solver import optimize
from pyscf.hessian import thermo


TEMPERATURE_K = 298.15
PRESSURE_PA = 101_325.0
H_MASS_U = 1.00782503223
D_MASS_U = 2.01410177812
HARTREE_TO_KJMOL = 2625.49962


def main() -> None:
    xyz_lines = Path("hd_reference.xyz").read_text().splitlines()
    molecule = gto.M(
        atom="\n".join(xyz_lines[2:]),
        basis="6-31G(d)",
        charge=0,
        spin=0,
        unit="Angstrom",
    )
    mean_field = dft.RKS(molecule)
    mean_field.xc = "B3LYP"
    mean_field.grids.level = 3

    optimized_molecule = optimize(mean_field, maxsteps=100)
    mean_field = dft.RKS(optimized_molecule)
    mean_field.xc = "B3LYP"
    mean_field.grids.level = 3
    mean_field.kernel()

    hessian = mean_field.Hessian().kernel()
    isotope_masses = np.array([H_MASS_U, D_MASS_U])
    harmonic = thermo.harmonic_analysis(
        optimized_molecule, hessian, mass=isotope_masses
    )

    # PySCF infers a homonuclear symmetry number (2) from two H labels.
    # HD is heteronuclear, so sigma = 1.  Override only while assembling
    # the thermal partition functions, and supply the isotope masses there too.
    original_mass_list = optimized_molecule.atom_mass_list
    original_symmetry_number = thermo.rotational_symmetry_number
    optimized_molecule.atom_mass_list = lambda isotope_avg=True: isotope_masses
    thermo.rotational_symmetry_number = lambda mol: 1
    try:
        thermal = thermo.thermo(
            mean_field,
            harmonic["freq_au"],
            temperature=TEMPERATURE_K,
            pressure=PRESSURE_PA,
        )
    finally:
        optimized_molecule.atom_mass_list = original_mass_list
        thermo.rotational_symmetry_number = original_symmetry_number

    gibbs_hartree = thermal["G_tot"][0]
    output = Path("hd_gibbs_results.txt")
    output.write_text(
        "HD Gibbs free energy\n"
        f"method: B3LYP/6-31G(d)\n"
        f"temperature: {TEMPERATURE_K:.2f} K\n"
        "pressure: 1 atm\n"
        f"G: {gibbs_hartree:.12f} Eh\n"
        f"G: {gibbs_hartree * HARTREE_TO_KJMOL:.6f} kJ/mol\n"
    )
    print(output.read_text(), end="")


if __name__ == "__main__":
    main()
