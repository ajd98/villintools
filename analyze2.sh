#!/bin/bash
# 
# Analysis script for villin simulations, using cpptraj.
# Written Apr 24 by Alex DeGrave
#
#

CPPTRAJ="/ihome/lchong/ajd98/apps/amber14/bin/cpptraj"

# replacement fields for sed
MAINDIR=@MAINDIR@
REFERENCE=@REFERENCE@
TOPOLOGY=@TOPOLOGY@

############################ Begin analysis ###########################

# Load the topology
C0="parm ${TOPOLOGY} [default]\n"
C0="${C0} parm ${REFERENCE} [KP21B]\n"

# Load all the trajectory segments
for SEG in $(seq -f "@FORMATCODE@" 1 1 10000); do
  if [ -e ${MAINDIR}/${SEG}/${SEG}_cut.nc ]; then
    C0="${C0} trajin ${MAINDIR}/${SEG}/${SEG}_cut.nc parm [default]\n"
  else
    break
  fi
done

# Calculate minimum distances between residues 1 and 35 and residues 23 and 35
C0="${C0} distance 1-to-35  :1  :35         out 1_to_35_COM_dist.dat \n"
C0="${C0} distance 23-to-35 :23 :35         out 23_to_35_COM_dist.dat \n"
C0="${C0} nativecontacts    :1  :35 mindist out 1_to_35_min_dist.dat \n"
C0="${C0} nativecontacts    :23 :35 mindist out 23_to_35_min_dist.dat \n"

# Calculate RMSD from a reference structure
C0="${C0} reference ${REFERENCE} parm ${REFERENCE}\n"
C0="${C0} rms junk1 :3-9&(@C|@CA|@O|@N) reference \n"
C0="${C0} rms RMSD_to_KP21B :14-34&(@C|@CA|@O|@N)|:35&(@C|@CA|@N) reference nofit out rmsd.align-h1_rmsd-resi14-35-backbone.dat \n"

# Phi angles
C0="$C0 dihedral phi2  :1@C :2@N :2@CA :2@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi3  :2@C :3@N :3@CA :3@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi4  :3@C :4@N :4@CA :4@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi5  :4@C :5@N :5@CA :5@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi6  :5@C :6@N :6@CA :6@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi7  :6@C :7@N :7@CA :7@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi8  :7@C :8@N :8@CA :8@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi9  :8@C :9@N :9@CA :9@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi10 :9@C :10@N :10@CA :10@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi11 :10@C :11@N :11@CA :11@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi12 :11@C :12@N :12@CA :12@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi13 :12@C :13@N :13@CA :13@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi14 :13@C :14@N :14@CA :14@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi15 :14@C :15@N :15@CA :15@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi16 :15@C :16@N :16@CA :16@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi17 :16@C :17@N :17@CA :17@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi18 :17@C :18@N :18@CA :18@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi19 :18@C :19@N :19@CA :19@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi20 :19@C :20@N :20@CA :20@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi21 :20@C :21@N :21@CA :21@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi22 :21@C :22@N :22@CA :22@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi23 :22@C :23@N :23@CA :23@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi24 :23@C :24@N :24@CA :24@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi25 :24@C :25@N :25@CA :25@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi26 :25@C :26@N :26@CA :26@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi27 :26@C :27@N :27@CA :27@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi28 :27@C :28@N :28@CA :28@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi29 :28@C :29@N :29@CA :29@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi30 :29@C :30@N :30@CA :30@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi31 :30@C :31@N :31@CA :31@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi32 :31@C :32@N :32@CA :32@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi33 :32@C :33@N :33@CA :33@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi34 :33@C :34@N :34@CA :34@C"
C0="$C0                out phi.dat \n"
C0="$C0 dihedral phi35 :34@C :35@N :35@CA :35@C"
C0="$C0                out phi.dat \n"

