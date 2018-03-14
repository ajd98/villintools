#!/usr/bin/env python
import os
import numpy

class RMSFAnalysis(object):
    def __init__(self, statefiles):
        '''
        statefiles: (iteratable) strings denoting paths to .npy files describing
            simulation states.
        '''
        self.statefiles = statefiles
        self.parse_statefiles()
        self.generate_script()

    def parse_statefiles(self):
        self.load_states()
        self.sims = [os.path.basename(statefile)[:-4] for statefile in self.statefiles]

    def load_states(self):
        self.states = []
        for statefile in self.statefiles:
            probs = numpy.load(statefile)
            states = numpy.argmax(probs, axis=1)
            mask = numpy.all(numpy.isnan(probs), axis=1)
            states[mask] = -1
            self.states.append(states)

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

    def get_state_ranges(self, isim, state):
        classifications = self.states[isim]
        persistent_state = -1
        ranges = []
        for i, classification in enumerate(classifications):
            if classification == state and persistent_state != state:
                start = i
            if classification != state and persistent_state == state:
                end = i-1
                ranges.append([start, end])
            persistent_state = classification
        return ranges


     
    def generate_script(self):
        FRAMES_PER_SEGMENT = 1
        # Collect structures in each state
        for state in range(5):
            scriptlines = []

            for isim, sim in enumerate(self.sims):
                if isim == 0:
                    parmpath = self.get_parmpath(sim)
                    scriptlines.append("parm {:s}\n".format(parmpath))
                # Ranges in which the simulation is in ``state``
                #[[0,20], [22,70] .. ]
                # state_ranges is zero-indexed
                state_ranges = self.get_state_ranges(isim, state)
                print(state_ranges)
                for rangestart, rangeend in state_ranges:
                    
                    # Get the cpptraj lines for loading the range, (rangestart, rangeend)
                    # segmentstart, segmentend, segment, framestart, and frameend are one-indexed
                    segmentstart = rangestart//FRAMES_PER_SEGMENT + 1
                    segmentend = rangeend//FRAMES_PER_SEGMENT + 1
                    for segment in range(segmentstart, segmentend+1):
                        segmentpath = self.get_trajpath(sim, segment)
                        framestart = rangestart - (segment-1)*FRAMES_PER_SEGMENT + 1
                        frameend = rangeend - (segment-1)*FRAMES_PER_SEGMENT + 1

                        framestart = max(1, framestart)
                        frameend = min(FRAMES_PER_SEGMENT, frameend)

                        ## for loading only every 1000th frame ##
                        framestart = 1000*(framestart - 1)+1
                        frameend = 1000*(frameend-1)+1
                        #######################################

                        #                       Also for loading every 1000th frame
                        #                                         V
                        scriptlines.append('trajin {:s} {:d} {:d} 1000\n'.format(segmentpath,
                                                                          framestart, 
                                                                          frameend))
            # Calculate the average structure, starting by rms-fitting on first frame
            #scriptlines.append('rms PHONY !@Cl,Cl-,CL first\n')
            scriptlines.append('rms PHONY @N,CA,C,O&(!:35)|(@N,CA,C)&:35 first\n')
            # Get the actual average structure, saving it as average.pdb
            scriptlines.append('average average.{:d}.pdb\n'.format(state))
            scriptlines.append('average crdset AVERAGESTRUCTURE\n')
            # Run to do the calculation
            scriptlines.append('run\n')
            # Now fit on the average structure
            scriptlines.append('rms PHONY2 @N,CA,C,O&(!:35)|(@N,CA,C)&:35 ref AVERAGESTRUCTURE\n')
            # Finally calculate the rmsf
            scriptlines.append('rmsf byres out rmsf.{:d}.dat\n'.format(state))
            scriptlines.append('run\n')
            with open("{:d}.cpptraj".format(state), 'w+') as f:
                f.writelines(scriptlines)

if __name__ == "__main__":
    ff14sbstatefiles = ['/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.xray.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.xray.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.xray.3.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.nmr.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.nmr.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.nmr.3.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.KLP21D.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.KLP21D.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.KLP21D.3.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.KP21B.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.KP21B.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff14sb.KP21B.3.npy']

    ff03wstatefiles = ['/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.xray.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.xray.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.xray.3.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.nmr.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.nmr.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.nmr.3.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.KLP21D.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.KLP21D.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.KLP21D.3.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.KP21B.1.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.KP21B.2.npy',
                        '/home/ajd98/projects/villin/18.03.03/ntoruskdc/ff03w.KP21B.3.npy']
    RMSFAnalysis(ff14sbstatefiles)
