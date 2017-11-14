#!/usr/bin/env python
import multiprocessing
import numpy

global INPUTTEMPLATE = \
'''1 ns unrestrained NPT run using Langevin thermostat and MC barostat
&cntrl
  irest     = 1,
  ntx       = 5,
  ig        = -1,
  dt        = 0.002,
  nstlim    = NSTLIM,
  nscm      = 500,
  ntr       = 0,
  ntb       = 2,
  ntp       = 1,
  barostat  = 2,
  pres0     = 1.0,
  mcbarint  = 100,
  comp      = 44.6,
  taup      = 1.0,
  ntt       = 3,
  temp0     = 278.15,
  gamma_ln  = 1.0,
  ntf       = 2,
  ntc       = 2,
  cut       = 10.0,
  ntpr      = 500,
  ntxo      = 2,
  ntwr      = NTWR,
  ioutfm    = 1,
  ntwx      = 500,
  iwrap     = 1,
&end
'''

global PMEMDSCRIPT = \
'''
module purge
module load intel/2017.1.132 mkl/2017.1.132 cuda/8.0.44 amber/16

cd DIRECTORY

PMEMD="$(which pmemd.cuda) -O"
${PMEMD} -i INPUT -o MDOUT -c RESTART -p TOPOLOGY -r NEWRESTART
'''


class HP35Classifier(object):
    '''
    Classify the states that a simulation has visited. If the simulation has
    reached state n (where n is a positive integer) prior to any other state, 
    return n.  Otherwise, return -1
    '''
    def __init__(self, coordpath, parmpath):
        self.coordpath = coordpath
        self.parmpath = parmpath

    def run(self):
        return NotImplementedError

class FrameJob(object):
    def __init__(self, restartpath, parmpath, maindir, classifier, nsims=20):

class SegmentJob(object):
    '''
    Container for all tasks related to segment of the original simulation
    (in my case, the segments are labeled 00001 00002 ... 10000, each 1 ns in
    length).

    First, we need to re-run the simulation and save the velocities at every
    relevant time point.

    indicatorarr should be an array of ones and zeros; for timepoints corresponding
    to ones, calculate the transmission coefficient.

    Once we have the velocities for each time point, we can run N copies of the
    simulation, stopping each when it reaches one of the boundary states (N or 
    N')

    All data is saved to analysisdir/segid.  analysisdir should be a path unique
    to the simulation
    '''

    N = 20

    def __init__(self, segid, simdir, parmpath, indicatorarr, analysisdir, classifier):
        self.segid = segid
        self.simdir = simdir
        self.parmpath = parmpath
        self.indicatorarr = indicatorarr
        self.analysisdir = analysisdir
        self.classifier = classifier

    def get_restart_path(self):
        '''
        Return the path to the restart file that was used to start segment
        self.segid
        '''
        if self.segid > 1:
            # The formatting is different for these simulations
            if ('ff14sb.xray.1' in simdir or 'ff14sb.nmr.1' in simdir):
                extension = os.path.join("{:04d}".format(self.segid-1),
                                         "{:04d}.rst".format(self.segid-1))
            else:
                extension = os.path.join("{:05d}".format(self.segid-1),
                                         "{:05d}.rst".format(self.segid-1))
        # Return the restart file from the end of equilibration
        else:
            if 'ff14sb' in simdir and not ('ttet' in simdir):
                extension = "4_eq2/4_eq2.rst"
            elif 'ff14sb' in simdir and 'ttet' in simdir and not ('035' in simdir):
                extension = "12_eq2/12_eq2.rst"
            elif 'ff14sb' in simdir and 'ttet' in simdir and '035' in simdir:
                extension = '7_eq2/7_eq2.rst'
            elif 'ff03w' in simdir:
                extension = '4_eq2/4_eq2.rst'
            else:
                raise ValueError
        return os.path.join(self.simdir, extension) 

    def run(self):
        # First, re-run the simulation
        restartpath = self.get_restart_path()

        # run the simulation for 1 nanosecond, and save a new restart file every 10 ps
        inputstr = INPUTTEMPLATE.replace('NSTLIM','500000').replace('NTWR', '-5000')

        # Restartdir will contain all the restart files that we need for starting the
        # transmission coefficient calculation simulations
        restartdir = os.path.join(self.analysisdir, 
                                  "{:05d}".format(self.segid),
                                  "restarts")
        os.makedirs(restartdir)
        os.chdir(restartdir)

        script = PMEMDSCRIPT.replace('DIR', restartdir)\
                            .replace('RESTART', restartpath)\
                            .replace('TOPOLOGY', self.parmpath)\
                            .replace('MDOUT', 'mdout')\
                            .replace('NEWRESTART', 'restart')

        with open('run.pmemd', 'w+') as f:
            f.write(script)

        # This should take between 5 and 10 minutes.
        subprocess.Popen(['bash', 'run.pmemd']).wait()

        # At this point, we should be finished saving all the restart files for the specified segment
        # Now it is a matter of looping over the segments for which we need to calculate the transmission coefficient
        for itp, do_calculation in enumerate(self.indicatorarr):
            if do_calculation:
               restartsuffix = 5000*itp
               restartfile = os.path.join(restartdir, 'restart.{:d}'.format(restartsuffix))
               jobdir = os.path.join(self.analysisdir, 
                                     "{:05d}".format(self.segid), 
                                     "{:07d}".format(itp))
               job = FrameJob(restartfile, parmpath, jobdir, self.classifier, nsims=self.N)
 

        



class TransmissionCalculation(object):
    '''
    Calculate transmission coefficients for a specified set of structures.

    ----------
    Arguments:
    ----------
    indicatorfile: (str) The path to a .npy file containing an array of ones and
        zeros. Structures corresponding to ones should have their transmission
        coefficients calculated.

    parmpath: (str) The path to the topology file.

    simdir: (str) The path to the main simulation directory
    '''

    def __init__(self, indicatorfile, parmpath, simdir):

        self.indicator = numpy.load(indicatorfile)
        self.parmpath = parmpath
        self.simdir = simdir

     