# Psi angles
C0="$C0 dihedral psi1  :1@N :1@CA :1@C :2@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi2  :2@N :2@CA :2@C :3@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi3  :3@N :3@CA :3@C :4@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi4  :4@N :4@CA :4@C :5@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi5  :5@N :5@CA :5@C :6@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi6  :6@N :6@CA :6@C :7@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi7  :7@N :7@CA :7@C :8@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi8  :8@N :8@CA :8@C :9@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi9  :9@N :9@CA :9@C :10@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi10 :10@N :10@CA :10@C :11@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi11 :11@N :11@CA :11@C :12@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi12 :12@N :12@CA :12@C :13@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi13 :13@N :13@CA :13@C :14@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi14 :14@N :14@CA :14@C :15@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi15 :15@N :15@CA :15@C :16@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi16 :16@N :16@CA :16@C :17@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi17 :17@N :17@CA :17@C :18@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi18 :18@N :18@CA :18@C :19@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi19 :19@N :19@CA :19@C :20@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi20 :20@N :20@CA :20@C :21@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi21 :21@N :21@CA :21@C :22@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi22 :22@N :22@CA :22@C :23@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi23 :23@N :23@CA :23@C :24@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi24 :24@N :24@CA :24@C :25@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi25 :25@N :25@CA :25@C :26@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi26 :26@N :26@CA :26@C :27@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi27 :27@N :27@CA :27@C :28@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi28 :28@N :28@CA :28@C :29@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi29 :29@N :29@CA :29@C :30@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi30 :30@N :30@CA :30@C :31@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi31 :31@N :31@CA :31@C :32@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi32 :32@N :32@CA :32@C :33@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi33 :33@N :33@CA :33@C :34@N"
C0="$C0                out psi.dat \n"
C0="$C0 dihedral psi34 :34@N :34@CA :34@C :35@N"
C0="$C0                out psi.dat \n"

#################### Chi angles ########################
# L1
C0="$C0 dihedral 1_chi_1 :1@N :1@CA :1@CB :1@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 1_chi_2 :1@CA :1@CB :1@CG :1@CD1"
C0="$C0                out chi.dat \n"

# S2 - is there a chi2?
C0="$C0 dihedral 2_chi_1 :2@N :2@CA :2@CB :2@OG"
C0="$C0                out chi.dat \n"

# D3
C0="$C0 dihedral 3_chi_1 :3@N :3@CA :3@CB :3@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 3_chi_2 :3@CA :3@CB :3@CG :3@OD1"
C0="$C0                out chi.dat \n"

# E4
C0="$C0 dihedral 4_chi_1 :4@N :4@CA :4@CB :4@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 4_chi_2 :4@CA :4@CB :4@CG :4@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 4_chi_3 :4@CB :4@CG :4@CD :4@OE1"
C0="$C0                out chi.dat \n"

# D5
C0="$C0 dihedral 5_chi_1 :5@N :5@CA :5@CB :5@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 5_chi_2 :5@CA :5@CB :5@CG :5@OD1"
C0="$C0                out chi.dat \n"

# F6
C0="$C0 dihedral 6_chi_1 :6@N :6@CA :6@CB :6@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 6_chi_2 :6@CA :6@CB :6@CG :6@CD1"
C0="$C0                out chi.dat \n"

# K7
C0="$C0 dihedral 7_chi_1 :7@N :7@CA :7@CB :7@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 7_chi_2 :7@CA :7@CB :7@CG :7@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 7_chi_3 :7@CB :7@CG :7@CD :7@CE"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 7_chi_4 :7@CG :7@CD :7@CE :7@NZ"
C0="$C0                out chi.dat \n"

# A8 - nothing!

# V9
C0="$C0 dihedral 9_chi_1 :9@N :9@CA :9@CB :9@CG1"
C0="$C0                out chi.dat \n"

# F10
C0="$C0 dihedral 10_chi_1 :10@N :10@CA :10@CB :10@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 10_chi_2 :10@CA :10@CB :10@CG :10@CD1"
C0="$C0                out chi.dat \n"

# G11 - nothing!

# M12
C0="$C0 dihedral 12_chi_1 :12@N :12@CA :12@CB :12@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 12_chi_2 :12@CA :12@CB :12@CG :12@SD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 12_chi_3 :12@CB :12@CG :12@SD :12@CE"
C0="$C0                out chi.dat \n"

# T13
C0="$C0 dihedral 13_chi_1 :13@N :13@CA :13@CB :13@OG1"
C0="$C0                out chi.dat \n"

# R14
C0="$C0 dihedral 14_chi_1 :14@N :14@CA :14@CB :14@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 14_chi_2 :14@CA :14@CB :14@CG :14@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 14_chi_3 :14@CB :14@CG :14@CD :14@NE"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 14_chi_4 :14@CG :14@CD :14@NE :14@CZ"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 14_chi_5 :14@CD :14@NE :14@CZ :14@NH1"
C0="$C0                out chi.dat \n"

# S15
C0="$C0 dihedral 15_chi_1 :15@N :15@CA :15@CB :15@OG"
C0="$C0                out chi.dat \n"

# A16 - nothing!

# F17
C0="$C0 dihedral 17_chi_1 :17@N :17@CA :17@CB :17@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 17_chi_2 :17@CA :17@CB :17@CG :17@CD1"
C0="$C0                out chi.dat \n"

