#!/usr/bin/env python
import os
import subprocess
import numpy
import tempfile
from classify_no_smoothing import StateClassifier

INPUTTEMPLATE = \
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

PMEMDSCRIPT = \
'''
module purge
module load intel/2017.1.132 mkl/2017.1.132 cuda/8.0.44 amber/16

cd DIRECTORY

PMEMD="$(which pmemd.cuda) -O"
${PMEMD} -i INPUT -o MDOUT -c RESTART -p TOPOLOGY -r NEWRESTART
'''

CPPTRAJSCRIPT = \
'''
parm PARMPATH
trajin COORDPATH

# Phi angles
dihedral phi2  :1@C :2@N :2@CA :2@C out phi.dat
dihedral phi3  :2@C :3@N :3@CA :3@C out phi.dat
dihedral phi4  :3@C :4@N :4@CA :4@C out phi.dat
dihedral phi5  :4@C :5@N :5@CA :5@C out phi.dat
dihedral phi6  :5@C :6@N :6@CA :6@C out phi.dat
dihedral phi7  :6@C :7@N :7@CA :7@C out phi.dat
dihedral phi8  :7@C :8@N :8@CA :8@C out phi.dat
dihedral phi9  :8@C :9@N :9@CA :9@C out phi.dat
dihedral phi10 :9@C :10@N :10@CA :10@C out phi.dat
dihedral phi11 :10@C :11@N :11@CA :11@C out phi.dat
dihedral phi12 :11@C :12@N :12@CA :12@C out phi.dat
dihedral phi13 :12@C :13@N :13@CA :13@C out phi.dat
dihedral phi14 :13@C :14@N :14@CA :14@C out phi.dat
dihedral phi15 :14@C :15@N :15@CA :15@C out phi.dat
dihedral phi16 :15@C :16@N :16@CA :16@C out phi.dat
dihedral phi17 :16@C :17@N :17@CA :17@C out phi.dat
dihedral phi18 :17@C :18@N :18@CA :18@C out phi.dat
dihedral phi19 :18@C :19@N :19@CA :19@C out phi.dat
dihedral phi20 :19@C :20@N :20@CA :20@C out phi.dat
dihedral phi21 :20@C :21@N :21@CA :21@C out phi.dat
dihedral phi22 :21@C :22@N :22@CA :22@C out phi.dat
dihedral phi23 :22@C :23@N :23@CA :23@C out phi.dat
dihedral phi24 :23@C :24@N :24@CA :24@C out phi.dat
dihedral phi25 :24@C :25@N :25@CA :25@C out phi.dat
dihedral phi26 :25@C :26@N :26@CA :26@C out phi.dat
dihedral phi27 :26@C :27@N :27@CA :27@C out phi.dat
dihedral phi28 :27@C :28@N :28@CA :28@C out phi.dat
dihedral phi29 :28@C :29@N :29@CA :29@C out phi.dat
dihedral phi30 :29@C :30@N :30@CA :30@C out phi.dat
dihedral phi31 :30@C :31@N :31@CA :31@C out phi.dat
dihedral phi32 :31@C :32@N :32@CA :32@C out phi.dat
dihedral phi33 :32@C :33@N :33@CA :33@C out phi.dat
dihedral phi34 :33@C :34@N :34@CA :34@C out phi.dat
dihedral phi35 :34@C :35@N :35@CA :35@C out phi.dat

# Psi angles
dihedral psi1  :1@N :1@CA :1@C :2@N out psi.dat
dihedral psi2  :2@N :2@CA :2@C :3@N out psi.dat
dihedral psi3  :3@N :3@CA :3@C :4@N out psi.dat
dihedral psi4  :4@N :4@CA :4@C :5@N out psi.dat
dihedral psi5  :5@N :5@CA :5@C :6@N out psi.dat
dihedral psi6  :6@N :6@CA :6@C :7@N out psi.dat
dihedral psi7  :7@N :7@CA :7@C :8@N out psi.dat
dihedral psi8  :8@N :8@CA :8@C :9@N out psi.dat
dihedral psi9  :9@N :9@CA :9@C :10@N out psi.dat
dihedral psi10 :10@N :10@CA :10@C :11@N out psi.dat
dihedral psi11 :11@N :11@CA :11@C :12@N out psi.dat
dihedral psi12 :12@N :12@CA :12@C :13@N out psi.dat
dihedral psi13 :13@N :13@CA :13@C :14@N out psi.dat
dihedral psi14 :14@N :14@CA :14@C :15@N out psi.dat
dihedral psi15 :15@N :15@CA :15@C :16@N out psi.dat
dihedral psi16 :16@N :16@CA :16@C :17@N out psi.dat
dihedral psi17 :17@N :17@CA :17@C :18@N out psi.dat
dihedral psi18 :18@N :18@CA :18@C :19@N out psi.dat
dihedral psi19 :19@N :19@CA :19@C :20@N out psi.dat
dihedral psi20 :20@N :20@CA :20@C :21@N out psi.dat
dihedral psi21 :21@N :21@CA :21@C :22@N out psi.dat
dihedral psi22 :22@N :22@CA :22@C :23@N out psi.dat
dihedral psi23 :23@N :23@CA :23@C :24@N out psi.dat
dihedral psi24 :24@N :24@CA :24@C :25@N out psi.dat
dihedral psi25 :25@N :25@CA :25@C :26@N out psi.dat
dihedral psi26 :26@N :26@CA :26@C :27@N out psi.dat
dihedral psi27 :27@N :27@CA :27@C :28@N out psi.dat
dihedral psi28 :28@N :28@CA :28@C :29@N out psi.dat
dihedral psi29 :29@N :29@CA :29@C :30@N out psi.dat
dihedral psi30 :30@N :30@CA :30@C :31@N out psi.dat
dihedral psi31 :31@N :31@CA :31@C :32@N out psi.dat
dihedral psi32 :32@N :32@CA :32@C :33@N out psi.dat
dihedral psi33 :33@N :33@CA :33@C :34@N out psi.dat
dihedral psi34 :34@N :34@CA :34@C :35@N out psi.dat

# Chi angles
# L1
dihedral 1_chi_1 :1@N :1@CA :1@CB :1@CG out chi.dat
dihedral 1_chi_2 :1@CA :1@CB :1@CG :1@CD1 out chi.dat

# S2 - is there a chi2?
dihedral 2_chi_1 :2@N :2@CA :2@CB :2@OG out chi.dat

# D3
dihedral 3_chi_1 :3@N :3@CA :3@CB :3@CG out chi.dat
dihedral 3_chi_2 :3@CA :3@CB :3@CG :3@OD1 out chi.dat

# E4
dihedral 4_chi_1 :4@N :4@CA :4@CB :4@CG out chi.dat
dihedral 4_chi_2 :4@CA :4@CB :4@CG :4@CD out chi.dat
dihedral 4_chi_3 :4@CB :4@CG :4@CD :4@OE1 out chi.dat

# D5
dihedral 5_chi_1 :5@N :5@CA :5@CB :5@CG out chi.dat
dihedral 5_chi_2 :5@CA :5@CB :5@CG :5@OD1 out chi.dat

# F6
dihedral 6_chi_1 :6@N :6@CA :6@CB :6@CG out chi.dat
dihedral 6_chi_2 :6@CA :6@CB :6@CG :6@CD1 out chi.dat

# K7
dihedral 7_chi_1 :7@N :7@CA :7@CB :7@CG out chi.dat
dihedral 7_chi_2 :7@CA :7@CB :7@CG :7@CD out chi.dat
dihedral 7_chi_3 :7@CB :7@CG :7@CD :7@CE out chi.dat
dihedral 7_chi_4 :7@CG :7@CD :7@CE :7@NZ out chi.dat

# A8 - nothing!

# V9
dihedral 9_chi_1 :9@N :9@CA :9@CB :9@CG1 out chi.dat

# F10
dihedral 10_chi_1 :10@N :10@CA :10@CB :10@CG out chi.dat
dihedral 10_chi_2 :10@CA :10@CB :10@CG :10@CD1 out chi.dat

# G11 - nothing!

# M12
dihedral 12_chi_1 :12@N :12@CA :12@CB :12@CG out chi.dat
dihedral 12_chi_2 :12@CA :12@CB :12@CG :12@SD out chi.dat
dihedral 12_chi_3 :12@CB :12@CG :12@SD :12@CE out chi.dat

# T13
dihedral 13_chi_1 :13@N :13@CA :13@CB :13@OG1 out chi.dat

# R14
dihedral 14_chi_1 :14@N :14@CA :14@CB :14@CG out chi.dat
dihedral 14_chi_2 :14@CA :14@CB :14@CG :14@CD out chi.dat
dihedral 14_chi_3 :14@CB :14@CG :14@CD :14@NE out chi.dat
dihedral 14_chi_4 :14@CG :14@CD :14@NE :14@CZ out chi.dat
dihedral 14_chi_5 :14@CD :14@NE :14@CZ :14@NH1 out chi.dat

# S15
dihedral 15_chi_1 :15@N :15@CA :15@CB :15@OG out chi.dat

# A16 - nothing!

# F17
dihedral 17_chi_1 :17@N :17@CA :17@CB :17@CG out chi.dat
dihedral 17_chi_2 :17@CA :17@CB :17@CG :17@CD1 out chi.dat

# A18 - nothing!

# N19
dihedral 19_chi_1 :19@N :19@CA :19@CB :19@CG out chi.dat
dihedral 19_chi_2 :19@CA :19@CB :19@CG :19@OD1 out chi.dat

# L20
dihedral 20_chi_1 :20@N :20@CA :20@CB :20@CG out chi.dat
dihedral 20_chi_2 :20@CA :20@CB :20@CG :20@CD1 out chi.dat

# P21
dihedral 21_chi_1 :21@N :21@CA :21@CB :21@CG out chi.dat
dihedral 21_chi_2 :21@CA :21@CB :21@CG :21@CD out chi.dat

# L22
dihedral 22_chi_1 :22@N :22@CA :22@CB :22@CG out chi.dat
dihedral 22_chi_2 :22@CA :22@CB :22@CG :22@CD1 out chi.dat

# W23
dihedral 23_chi_1 :23@N :23@CA :23@CB :23@CG out chi.dat
dihedral 23_chi_2 :23@CA :23@CB :23@CG :23@CD1 out chi.dat

# K24
dihedral 24_chi_1 :24@N :24@CA :24@CB :24@CG out chi.dat
dihedral 24_chi_2 :24@CA :24@CB :24@CG :24@CD out chi.dat
dihedral 24_chi_3 :24@CB :24@CG :24@CD :24@CE out chi.dat
dihedral 24_chi_4 :24@CG :24@CD :24@CE :24@NZ out chi.dat

# Q25
dihedral 25_chi_1 :25@N :25@CA :25@CB :25@CG out chi.dat
dihedral 25_chi_2 :25@CA :25@CB :25@CG :25@CD out chi.dat
dihedral 25_chi_3 :25@CB :25@CG :25@CD :25@OE1 out chi.dat

# Q26
dihedral 26_chi_1 :26@N :26@CA :26@CB :26@CG out chi.dat
dihedral 26_chi_2 :26@CA :26@CB :26@CG :26@CD out chi.dat
dihedral 26_chi_3 :26@CB :26@CG :26@CD :26@OE1 out chi.dat

# N27
dihedral 27_chi_1 :27@N :27@CA :27@CB :27@CG out chi.dat
dihedral 27_chi_2 :27@CA :27@CB :27@CG :27@OD1 out chi.dat

# L28
dihedral 28_chi_1 :28@N :28@CA :28@CB :28@CG out chi.dat
dihedral 28_chi_2 :28@CA :28@CB :28@CG :28@CD1 out chi.dat

# K29
dihedral 29_chi_1 :29@N :29@CA :29@CB :29@CG out chi.dat
dihedral 29_chi_2 :29@CA :29@CB :29@CG :29@CD out chi.dat
dihedral 29_chi_3 :29@CB :29@CG :29@CD :29@CE out chi.dat
dihedral 29_chi_4 :29@CG :29@CD :29@CE :29@NZ out chi.dat

# K30
dihedral 30_chi_1 :30@N :30@CA :30@CB :30@CG out chi.dat
dihedral 30_chi_2 :30@CA :30@CB :30@CG :30@CD out chi.dat
dihedral 30_chi_3 :30@CB :30@CG :30@CD :30@CE out chi.dat
dihedral 30_chi_4 :30@CG :30@CD :30@CE :30@NZ out chi.dat

# E31
dihedral 31_chi_1 :31@N :31@CA :31@CB :31@CG out chi.dat
dihedral 31_chi_2 :31@CA :31@CB :31@CG :31@CD out chi.dat
dihedral 31_chi_3 :31@CB :31@CG :31@CD :31@OE1 out chi.dat

# K32
dihedral 32_chi_1 :32@N :32@CA :32@CB :32@CG out chi.dat
dihedral 32_chi_2 :32@CA :32@CB :32@CG :32@CD out chi.dat
dihedral 32_chi_3 :32@CB :32@CG :32@CD :32@CE out chi.dat
dihedral 32_chi_4 :32@CG :32@CD :32@CE :32@NZ out chi.dat

# G33 - nothing

# L34
dihedral 34_chi_1 :34@N :34@CA :34@CB :34@CG out chi.dat
dihedral 34_chi_2 :34@CA :34@CB :34@CG :34@CD1 out chi.dat

# F35
dihedral 35_chi_1 :35@N :35@CA :35@CB :35@CG out chi.dat
dihedral 35_chi_2 :35@CA :35@CB :35@CG :35@CD1 out chi.dat

# Run the analysis
run
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
        self.cpptrajbin = '/ihome/lchong/ajd98/apps/amber14/bin/cpptraj'

    def run(self):
        cpptrajscript = CPPTRAJSCRIPT.replace('PARMPATH',parmpath)\
                                     .replace('COORDPATH', coordpath)
        with tempfile.NamedTemporaryFile() as cpptrajfile:
            cpptrajfile.write(cpptrajscript)
            cpptrajfile.flush()
            subprocess.Popen([self.cpptrajbin, '-i', cpptrajfile.name]).wait()

        cwd = os.path.getcwd()
        
        nosmoothingclassifier = StateClassifier()
        data = nosmoothingclassifier.load_data(cwd)
        classifications = nosmoothingclassifier.vector_classify(data)
        if numpy.all(classifications == -1):
            status = -1
            return status
        else: 
            position = numpy.argmin(classifications == -1)[0]
            status = classifications[position] 
            assert status != -1
            return status

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

            classifier = HP35Classifier

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
