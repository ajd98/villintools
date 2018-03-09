#!/usr/bin/env python
import os
import subprocess

class CpptrajController(object):
    def __init__(self, simname):
        self.simname = simname
        self.parmpath = self.get_parmpath()
        self.simdir = self.get_simdir()

    def get_parmpath(self):
        simdir = self.get_simdir()

        if 'ff14sb' in self.simname:
            if 'ttet035' in self.simname:
                return os.path.join(simdir, '3_leap', 'VILLIN.parm7')
            elif 'ttet' in self.simname:
                return os.path.join(simdir, '8_leap2', 'VILLIN.parm7')
            else:
                return os.path.join(simdir, '1_leap', 'VILLIN.parm7')
        elif 'ff03w' in self.simname:
            return os.path.join(simdir, '1_parmed', 'VILLIN_waters_edited.parm7')
            
    def get_simdir(self):
        maindir = self.get_maindir()
        if 'ff14sb.xray' in self.simname:
            subdir =  'ff14sb.1yrf'
        elif 'ff14sb.nmr' in self.simname:
            subdir = 'ff14sb.1vii':
        elif 'ff03w.xray' in self.simname:
            subdir = 'ff03w.1yrf'
        elif 'ff03w.nmr' in self.simname:
            subdir = 'ff03w.1vii'
        else:
            subdir = self.simname[:-2]

        if 'ff14sb.xray.1' in self.simname:
            subsubdir = 'ff14sb.1yrf.1'
        elif 'ff14sb.nmr.1' in self.simname:
            subsubdir = 'ff14sb.1vii.1'
        else:
            subsubdir = self.simname

        return os.path.join(maindir, subdir, subsubdir)

    def get_maindir(self):
        if 'ttet035' in self.simname:
            maindir = '/mnt/NAS4/villin/'
        else:
            maindir = '/mnt/NAS2/VILLIN/'
        return maindir

    def get_trajpath(self, iseg):
        try:
            simdir = self.simdir
        except AttributeError:
            self.simdir = self.get_simdir()
            simdir = self.simdir
        if self.simname in ['ff14sb.xray.1', 'ff14sb.nmr.1']:
            fmtstr = "{:04d}" 
        else:
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
