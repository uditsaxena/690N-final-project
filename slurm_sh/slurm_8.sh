#!/bin/bash
#
#SBATCH --job-name=us_rnn_8
#SBATCH --mem=10000
#SBATCH --partition=longq
#SBATCH --output=us_experiment_%A.out
#SBATCH --error=us_experiment_%A.err

# Log what we're running and where.
echo $SLURM_JOBID - `hostname` >> ~/slurm-lstm-jobs.txt

module purge
module load tensorflow/1.0.0
cd /mnt/nfs/work1/mccallum/usaxena/programs/python/nlp/src/rnn
python babi-rnn.py 8
