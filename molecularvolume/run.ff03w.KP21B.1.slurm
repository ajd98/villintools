#!/bin/bash
#SBATCH --job-name=v.ff03w.KP21B.1.slurm
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --output=slurm.ff03w.KP21B.1.out
#SBATCH --error=slurm.ff03w.KP21B.1.err
#SBATCH --time=36:00:00
#SBATCH --qos=normal
#SBATCH --cluster=smp
#SBATCH --partition=smp
set -e
set -x

MAIN_ANALYSIS_DIR=/gscratch3/lchong/ajd98/villin/analysis/volume2
cd $MAIN_ANALYSIS_DIR

ANALYZE () {
  MAINDIR=$1
  TOPOLOGY=$2

  SIMNAME=$(basename ${MAINDIR})
  if [ ! -d ${MAIN_ANALYSIS_DIR}/${SIMNAME} ]; then
    mkdir ${MAIN_ANALYSIS_DIR}/${SIMNAME}
  fi

  python runparallel.py\
    --maindir $MAINDIR\
    --topology $TOPOLOGY\
    --outdir ${MAIN_ANALYSIS_DIR}/${SIMNAME}/
}


ANALYZE \
  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.1\
  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.1/1_parmed/VILLIN.parm7 &

wait
