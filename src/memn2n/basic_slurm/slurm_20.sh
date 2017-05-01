#!/bin/bash
#
#SBATCH --job-name=us_memn2nb_20
#SBATCH --mem=10000
#SBATCH --partition=titanx-long
#SBATCH --output=us_experiment_%A.out
#SBATCH --error=us_experiment_%A.err

# Log what we're running and where.
echo $SLURM_JOBID - `hostname` >> ~/slurm-lstm-jobs.txt

module purge
module load tensorflow/1.0.0
cd /home/usaxena/work/690/project/src/memn2n
python memn2n_basic.py 20
