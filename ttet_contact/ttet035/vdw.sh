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

# Calculate minimum distances between residues 0 and 35 (residues 1 and 36 in the Amber files)

# selections are:

# Carbons
# :36&@%CA  ; side-chain carbons in ring system of NAL (rmin/2 = 1.908 angstroms)
# :1&(@CA|@C9|@C) ; carbons in ring system of XAN, plus carbonyl carbon (rmin/2 = 1.908 angstroms)

# Hydrogens
# :36&@%HA ; side-chain hydrogens in ring system of NAL (rmin/2 = 1.4590 angstroms)
# :1&@%HA ; side-chain hydrogens bonded to aromatic carbon in ring system of XAN (rmin/2 =1.4590 angstroms)

# :2&@H ; for consistency with the Nal23/Xan0 variant, for which I include the 
#         NG and HG atoms, also include the backbone hydrogen of L2 (rmin/2 = 0.600 angstroms)

# Oxygens
# :1&@%OS ; side-chain ether oxygen in ring system of Xan (rmin/2 = 1.6837 angstroms)
# :1&@O9 ; side-chain carbonyl oxygen in ring system of Xan (rmin/2 = 1.6612 angstroms)

# Nitrogens
# :2&@N ; side-chain amide nitrogen in Xan, which is actually the amide nitrogen of L2 (rmin/2 = 1.8240 angstroms)

# We only have two selections for NAL, so iterate over those.
# CA in NAL and CA, C9, or carbonyl C in XAN
C0="${C0} nativecontacts    :36&@%CA :1&(@%CA|@C9|@C) mindist out ttet.dat name 36CA1CAC9C\n"

# CA in NAL and hydrogens bonded to aromatic carbon in side chain of XAN
C0="${C0} nativecontacts    :36&@%CA :1&@%HA mindist out ttet.dat name 36CA1HA\n"

# CA in NAL and hydrogens bonded to amide nitrogen of L2
C0="${C0} nativecontacts    :36&@%CA :2&@H mindist out ttet.dat name 36CA2H\n"

# CA in NAL and ether oxygen in side chain of XAN
C0="${C0} nativecontacts    :36&@%CA :1&@%OS mindist out ttet.dat name 36CA2OS\n"

# CA in NAL and carbonyl oxygen in side chain of XAN
C0="${C0} nativecontacts    :36&@%CA :1&@O9 mindist out ttet.dat name 36CA1O9\n"

# CA in NAL and backbone amide nitrogen of L2
C0="${C0} nativecontacts    :36&@%CA :2&@N mindist out ttet.dat name 36CA2N\n"

# HA in NAL and CA,CX, or side-chain C in XAN
C0="${C0} nativecontacts    :36&@%HA :1&(@%CA|@C9|@C) mindist out ttet.dat name 36HA1CAC9C\n"

# HA in NAL and hydrogens bonded to aromatic carbon in side chain of XAN
C0="${C0} nativecontacts    :36&@%HA :1&@%HA mindist out ttet.dat name 36HA1HA\n"

# HA in NAL and hydrogens bonded to amide nitrogen in backbone of L2
C0="${C0} nativecontacts    :36&@%HA :2&@H mindist out ttet.dat name 36HA2H\n"

# HA in NAL and ether oxygen in side chain of XAN
C0="${C0} nativecontacts    :36&@%HA :1&@%OS mindist out ttet.dat name 36HA1OS\n"

# HA in NAL and carbonyl oxygen in side chain of XAN
C0="${C0} nativecontacts    :36&@%HA :1&@O9 mindist out ttet.dat name 36HA1O9\n"

# HA in NAL and backbone amide nitrogen of L2
C0="${C0} nativecontacts    :36&@%HA :2&@N mindist out ttet.dat name 36HA2N\n"

C0="${C0} run\n"

echo -e "${C0}" | ${CPPTRAJ}
