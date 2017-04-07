#!/bin/bash
#
#SBATCH --job-name=us_rnn_lstm
#SBATCH --mem=10000
#SBATCH --output=us_experiment_%A.out
#SBATCH --error=us_experiment_%A.err
#SBATCH --gres=gpu:1

# Log what we're running and where.
echo $SLURM_JOBID - `hostname` >> ~/slurm-lstm-jobs.txt

module purge
module load tensorflow/1.0.0
cd /mnt/nfs/work1/mccallum/usaxena/nlp/src/rnn
python babi-rnn.py 2