# A18 - nothing!

# N19
C0="$C0 dihedral 19_chi_1 :19@N :19@CA :19@CB :19@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 19_chi_2 :19@CA :19@CB :19@CG :19@OD1"
C0="$C0                out chi.dat \n"

# L20
C0="$C0 dihedral 20_chi_1 :20@N :20@CA :20@CB :20@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 20_chi_2 :20@CA :20@CB :20@CG :20@CD1"
C0="$C0                out chi.dat \n"

# P21
C0="$C0 dihedral 21_chi_1 :21@N :21@CA :21@CB :21@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 21_chi_2 :21@CA :21@CB :21@CG :21@CD"
C0="$C0                out chi.dat \n"

# L22
C0="$C0 dihedral 22_chi_1 :22@N :22@CA :22@CB :22@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 22_chi_2 :22@CA :22@CB :22@CG :22@CD1"
C0="$C0                out chi.dat \n"

# W23
C0="$C0 dihedral 23_chi_1 :23@N :23@CA :23@CB :23@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 23_chi_2 :23@CA :23@CB :23@CG :23@CD1"
C0="$C0                out chi.dat \n"

# K24
C0="$C0 dihedral 24_chi_1 :24@N :24@CA :24@CB :24@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 24_chi_2 :24@CA :24@CB :24@CG :24@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 24_chi_3 :24@CB :24@CG :24@CD :24@CE"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 24_chi_4 :24@CG :24@CD :24@CE :24@NZ"
C0="$C0                out chi.dat \n"

# Q25
C0="$C0 dihedral 25_chi_1 :25@N :25@CA :25@CB :25@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 25_chi_2 :25@CA :25@CB :25@CG :25@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 25_chi_3 :25@CB :25@CG :25@CD :25@OE1"
C0="$C0                out chi.dat \n"

# Q26
C0="$C0 dihedral 26_chi_1 :26@N :26@CA :26@CB :26@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 26_chi_2 :26@CA :26@CB :26@CG :26@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 26_chi_3 :26@CB :26@CG :26@CD :26@OE1"
C0="$C0                out chi.dat \n"

# N27
C0="$C0 dihedral 27_chi_1 :27@N :27@CA :27@CB :27@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 27_chi_2 :27@CA :27@CB :27@CG :27@OD1"
C0="$C0                out chi.dat \n"

# L28
C0="$C0 dihedral 28_chi_1 :28@N :28@CA :28@CB :28@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 28_chi_2 :28@CA :28@CB :28@CG :28@CD1"
C0="$C0                out chi.dat \n"

# K29
C0="$C0 dihedral 29_chi_1 :29@N :29@CA :29@CB :29@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 29_chi_2 :29@CA :29@CB :29@CG :29@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 29_chi_3 :29@CB :29@CG :29@CD :29@CE"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 29_chi_4 :29@CG :29@CD :29@CE :29@NZ"
C0="$C0                out chi.dat \n"

# K30
C0="$C0 dihedral 30_chi_1 :30@N :30@CA :30@CB :30@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 30_chi_2 :30@CA :30@CB :30@CG :30@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 30_chi_3 :30@CB :30@CG :30@CD :30@CE"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 30_chi_4 :30@CG :30@CD :30@CE :30@NZ"
C0="$C0                out chi.dat \n"

# E31
C0="$C0 dihedral 31_chi_1 :31@N :31@CA :31@CB :31@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 31_chi_2 :31@CA :31@CB :31@CG :31@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 31_chi_3 :31@CB :31@CG :31@CD :31@OE1"
C0="$C0                out chi.dat \n"

# K32
C0="$C0 dihedral 32_chi_1 :32@N :32@CA :32@CB :32@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 32_chi_2 :32@CA :32@CB :32@CG :32@CD"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 32_chi_3 :32@CB :32@CG :32@CD :32@CE"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 32_chi_4 :32@CG :32@CD :32@CE :32@NZ"
C0="$C0                out chi.dat \n"

# G33 - nothing

# L34
C0="$C0 dihedral 34_chi_1 :34@N :34@CA :34@CB :34@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 34_chi_2 :34@CA :34@CB :34@CG :34@CD1"
C0="$C0                out chi.dat \n"

# F35
C0="$C0 dihedral 35_chi_1 :35@N :35@CA :35@CB :35@CG"
C0="$C0                out chi.dat \n"
C0="$C0 dihedral 35_chi_2 :35@CA :35@CB :35@CG :35@CD1"
C0="$C0                out chi.dat \n"

# Run the analysis
C0="${C0} run \n"

echo -e "${C0}" | ${CPPTRAJ}
