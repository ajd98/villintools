#!/bin/bash
#PBS -N villin.analysis
#PBS -o analysis.out
#PBS -e analysis.err
#PBS -l nodes=1:ppn=1
#PBS -l walltime=2:00:00:00
#PBS -q dist_amd
#PBS -V
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


  ANALYSIS_TEMPLATE=${MAIN_ANALYSIS_DIR}/ttet_contact_analysis/vdw.sh

  cat ${ANALYSIS_TEMPLATE}\
    | sed -e "s#\@MAINDIR\@#${MAINDIR}#"\
    | sed -e "s#\@TOPOLOGY\@#${TOPOLOGY}#"\
    | sed -e "s#\@REFERENCE\@#${REFERENCE}#"\
    | sed -e "s#\@FORMATCODE\@#${FORMATCODE}#"\
    > ttet_analysis.sh

  bash ttet_analysis.sh
  python ${MAIN_ANALYSIS_DIR}/ttet_contact_analysis/check_contact.py
}
################################ ff14sb.KP21B.ttet ############################
ANALYZE \
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.1\
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.1/8_leap2/VILLIN.parm7\
  /gscratch3/lchong/ajd98/villin/analysis/reference/VILLIN.pdb

ANALYZE \
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.2\
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.2/8_leap2/VILLIN.parm7\
  /gscratch3/lchong/ajd98/villin/analysis/reference/VILLIN.pdb

ANALYZE \
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.3\
  /gscratch3/lchong/ajd98/villin/ff14sb.KP21B.ttet.3/8_leap2/VILLIN.parm7\
  /gscratch3/lchong/ajd98/villin/analysis/reference/VILLIN.pdb

