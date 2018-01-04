#!/usr/bin/env python
import numpy


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

class TTETDetect(object):
    def __init__(self, datapath):
        self.datapath = datapath
        self.load_data()
        self._calc()

    def load_data(self):
        self.data_arr = numpy.loadtxt(self.datapath, 
                                      usecols=(3,6,9,12,15,18,21,24,27,30,33,36), 
                                      skiprows=1)

    def _calc(self):
        comparison_arr = [1.908+1.908,
                          1.908+1.4590,
                          1.908+0.600,
                          1.908+1.6837,
                          1.908+1.6612,
                          1.908+1.8240,
                          1.459+1.908,
                          1.459+1.4590,
                          1.459+0.600,
                          1.459+1.6837,
                          1.459+1.6612,
                          1.459+1.8240]
        comparison_arr = numpy.array(comparison_arr)
        check = numpy.empty(self.data_arr.shape[0], dtype=int)
        for i, dists in enumerate(self.data_arr):
            if numpy.any(dists < comparison_arr):
                check[i] = 1 
            else: 
                check[i] = 0 
        numpy.save('ttet_contact',check)
            

if __name__ == "__main__":
    TTETDetect('ttet.dat')
        
