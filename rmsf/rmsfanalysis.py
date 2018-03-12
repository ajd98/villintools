#!/usr/bin/env python
import os
import subprocess

class RMSFAnalysis(object):
    def __init__(self, statefiles):
        '''
        statefiles: (iteratable) strings denoting paths to .npy files describing
            simulation states.
        '''
        self.statefiles = statefiles

    def load_states(self):
        self.states = [numpy.load(statefile) for statefile in self.statefiles]

    def get_parmpath(self, simname):
        '''
        Return path to topology file for simulation
        '''
        simdir = self.get_simdir()
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
        simdir = self.get_simdir()
        fmtstr = "{:05d}"
        return os.path.join(simdir, fmtstr.format(iseg), 
                            "{:s}_solute.nc".format(fmtstr.format(iseg)))

    def generate_script(self):
        NSEGS=10000
        self.scriptlines = []
        self.scriptlines.append('parm {:s}\n'.format(self.parmpath))
        for iseg in range(1,NSEGS+1):
            trajpath = self.get_trajpath(iseg)
            self.scriptlines.append('trajin {:s}\n'.format(trajpath))

        self.scriptlines.append('rmsd JUNK :@C,CA,O,N first \n')
        self.scriptlines.append('go\n')
