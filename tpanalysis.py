#!/usr/bin/env python
import numpy

class TPAnalysis(object):
    def __init__(self, statelabelpaths, volumedatapaths):
        '''
        statelabelpaths: (list of str) A list of file paths to .npy files, each
            of which contains a column of integers indicating state labels. 
            For timepoints at which the system is in between states, the label
            should be "-1". Non-negative integers are treated as state labels.
        volumedatapaths: (list of str) A list of file paths to .npy files, each
            of which contains an n-by-1 numpy array, where the index runs over
            the timepoint, and each element of the array is the volume of the
            protein at the that timepoint.
        '''
        self.statelabelpaths = statelabelpaths
        self.volumedatapaths = volumedatapaths

        self.load_state_labels()
        self.load_volume_data()


    def load_state_labels(self):
        '''
        Load the state labels from the .npy files specified in the attribute
        ``self.statelabelpaths``, into the attribute ``self.statelabels``,
        a list of numpy arrays, where the i^th index of each array indicates the
        state label at the i^th time point.
        '''
        self.statelabels = []
        for statelabelpath in self.statelabelpaths:
            self.statelabels.append(numpy.load(statelabelpath))

    def load_volume_data(self):
        '''
        Load the volume data from the .npy files specified in the attribute
        ``self.volumedatapaths`` into the attribute ``self.volume``, a list
        of numpy arrays, where the i^th index of each array indicates the state
        label at the i^th time point.
        '''
        self.volume = []
        for volumedatapath in self.volumedatapaths:
            self.volume.append(numpy.load(volumedatapath))

    def assign_tp(self, assignments, departing_state=0, arriving_state=1):
        '''
        Assign timepoints that are members of the transition path ensemble.

        ---------------
        Arguments
        ---------------
        assignments: (numpy.ndarray, dtype=int) An array of state labels. The
            value should be -1 for time points at which the system is in-
            between states.

        departing_state: (int) The state from which transition paths originate.

        arriving_state: (int) The state at which transitino paths terminate.

        ---------
        Returns
        ---------
        tpassignments: (numpy.ndarray) A length-n numpy array that is True where
            the corresponding timepoint is part of the transition path ensemble,
            and False elsewhere.
        groundassignments: (numpy.ndarray) A legnth-n numpy array that is True
            where the corresponding timepoint is either in the departing state
            (based on ``assignments``), or has left the departing state and next
            returns to the departing state before visiting any other state.
        '''
        tpassignments = numpy.zeros(assignments.shape, dtype=bool)
        groundassignments = numpy.zeros(assignments.shape, dtype=bool)
        arrival_time = 0
        departure_time = assignments.shape[0]
        for i in xrange(1, assignments.shape[0]):
            # If the system leaves the departing_state
            if assignments[i] == -1 and assignments[i-1] == departing_state:
                departure_time = i

            # If the system enters the arrival_state
            if assignments[i] == arriving_state and assignments[i-1] == -1:
                arrival_time = i

            # If we encounter a state other than departing-state, arriving_state
            # and the intermediate state (-1), then reset the departure time to
            # the largest possible value, so that we do not count the transition
            # path
            if assignments[i] not in {-1, departing_state, arriving_state}:
                departure_time = assignments.shape[0]

            # Enter the following statement if the system left the departing 
            # state and entered the arriving state without visiting another 
            # state in between (except the intermediate state, -1)
            if arrival_time > departure_time:
                tpassignments[departure_time:arrival_time] = True
                departure_time = assignments.shape[0]

            if assignments[i] == departing_state and i > departure_time:
                groundassignments[departure_time:i] = True
                departure_time = assignments.shape[0]

        groundassignments[assignments==departing_state] = True

        return tpassignments, groundassignments

    def run(self, departing_state=0, arriving_state=1):
        '''
        Run the transition path analysis to generate assignments for the 
        transition path ensemble.

        ---------------
        Arguments
        ---------------
        departing_state: (int) The state from which transition paths originate.

        arriving_state: (int) The state at which transitino paths terminate.
        '''
        self.tpassignments = []
        self.groundassignments = []
        self.departing_state = departing_state
        self.arriving_state = arriving_state
        for isim in xrange(len(self.statelabels)):
            statelabelarr = self.statelabels[isim]
            tpassignments, groundassignments = self.assign_tp(statelabelarr,
                                                departing_state=departing_state,
                                                arriving_state=arriving_state)
            self.tpassignments.append(tpassignments)
            self.groundassignments.append(groundassignments)

            print("Number of timepoints in transition paths for simulation "
                  "{:d}: {:f}".format(isim, self.tpassignments[isim].sum()))
            print("Number of timepoints in departing state for "
                  "simulation {:d}: {:f}"\
                  .format(isim, self.groundassignments[isim].sum()))

    def compare_volume(self, saveprefix='default'):
        '''
        Calculate the average volume in the departing state and the transition
        path ensemble. Also, save the arrays of volume data to 
            prefix.departing.npy
            prefix.tp.npy
        where prefix is the prefix specified by the keyword argument 
        ``saveprefix``.
        '''
        departing_volume = []
        tp_volume = []
        for isim in xrange(len(self.statelabels)):
            tpassignments = self.tpassignments[isim]
            departing_assignments = self.groundassignments[isim]
            #departing_assignments = self.statelabels[isim]==self.departing_state
            volume = self.volume[isim]
            departing_volume.append(volume[departing_assignments])
            tp_volume.append(volume[tpassignments])

        departing_volume = numpy.concatenate(departing_volume)
        tp_volume = numpy.concatenate(tp_volume)

        numpy.save("{:s}.departing".format(saveprefix), departing_volume)
        numpy.save("{:s}.tp".format(saveprefix), tp_volume)

        print("Average volume in departing state ({:d}) is {:.02f}"\
              .format(self.departing_state, departing_volume.mean()))
        print("Average volume in transition path ensemble is {:.02f}"\
              .format(tp_volume.mean()))

if __name__ == "__main__":
    sims = ['ff14sb.xray.1',
            'ff14sb.xray.2',
            'ff14sb.xray.3',
            'ff14sb.nmr.1',
            'ff14sb.nmr.2',
            'ff14sb.nmr.3',
            'ff14sb.KP21B.1',
            'ff14sb.KP21B.2',
            'ff14sb.KP21B.3',
            'ff14sb.KLP21D.1',
            'ff14sb.KLP21D.2',
            'ff14sb.KLP21D.3']

    statelabelpaths = ["/home/ajd98/projects/villin/17.10.31/classifications/{:s}.npy"\
                       .format(sim) for sim in sims]
    volumedatapaths = ["/mnt/NAS2/VILLIN/brute_force_analysis/volume/{:s}/volume.npy"\
                       .format(sim) for sim in sims]

    tpa = TPAnalysis(statelabelpaths, volumedatapaths) 
    tpa.run(departing_state=0, arriving_state=1)
    tpa.compare_volume()

    tpa.run(departing_state=1, arriving_state=0)
    tpa.compare_volume()

    tpa.run(departing_state=1, arriving_state=0)
    tpa.compare_volume()
        
