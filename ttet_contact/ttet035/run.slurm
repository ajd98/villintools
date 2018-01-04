#!/bin/bash
#SBATCH --job-name=vdw.ttet
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=3
#SBATCH --output=slurm.out
#SBATCH --error=slurm.err
#SBATCH --time=36:00:00
#SBATCH --qos=normal
#SBATCH --cluster=smp
#SBATCH --partition=smp
set -e
set -x

MAIN_ANALYSIS_DIR=/gscratch3/lchong/ajd98/villin/analysis/

ANALYZE () {
  MAINDIR=$1
  TOPOLOGY=$2
  REFERENCE=$3
  
  SIMNAME=$(basename ${MAINDIR})
  if [ ! -d ${MAIN_ANALYSIS_DIR}/${SIMNAME} ]; then
    mkdir ${MAIN_ANALYSIS_DIR}/${SIMNAME}
  fi

  FORMATCODE='%05g'

  cd ${MAIN_ANALYSIS_DIR}/${SIMNAME} || exit 1


  ANALYSIS_TEMPLATE=${MAIN_ANALYSIS_DIR}/ttet035_contact_analysis/vdw.sh

  cat ${ANALYSIS_TEMPLATE}\
    | sed -e "s#\@MAINDIR\@#${MAINDIR}#"\
    | sed -e "s#\@TOPOLOGY\@#${TOPOLOGY}#"\
    | sed -e "s#\@REFERENCE\@#${REFERENCE}#"\
    | sed -e "s#\@FORMATCODE\@#${FORMATCODE}#"\
    > ttet_analysis.sh

  bash ttet_analysis.sh
  python ${MAIN_ANALYSIS_DIR}/ttet_contact_analysis/label_contacts.py
}
################################ ff14sb.KP21B.ttet035 ############################
ANALYZE \
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet035.1\
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet035.1/3_leap/VILLIN.parm7\
  /gscratch3/lchong/ajd98/villin/analysis/reference/VILLIN.pdb &

ANALYZE \
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet035.2\
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet035.2/3_leap/VILLIN.parm7\
  /gscratch3/lchong/ajd98/villin/analysis/reference/VILLIN.pdb &

ANALYZE \
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet035.3\
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet035.3/3_leap/VILLIN.parm7\
  /gscratch3/lchong/ajd98/villin/analysis/reference/VILLIN.pdb &

wait

