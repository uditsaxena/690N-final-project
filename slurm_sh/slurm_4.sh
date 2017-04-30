#!/bin/bash
#
#SBATCH --job-name=us_rnn_4
#SBATCH --mem=10000

#SBATCH --output=us_experiment_%A.out
#SBATCH --error=us_experiment_%A.err

# Log what we're running and where.
echo $SLURM_JOBID - `hostname` >> ~/slurm-lstm-jobs.txt

module purge
module load tensorflow/1.0.0
cd /home/usaxena/work/690/project/src/rnn
python babi-rnn.py 4
