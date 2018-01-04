#!/bin/bash
# 
# Analysis script for villin simulations, using cpptraj.
# Written 17.09.15 by Alex DeGrave
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

# Load all the trajectory segments
#for SEG in $(seq -f "@FORMATCODE@" 1 1 10000); do
#  if [ -e ${MAINDIR}/${SEG}/${SEG}_cut.nc ]; then
#    C0="${C0} trajin ${MAINDIR}/${SEG}/${SEG}_cut.nc parm [default]\n"
#  else
#    break
#  fi
#done
for SEG in $(seq -f "@FORMATCODE@" 1 1 10000); do
  C0="${C0} trajin ${MAINDIR}/${SEG}/${SEG}_cut.nc parm [default]\n"
done

# Calculate minimum distances between residues 1 and 35 and residues 23 and 35

# selections are:

# Carbons
# :23&@%CA  ; side-chain carbons in ring system of NAL (rmin/2 = 1.908 angstroms)
# :35&(@CA|@C9|@CD) ; sidechain carbons in ring system of XAN (rmin/2 = 1.908 angstroms)

# Hydrogens
# :23&@%HA ; side-chain hydrogens in ring system of NAL (rmin/2 = 1.4590 angstroms)
# :35&@%HA ; side-chain hydrogens bonded to aromatic carbon in ring system of XAN (rmin/2 =1.4590 angstroms)
# :35&@HG ; side-chain hydrogen bonded to amide nitrogen in side chain of XAN (rmin/2 = 0.600 angstroms)

# Oxygens
# :35&@%OS ; side-chain ether oxygen in ring system of Xan (rmin/2 = 1.6837 angstroms)
# :35&@O9 ; side-chain carbonyl oxygen in ring system of Xan (rmin/2 = 1.6612 angstroms)

# Nitrogens
# :35&@NG ; side-chain amide nitrogen in Xan (rmin/2 = 1.8240 angstroms)

# We only have two selections for NAL, so iterate over those.
# CA in NAL and CA,CX, or side-chain C in XAN
C0="${C0} nativecontacts    :23&@%CA :35&(@%CA|@C9|@CD) mindist out ttet.dat name 23CA35CAC9CD\n"

# CA in NAL and hydrogens bonded to aromatic carbon in side chain of XAN
C0="${C0} nativecontacts    :23&@%CA :35&@%HA mindist out ttet.dat name 23CA35HA\n"

# CA in NAL and hydrogens bonded to amide nitrogen in side chain of XAN
C0="${C0} nativecontacts    :23&@%CA :35&@HG mindist out ttet.dat name 23CA35HG\n"

# CA in NAL and ether oxygen in side chain of XAN
C0="${C0} nativecontacts    :23&@%CA :35&@%OS mindist out ttet.dat name 23CA35OS\n"

# CA in NAL and carbonyl oxygen in side chain of XAN
C0="${C0} nativecontacts    :23&@%CA :35&@O9 mindist out ttet.dat name 23CA35O9\n"

# CA in NAL and amide nitrogen in side chain of XAN
C0="${C0} nativecontacts    :23&@%CA :35&@NG mindist out ttet.dat name 23CA35NG\n"

# HA in NAL and CA,CX, or side-chain C in XAN
C0="${C0} nativecontacts    :23&@%HA :35&(@%CA|@C9|@CD) mindist out ttet.dat name 23HA35CAC9CD\n"

# HA in NAL and hydrogens bonded to aromatic carbon in side chain of XAN
C0="${C0} nativecontacts    :23&@%HA :35&@%HA mindist out ttet.dat name 23HA35HA\n"

# HA in NAL and hydrogens bonded to amide nitrogen in side chain of XAN
C0="${C0} nativecontacts    :23&@%HA :35&@HG mindist out ttet.dat name 23HA35HG\n"

# HA in NAL and ether oxygen in side chain of XAN
C0="${C0} nativecontacts    :23&@%HA :35&@%OS mindist out ttet.dat name 23HA35OS\n"

# HA in NAL and carbonyl oxygen in side chain of XAN
C0="${C0} nativecontacts    :23&@%HA :35&@O9 mindist out ttet.dat name 23HA35O9\n"

# HA in NAL and amide nitrogen in side chain of XAN
C0="${C0} nativecontacts    :23&@%HA :35&@NG mindist out ttet.dat name 23HA35NG\n"

C0="${C0} run\n"

echo -e "${C0}" | ${CPPTRAJ}
