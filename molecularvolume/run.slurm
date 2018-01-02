#!/bin/bash
#SBATCH --job-name=volumes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err
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


######################### ff14sb.xray #############################
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.xray.1\
#  /gscratch3/lchong/ajd98/villin/ff14sb.xray.1/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.xray.2\
#  /gscratch3/lchong/ajd98/villin/ff14sb.xray.2/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.xray.3\
#  /gscratch3/lchong/ajd98/villin/ff14sb.xray.3/1_leap/VILLIN.parm7 &
#
############################ ff14sb.nmr #############################
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.nmr.1\
#  /gscratch3/lchong/ajd98/villin/ff14sb.nmr.1/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.nmr.2\
#  /gscratch3/lchong/ajd98/villin/ff14sb.nmr.2/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.nmr.3\
#  /gscratch3/lchong/ajd98/villin/ff14sb.nmr.3/1_leap/VILLIN.parm7 &
#
############################ ff14sb.KLP21D #############################
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KLP21D.1\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KLP21D.1/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KLP21D.2\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KLP21D.2/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KLP21D.3\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KLP21D.3/1_leap/VILLIN.parm7 &
#
######################### ff14sb.KP21B #########################################
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.1\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.1/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.2\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.2/1_leap/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.3\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.3/1_leap/VILLIN.parm7 &
#
#wait
#
################################ ff14sb.KP21B.ttet ############################
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.1\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.1/8_leap2/VILLIN.parm7
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.2\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.2/8_leap2/VILLIN.parm7
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.3\
#  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.3/8_leap2/VILLIN.parm7
#
########################### ff03w.xray #############################
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.xray.1\
#  /gscratch3/lchong/ajd98/villin/ff03w.xray.1/1_parmed/VILLIN_waters_edited.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.xray.2\
#  /gscratch3/lchong/ajd98/villin/ff03w.xray.2/1_parmed/VILLIN_waters_edited.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.xray.3\
#  /gscratch3/lchong/ajd98/villin/ff03w.xray.3/1_parmed/VILLIN_waters_edited.parm7 &
#
########################## ff03w.nmr #############################
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.nmr.1\
#  /gscratch3/lchong/ajd98/villin/ff03w.nmr.1/1_parmed/VILLIN_waters_edited.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.nmr.2\
#  /gscratch3/lchong/ajd98/villin/ff03w.nmr.2/1_parmed/VILLIN_waters_edited.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.nmr.3\
#  /gscratch3/lchong/ajd98/villin/ff03w.nmr.3/1_parmed/VILLIN_waters_edited.parm7 &
#
########################## ff03w.KLP21D #############################
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.KLP21D.1\
#  /gscratch3/lchong/ajd98/villin/ff03w.KLP21D.1/1_parmed/VILLIN_waters_edited.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.KLP21D.2\
#  /gscratch3/lchong/ajd98/villin/ff03w.KLP21D.2/1_parmed/VILLIN_waters_edited.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.KLP21D.3\
#  /gscratch3/lchong/ajd98/villin/ff03w.KLP21D.3/1_parmed/VILLIN_waters_edited.parm7 &
#
########################## ff03w.KP21B #########################################
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.1\
#  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.1/1_parmed/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.2\
#  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.2/1_parmed/VILLIN.parm7 &
#
#ANALYZE \
#  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.3\
#  /gscratch3/lchong/ajd98/villin/ff03w.KP21B.3/1_parmed/VILLIN.parm7 &

wait
