#!/usr/bin/env python
import argparse
import numpy
import os
import subprocess
import tempfile
import multiprocessing
import types
import copy_reg

import sys
sys.path.append('/gscratch3/lchong/ajd98/apps/molecularvolume')
import genradiilib
import pdb2volume

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

class VolumeAnalysis(object):
    nprocesses = 24

    def __init__(self):
        self._parse_args()
        self.generate_radii_lib()
        self.volumes = []
        self.go()

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--maindir', dest='maindir',
                            help='The main simulation directory '
                                 '(e.g., ff14sb.xray.1).',
                            required=True)
        parser.add_argument('--topology', dest='topologypath',
                            help='The path to the topology files',
                            required=True)
        parser.add_argument('--outdir', dest='outdirpath',
                            help='The path to the output directory.',
                            required=True)

        self.args = parser.parse_args()

    def generate_radii_lib(self):
        self.radiilibpath = os.path.join(self.args.outdirpath,
                                          "radii.lib")
        genradiilib.RadiiLibGen(self.args.topologypath, self.radiilibpath)


    def analyzesegment(self, segmentid): 
        cpptrajscript = tempfile.NamedTemporaryFile()
        pdbfile = tempfile.NamedTemporaryFile()
        pdbfilename = pdbfile.name
        pdbfile.close()
        pdbpath = "{:s}.pdb".format(pdbfilename)


        cpptrajscript.write("parm {:s}\n".format(self.args.topologypath))
        if "ff14sb.xray.1" in self.args.maindir or "ff14sb.nmr.1" in self.args.maindir:
            cpptrajscript.write("trajin {:s}/{:04d}/{:04d}_cut.nc 100 100\n"\
                                .format(self.args.maindir, segmentid, segmentid))  
        else:
            cpptrajscript.write("trajin {:s}/{:05d}/{:05d}_cut.nc 100 100\n"\
                                .format(self.args.maindir, segmentid, segmentid))  
        cpptrajscript.write("strip :WAT,Cl,Cl-,SOL\n")
        cpptrajscript.write("trajout {:s} pdb nobox\n".format(pdbpath))
        cpptrajscript.write("go\n")
        cpptrajscript.flush()

        # Call cpptraj to write out all pdb files.
        subprocess.Popen(['/ihome/lchong/ajd98/apps/amber14/bin/cpptraj', '-i', 
                          cpptrajscript.name], stdout=subprocess.PIPE).wait()
        vol = pdb2volume.PDBVolume("{:s}.pdb".format(pdbfilename), 
                                   self.radiilibpath, 
                                   explicitsolvent=False, 
                                   solventrad=1.4, 
                                   voxel_len=0.1).run()

        # Delete the pdb file
        os.remove(pdbpath)
        return vol


    def go(self):
        print("Using {:d} processes".format(self.nprocesses))
        pool = multiprocessing.Pool(self.nprocesses)

        jobs = [segid for segid in range(1,10001)]
        
        outfile = open(os.path.join(self.args.outdirpath, 'volume'),'w+')
        self.volumes = []
        for i in pool.map(self.analyzesegment, jobs):
            outfile.write("{:.02f}\n".format(i))
            self.volumes.append(i)
        self.volumes = numpy.array(self.volumes, 
                                   dtype=numpy.float64)

        outpath = os.path.join(self.args.outdirpath, 'volume')
        numpy.save(outpath, self.volumes)

if __name__ == '__main__':
    VolumeAnalysis() 
