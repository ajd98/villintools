#!/usr/bin/env python
import multiprocessing
import numpy

global INPUTTEMPLATE = \
'''1 ns unrestrained NPT run using Langevin thermostat and MC barostat
&cntrl
  irest     = 1,
  ntx       = 5,
  ig        = RANDOMSEED,
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
        self.restartpath = restartpath
        self.parmpath = parmpath
        self.maindir = maindir
        self.classifier = classifier
        self.nsims = nsims

    def segment_is_complete(self, segdir):
        '''
        Check if the segment in segdir is complete. Return True if so, and 
        return False otherwise
        '''
        # The last portion of segdir should be a string of digits that denotes
        # the segment number
        segnum = segdir.split('/')[-1]
        
        mdoutpath = os.path.join(segdir, "{:s}.out".format(segnum))

        if os.path.exists(mdoutpath):
            with open(mdoutpath, 'r') as mdout:
                last_line = mdout.readlines()[-1]
            if "Total wall time" in last_line:
                return True
            else:
                return False
        else:
            return False

    def run(self):
        # run self.nsims simulations. Each is performed until it reaches some 
        # state
        for isim in xrange(self.nsims):
            # simdir contains one simulation that starts from self.restartpath
            # and continues until it reaches any state. simdir contains multiple
            # sort segments; each segment is checked to see if the simulation
            # has reached a state
            simdir = os.path.join(maindir, "{:02d}".format(isim))
            # endpoint_path contains a single ascii character denoting the final
            # state of the simulations; if this file already exists, then the 
            # simulation was completed in a previous submission of this script.
            endpoint_path = os.path.join(simdir, 'endpoint')

            # if the simulation was completed in a previous submission of this
            # script, skip to the next simulation
            if os.path.exists(endpoint_path):
                continue

            os.chdir(simdir)

            # Think of the status as the "current" state of the simulation,
            # though it works as a toggle -- once the simulation arrives in a
            # state other than -1, status stays at that value. We exit the 
            # following while loop once status is nonnegative
            status = -1
            iseg = 0 
            
            current_restart = self.restartpath
            while status == -1:
                # Prepare a directory for this segment
                segdir = os.path.join(simdir, "{:04d}".format(iseg)) 
                coordpath = os.path.join(segdir, '{:04d}.nc'.format(iseg))
                newrestartpath = os.path.join(segdir, '{:04d}.rst'.format(iseg))

                if not os.path.exists(segdir):
                    os.makedirs(segdir)
                os.chdir(segdir)

                # Check if the segment is already completed. If not, run the 
                # segment. If the segment is completed and we got to this part 
                # of the script, we know also that the endnpoint file did not
                # exist, implying that status must still be -1.  Therefore we
                # do not need to update status.
                if not self.segment_is_complete(segdir):

                    inputstr = INPUTTEMPLATE.replace('RANDOMSEED', numpy.random.randint())\
                                            .replace('NSTLIM', '50000')\
                                            .replace('NTWR', '50000')

                    with open('{:04d}.in'.format(iseg), 'w+') as mdin:
                        mdin.write(inputstr)


                    script = PMEMDSCRIPT.replace('DIR', segdir)\
                                        .replace('RESTART', current_restart)\
                                        .replace('TOPOLOGY', self.parmpath)\
                                        .replace('MDOUT', coordpath)\
                                        .replace('NEWRESTART', newrestartpath)
                    with open('run.pmemd','w+') as f:
                        f.write(script)

                    # Run the simulation segment
                    subprocess.Popen(['bash', 'run.pmemd']).wait()

                    classifier = self.classifier(coordpath, self.parmpath)
                    status = classifier.run()

                current_restart = newrestartpath
                iseg += 1

                if iseg > 100:
                    break
            with open(endpoint_path, 'w+') as endpoint_file:
                endpoint_file.write("{:d}".format(status))

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
       sdf self.indicatorarr = indicatorarr
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

    def get_seed(self):
        # find the path to the mdout file from the previous run of the simulation
        if 'ff14sb.xray.1' in simdir or 'ff14sb.nmr.1' in simdir:
            mdoutpath = os.path.join(self.simdir, 
                                     "{:04d}".format(self.segid),
                                     "{:04d}.out".format(self.segid))
        else:
            mdoutpath = os.path.join(self.simdir, 
                                     "{:05d}".format(self.segid),
                                     "{:05d}.out".format(self.segid))
        # Scan the file for the line where the random seed is specified
        with open(mdoutpath, 'r') as mdout:
            for line in mdout:
                if 'random seed' in line:
                    break
        seed = int(line.split()[8])
        return seed

    def restart_files_already_generated(self, restartdir):
        '''
        Return True if the restart files for this segment were already generated
        and return False otherwise.
        '''
        mdoutpath = os.path.join(restartdir, 'mdout')
        if os.path.exists(mdoutpath):
            with open(mdoutpath, 'r') as mdout:
                lastline = mdout.readlines()[-1]
            if 'Total wall time' in lastline:
                return True
            else:
                return False
        else:
            return False


    def run(self):
        # First, re-run the simulation so we have restart files at every 
        # necessary time point

        # Restartdir will contain all the restart files that we need for starting the
        # transmission coefficient calculation simulations
        restartdir = os.path.join(self.analysisdir, 
                                  "{:05d}".format(self.segid),
                                  "restarts")
        if not os.path.exists(restartdir):
            os.makedirs(restartdir)

        os.chdir(restartdir)

        # Only do this next section if it was not already completed
        if not self.restart_files_already_generated(restartdir):
            # Get the path to the restart file that was originally used to start
            # this simulation segment
            restartpath = self.get_restart_path()

            # To rerun the simulation, we need the random seed that was used the first time.
            seed = self.get_seed()

            # run the simulation for 1 nanosecond, and save a new restart file every 10 ps
            inputstr = INPUTTEMPLATE.replace('NSTLIM','500000')\
                                    .replace('NTWR', '-5000')\
                                    .replace('RANDOMSEED', "{:d}".format(seed))


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
               job.run()
 

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

    def __init__(self, indicatorfile, parmpath, simdir, analysisdir):

        self.indicator = numpy.load(indicatorfile)
        self.parmpath = parmpath
        self.simdir = simdir
        self.analysisdir = analysisdir

        # Generate a list of jobs
        for iseg in xrange(1,10001):
            indicators = self.indicator[100*i:100*(i+1)]

            analysisdir = 
            classifier = 

            job = SegmentJob(iseg, self.simdir, self.parmpath, indicators,
                             self.analysisdir, classifier) 
            job.run()

if __name__ == "__main__":
    indicatorfile = '/gscratch3/lchong/ajd98/villin/transmission/indicatorfiles/ff14sb.xray.1.npy'
    parmpath = '/gscratch3/lchong/ajd98/villin/ff14sb.xray.1/1_leap/VILLIN.parm7'
    simdir = '/gscratch3/lchong/ajd98/villin/ff14sb.xray.1/'
    analysisdir = '/gscratch3/lchong/ajd98/villin/transmission/ff14sb.xray.1'

    TransmissionCalculation(indicatorfile,
                            parmpath,
                            simdir,
                            analysisdir)
