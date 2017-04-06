#!/bin/bash
#
#SBATCH --job-name=us_rnn_lstm
#SBATCH --partition=defq
#SBATCH --time=1-23:00:00
#SBATCH --mem=100000
#SBATCH --output=us_experiment_%A.out
#SBATCH --error=us_experiment_%A.err
#SBATCH --gres=gpu:1

# Log what we're running and where.
echo $SLURM_JOBID - `hostname` >> ~/slurm-lstm-jobs.txt

module purge
module load tensorflow/1.0.0
cd /home/usaxena/work/690/projectsrc/rnn
python babi-rnn.py