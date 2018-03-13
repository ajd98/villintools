#!/usr/bin/env python
import os
import numpy

class DihedralAnalysis(object):
    def __init__(self, simname):
        '''
        statefiles: (iteratable) strings denoting paths to .npy files describing
            simulation states.
        '''
        self.simname = simname
        self.generate_script()

    def get_parmpath(self, simname):
        '''
        Return path to topology file for simulation
        '''
        simdir = self.get_simdir(simname)
        return os.path.join(simdir, 'TOPOLOGY', 'solute.VILLIN.parm7')
            
    def get_simdir(self, simname):
        maindir = self.get_maindir(simname)
        subdir = simname[:-2]
        subsubdir = simname
        return os.path.join(maindir, subdir, subsubdir)

    def get_maindir(self, simname):
        if 'ttet035' in simname:
            maindir = '/mnt/NAS4/villin/'
        else:
            maindir = '/mnt/NAS2/VILLIN/'
        return maindir

    def get_trajpath(self, simname, iseg):
        simdir = self.get_simdir(simname)
        fmtstr = "{:05d}"
        return os.path.join(simdir, fmtstr.format(iseg), 
                            "{:s}_solute.nc".format(fmtstr.format(iseg)))

    def generate_script(self):
        FRAMES_PER_SEGMENT = 1000
        NSEGMENTS=10000
        # Collect structures in each state
        scriptlines = []
        parmpath = self.get_parmpath(sim)
        scriptlines.append("parm {:s}\n".format(parmpath))
        for iseg in xrange(1, NSEGMENTS+1):
            segmentpath = self.get_trajpath(self.simname, iseg)
            scriptlines.append('trajin {:s}\n'.format(segmentpath))
        analysislines = '''
dihedral phi2  :1@C :2@N :2@CA :2@C
               out phi.dat 
dihedral phi3  :2@C :3@N :3@CA :3@C
               out phi.dat 
dihedral phi4  :3@C :4@N :4@CA :4@C
               out phi.dat 
dihedral phi5  :4@C :5@N :5@CA :5@C
               out phi.dat 
dihedral phi6  :5@C :6@N :6@CA :6@C
               out phi.dat 
dihedral phi7  :6@C :7@N :7@CA :7@C
               out phi.dat 
dihedral phi8  :7@C :8@N :8@CA :8@C
               out phi.dat 
dihedral phi9  :8@C :9@N :9@CA :9@C
               out phi.dat 
dihedral phi10 :9@C :10@N :10@CA :10@C
               out phi.dat 
dihedral phi11 :10@C :11@N :11@CA :11@C
               out phi.dat 
dihedral phi12 :11@C :12@N :12@CA :12@C
               out phi.dat 
dihedral phi13 :12@C :13@N :13@CA :13@C
               out phi.dat 
dihedral phi14 :13@C :14@N :14@CA :14@C
               out phi.dat 
dihedral phi15 :14@C :15@N :15@CA :15@C
               out phi.dat 
dihedral phi16 :15@C :16@N :16@CA :16@C
               out phi.dat 
dihedral phi17 :16@C :17@N :17@CA :17@C
               out phi.dat 
dihedral phi18 :17@C :18@N :18@CA :18@C
               out phi.dat 
dihedral phi19 :18@C :19@N :19@CA :19@C
               out phi.dat 
dihedral phi20 :19@C :20@N :20@CA :20@C
               out phi.dat 
dihedral phi21 :20@C :21@N :21@CA :21@C
               out phi.dat 
dihedral phi22 :21@C :22@N :22@CA :22@C
               out phi.dat 
dihedral phi23 :22@C :23@N :23@CA :23@C
               out phi.dat 
dihedral phi24 :23@C :24@N :24@CA :24@C
               out phi.dat 
dihedral phi25 :24@C :25@N :25@CA :25@C
               out phi.dat 
dihedral phi26 :25@C :26@N :26@CA :26@C
               out phi.dat 
dihedral phi27 :26@C :27@N :27@CA :27@C
               out phi.dat 
dihedral phi28 :27@C :28@N :28@CA :28@C
               out phi.dat 
dihedral phi29 :28@C :29@N :29@CA :29@C
               out phi.dat 
dihedral phi30 :29@C :30@N :30@CA :30@C
               out phi.dat 
dihedral phi31 :30@C :31@N :31@CA :31@C
               out phi.dat 
dihedral phi32 :31@C :32@N :32@CA :32@C
               out phi.dat 
dihedral phi33 :32@C :33@N :33@CA :33@C
               out phi.dat 
dihedral phi34 :33@C :34@N :34@CA :34@C
               out phi.dat 
dihedral phi35 :34@C :35@N :35@CA :35@C
               out phi.dat 

dihedral psi1  :1@N :1@CA :1@C :2@N
               out psi.dat 
dihedral psi2  :2@N :2@CA :2@C :3@N
               out psi.dat 
dihedral psi3  :3@N :3@CA :3@C :4@N
               out psi.dat 
dihedral psi4  :4@N :4@CA :4@C :5@N
               out psi.dat 
dihedral psi5  :5@N :5@CA :5@C :6@N
               out psi.dat 
dihedral psi6  :6@N :6@CA :6@C :7@N
               out psi.dat 
dihedral psi7  :7@N :7@CA :7@C :8@N
               out psi.dat 
dihedral psi8  :8@N :8@CA :8@C :9@N
               out psi.dat 
dihedral psi9  :9@N :9@CA :9@C :10@N
               out psi.dat 
dihedral psi10 :10@N :10@CA :10@C :11@N
               out psi.dat 
dihedral psi11 :11@N :11@CA :11@C :12@N
               out psi.dat 
dihedral psi12 :12@N :12@CA :12@C :13@N
               out psi.dat 
dihedral psi13 :13@N :13@CA :13@C :14@N
               out psi.dat 
dihedral psi14 :14@N :14@CA :14@C :15@N
               out psi.dat 
dihedral psi15 :15@N :15@CA :15@C :16@N
               out psi.dat 
dihedral psi16 :16@N :16@CA :16@C :17@N
               out psi.dat 
dihedral psi17 :17@N :17@CA :17@C :18@N
               out psi.dat 
dihedral psi18 :18@N :18@CA :18@C :19@N
               out psi.dat 
dihedral psi19 :19@N :19@CA :19@C :20@N
               out psi.dat 
dihedral psi20 :20@N :20@CA :20@C :21@N
               out psi.dat 
dihedral psi21 :21@N :21@CA :21@C :22@N
               out psi.dat 
dihedral psi22 :22@N :22@CA :22@C :23@N
               out psi.dat 
dihedral psi23 :23@N :23@CA :23@C :24@N
               out psi.dat 
dihedral psi24 :24@N :24@CA :24@C :25@N
               out psi.dat 
dihedral psi25 :25@N :25@CA :25@C :26@N
               out psi.dat 
dihedral psi26 :26@N :26@CA :26@C :27@N
               out psi.dat 
dihedral psi27 :27@N :27@CA :27@C :28@N
               out psi.dat 
dihedral psi28 :28@N :28@CA :28@C :29@N
               out psi.dat 
dihedral psi29 :29@N :29@CA :29@C :30@N
               out psi.dat 
dihedral psi30 :30@N :30@CA :30@C :31@N
               out psi.dat 
dihedral psi31 :31@N :31@CA :31@C :32@N
               out psi.dat 
dihedral psi32 :32@N :32@CA :32@C :33@N
               out psi.dat 
dihedral psi33 :33@N :33@CA :33@C :34@N
               out psi.dat 
dihedral psi34 :34@N :34@CA :34@C :35@N
               out psi.dat 

dihedral 1_chi_1 :1@N :1@CA :1@CB :1@CG
               out chi.dat 
dihedral 1_chi_2 :1@CA :1@CB :1@CG :1@CD1
               out chi.dat 

s there a chi2?
dihedral 2_chi_1 :2@N :2@CA :2@CB :2@OG
               out chi.dat 

dihedral 3_chi_1 :3@N :3@CA :3@CB :3@CG
               out chi.dat 
dihedral 3_chi_2 :3@CA :3@CB :3@CG :3@OD1
               out chi.dat 

dihedral 4_chi_1 :4@N :4@CA :4@CB :4@CG
               out chi.dat 
dihedral 4_chi_2 :4@CA :4@CB :4@CG :4@CD
               out chi.dat 
dihedral 4_chi_3 :4@CB :4@CG :4@CD :4@OE1
               out chi.dat 

dihedral 5_chi_1 :5@N :5@CA :5@CB :5@CG
               out chi.dat 
dihedral 5_chi_2 :5@CA :5@CB :5@CG :5@OD1
               out chi.dat 

dihedral 6_chi_1 :6@N :6@CA :6@CB :6@CG
               out chi.dat 
dihedral 6_chi_2 :6@CA :6@CB :6@CG :6@CD1
               out chi.dat 

dihedral 7_chi_1 :7@N :7@CA :7@CB :7@CG
               out chi.dat 
dihedral 7_chi_2 :7@CA :7@CB :7@CG :7@CD
               out chi.dat 
dihedral 7_chi_3 :7@CB :7@CG :7@CD :7@CE
               out chi.dat 
dihedral 7_chi_4 :7@CG :7@CD :7@CE :7@NZ
               out chi.dat 

dihedral 9_chi_1 :9@N :9@CA :9@CB :9@CG1
               out chi.dat 

dihedral 10_chi_1 :10@N :10@CA :10@CB :10@CG
               out chi.dat 
dihedral 10_chi_2 :10@CA :10@CB :10@CG :10@CD1
               out chi.dat 

dihedral 12_chi_1 :12@N :12@CA :12@CB :12@CG
               out chi.dat 
dihedral 12_chi_2 :12@CA :12@CB :12@CG :12@SD
               out chi.dat 
dihedral 12_chi_3 :12@CB :12@CG :12@SD :12@CE
               out chi.dat 

dihedral 13_chi_1 :13@N :13@CA :13@CB :13@OG1
               out chi.dat 

dihedral 14_chi_1 :14@N :14@CA :14@CB :14@CG
               out chi.dat 
dihedral 14_chi_2 :14@CA :14@CB :14@CG :14@CD
               out chi.dat 
dihedral 14_chi_3 :14@CB :14@CG :14@CD :14@NE
               out chi.dat 
dihedral 14_chi_4 :14@CG :14@CD :14@NE :14@CZ
               out chi.dat 
dihedral 14_chi_5 :14@CD :14@NE :14@CZ :14@NH1
               out chi.dat 

dihedral 15_chi_1 :15@N :15@CA :15@CB :15@OG
               out chi.dat 

dihedral 17_chi_1 :17@N :17@CA :17@CB :17@CG
               out chi.dat 
dihedral 17_chi_2 :17@CA :17@CB :17@CG :17@CD1
               out chi.dat 

dihedral 19_chi_1 :19@N :19@CA :19@CB :19@CG
               out chi.dat 
dihedral 19_chi_2 :19@CA :19@CB :19@CG :19@OD1
               out chi.dat 

dihedral 20_chi_1 :20@N :20@CA :20@CB :20@CG
               out chi.dat 
dihedral 20_chi_2 :20@CA :20@CB :20@CG :20@CD1
               out chi.dat 

dihedral 21_chi_1 :21@N :21@CA :21@CB :21@CG
               out chi.dat 
dihedral 21_chi_2 :21@CA :21@CB :21@CG :21@CD
               out chi.dat 

dihedral 22_chi_1 :22@N :22@CA :22@CB :22@CG
               out chi.dat 
dihedral 22_chi_2 :22@CA :22@CB :22@CG :22@CD1
               out chi.dat 

dihedral 23_chi_1 :23@N :23@CA :23@CB :23@CG
               out chi.dat 
dihedral 23_chi_2 :23@CA :23@CB :23@CG :23@CD1
               out chi.dat 

dihedral 24_chi_1 :24@N :24@CA :24@CB :24@CG
               out chi.dat 
dihedral 24_chi_2 :24@CA :24@CB :24@CG :24@CD
               out chi.dat 
dihedral 24_chi_3 :24@CB :24@CG :24@CD :24@CE
               out chi.dat 
dihedral 24_chi_4 :24@CG :24@CD :24@CE :24@NZ
               out chi.dat 

dihedral 25_chi_1 :25@N :25@CA :25@CB :25@CG
               out chi.dat 
dihedral 25_chi_2 :25@CA :25@CB :25@CG :25@CD
               out chi.dat 
dihedral 25_chi_3 :25@CB :25@CG :25@CD :25@OE1
               out chi.dat 

dihedral 26_chi_1 :26@N :26@CA :26@CB :26@CG
               out chi.dat 
dihedral 26_chi_2 :26@CA :26@CB :26@CG :26@CD
               out chi.dat 
dihedral 26_chi_3 :26@CB :26@CG :26@CD :26@OE1
               out chi.dat 

dihedral 27_chi_1 :27@N :27@CA :27@CB :27@CG
               out chi.dat 
dihedral 27_chi_2 :27@CA :27@CB :27@CG :27@OD1
               out chi.dat 

dihedral 28_chi_1 :28@N :28@CA :28@CB :28@CG
               out chi.dat 
dihedral 28_chi_2 :28@CA :28@CB :28@CG :28@CD1
               out chi.dat 

dihedral 29_chi_1 :29@N :29@CA :29@CB :29@CG
               out chi.dat 
dihedral 29_chi_2 :29@CA :29@CB :29@CG :29@CD
               out chi.dat 
dihedral 29_chi_3 :29@CB :29@CG :29@CD :29@CE
               out chi.dat 
dihedral 29_chi_4 :29@CG :29@CD :29@CE :29@NZ
               out chi.dat 

dihedral 30_chi_1 :30@N :30@CA :30@CB :30@CG
               out chi.dat 
dihedral 30_chi_2 :30@CA :30@CB :30@CG :30@CD
               out chi.dat 
dihedral 30_chi_3 :30@CB :30@CG :30@CD :30@CE
               out chi.dat 
dihedral 30_chi_4 :30@CG :30@CD :30@CE :30@NZ
               out chi.dat 

dihedral 31_chi_1 :31@N :31@CA :31@CB :31@CG
               out chi.dat 
dihedral 31_chi_2 :31@CA :31@CB :31@CG :31@CD
               out chi.dat 
dihedral 31_chi_3 :31@CB :31@CG :31@CD :31@OE1
               out chi.dat 

dihedral 32_chi_1 :32@N :32@CA :32@CB :32@CG
               out chi.dat 
dihedral 32_chi_2 :32@CA :32@CB :32@CG :32@CD
               out chi.dat 
dihedral 32_chi_3 :32@CB :32@CG :32@CD :32@CE
               out chi.dat 
dihedral 32_chi_4 :32@CG :32@CD :32@CE :32@NZ
               out chi.dat 

dihedral 34_chi_1 :34@N :34@CA :34@CB :34@CG
               out chi.dat 
dihedral 34_chi_2 :34@CA :34@CB :34@CG :34@CD1
               out chi.dat 

dihedral 35_chi_1 :35@N :35@CA :35@CB :35@CG
               out chi.dat 
dihedral 35_chi_2 :35@CA :35@CB :35@CG :35@CD1
               out chi.dat 
'''
        scriptlines.append(analysislines)
        scriptlines.append('run\n')
        try: os.makedirs(self.simname)
        except OSError:
            pass
        with open("{:s}/{:s}.cpptraj".format(self.simname, self.simname), 'w+') as f:
            f.writelines(scriptlines)

if __name__ == "__main__":
    ff14sbsims = ['ff14sb.xray.1',
                  'ff14sb.xray.2',
                  'ff14sb.xray.3',
                  'ff14sb.nmr.1',
                  'ff14sb.nmr.2',
                  'ff14sb.nmr.3',
                  'ff14sb.KLP21D.1',
                  'ff14sb.KLP21D.2',
                  'ff14sb.KLP21D.3',
                  'ff14sb.KP21B.1',
                  'ff14sb.KP21B.2',
                  'ff14sb.KP21B.3']

    ff03wsims = ['ff03w.xray.1',
                 'ff03w.xray.2',
                 'ff03w.xray.3',
                 'ff03w.nmr.1',
                 'ff03w.nmr.2',
                 'ff03w.nmr.3',
                 'ff03w.KLP21D.1',
                 'ff03w.KLP21D.2',
                 'ff03w.KLP21D.3',
                 'ff03w.KP21B.1',
                 'ff03w.KP21B.2',
                 'ff03w.KP21B.3']

    for sim in ff14sbsims:
        DihedralAnalysis(sim)
    for sim in ff03wsims:
        DihedralAnalysis(sim)
