#!/bin/bash
#SBATCH --job-name=hd-gibbs
#SBATCH --nodelist=idle
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --output=hd-gibbs-%j.out
#SBATCH --error=hd-gibbs-%j.err

set -euo pipefail
cd "${SLURM_SUBMIT_DIR}"
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

MAESTRO_ALLOW_RAW=1 maestro-python hd_gibbs.py
