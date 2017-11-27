#!/usr/bin/env python
#
# Written 17.08.01 by Alex DeGrave
#
import numpy
import matplotlib
import os
import matplotlib.pyplot as pyplot
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle

def movingcircularaverage(orig_interval, window_size):
    window= numpy.ones(int(window_size))/float(window_size)
    interval = numpy.copy(orig_interval)
    
    interval *= (2.0*numpy.pi)/360.0

    sin_interval = numpy.sin(interval)
    cos_interval = numpy.cos(interval)

    sin_conv = numpy.convolve(sin_interval, window, 'same')
    cos_conv = numpy.convolve(cos_interval, window, 'same')

    return 360/(numpy.pi*2)*numpy.arctan2(sin_conv, cos_conv)

def multiple_and(tupl):
    check = numpy.logical_and(tupl[0], tupl[0]) 
    for data in tupl[1:]:
        check = numpy.logical_and(check, data)
    return check

def multiple_or(tupl):
    check = numpy.logical_or(tupl[0], tupl[0]) 
    for data in tupl[1:]:
        check = numpy.logical_or(check, data)
    return check

class StateClassifier(object):
    def __init__(self, **kwargs):
        pass

    def _load_data_from_txt(self, datadirpath):
        phipath = '{:s}/phi.dat'.format(datadirpath)
        psipath = '{:s}/psi.dat'.format(datadirpath)
        chipath = '{:s}/chi.dat'.format(datadirpath)

        # Load training data into numpy arrays
        phi = numpy.loadtxt(phipath, skiprows=1)[:,1:] # skip the timestamps
        psi = numpy.loadtxt(psipath, skiprows=1)[:,1:]
        chi = numpy.loadtxt(chipath, skiprows=1)[:,1:]

        # mod chi2 for Phe residues by 180
        chi[:, 11][chi[:, 11] < 0] = chi[:, 11][chi[:, 11] < 0] + 180
        chi[:, 18][chi[:, 18] < 0] = chi[:, 18][chi[:, 18] < 0] + 180
        chi[:, 30][chi[:, 30] < 0] = chi[:, 30][chi[:, 30] < 0] + 180

        if numpy.any(chi[:,11]<0):
            print(chi[:,11].max())
            raise ValueError
        
        if numpy.any(chi[:,18]<0):
            print(chi[:,18].max())
            raise ValueError
        
        if numpy.any(chi[:,30]<0):
            print(chi[:,30].max())
            raise ValueError
        
        data = numpy.concatenate((phi, psi, chi), axis=1)
        return data

    def load_data(self, datadirpath):
        npypath = "{:s}/all_data".format(datadirpath)
        if not os.path.exists(npypath+'.npy'):
            data = self._load_data_from_txt(datadirpath)  
            numpy.save(npypath+'.npy', data)
        else:
            data = numpy.load(npypath+'.npy')
        #for i in xrange(data.shape[1]):
        #    data[:,i] = movingcircularaverage(data[:,i],100)
        return data

    def fits_statedef(self, array, datalabel, bounds, *other_bounds):
        if datalabel == 'psi10':
            idx = 43
        if datalabel == 'phi11':
            idx = 9
        if datalabel == 'phi31':
            idx = 29
        if datalabel == 'chi10_1':
            idx = 85
        if datalabel == 'psi6':
            idx = 39
        if datalabel == 'psi11':
            idx = 44
        if datalabel == 'chi6_1':
            idx = 78
        if datalabel == 'phi9':
            idx = 7
        if datalabel == 'psi8':
            idx = 41 
        if datalabel == 'phi10':
            idx = 8 
        if datalabel == 'phi12':
            idx = 10 

        if datalabel == 'psi28':
            idx = 61
        if datalabel == 'psi29':
            idx = 62
        if datalabel == 'psi30':
            idx = 63
        if datalabel == 'psi31':
            idx = 64
        if datalabel == 'psi32':
            idx = 65

        if other_bounds:
           all_bounds = [bounds] + list(other_bounds)
           return multiple_or([numpy.logical_and(array[:,idx]>lb,
                                                 array[:,idx]<ub)
                               for (lb, ub) in all_bounds])
        else:
           (lb, ub) = bounds
           return numpy.logical_and(array[:,idx]>lb,array[:,idx]<ub)

    def vector_classify(self, data):
        psi10 = data[:,43]
        phi11 = data[:,9]
        phi31 = data[:,29]
        chi10_1 = data[:,85]
        psi6 = data[:,39]
        psi11 = data[:,44]
        chi6_1 = data[:,78]
        phi9 = data[:,7]
        psi8 = data[:,41]
        phi10 = data[:,8]
        phi12 = data[:,10]

        psi28 = data[:,61]
        psi29 = data[:,62]
        psi30 = data[:,63]
        psi31 = data[:,64]

        in_state0 = multiple_and([self.fits_statedef(data, 'psi10', (-20,10)),
                                  self.fits_statedef(data, 'phi11', (60,90)),
                                  self.fits_statedef(data, 'chi10_1', (-75,-55)),
                                  self.fits_statedef(data, 'psi6', (-50,-40)),
                                  self.fits_statedef(data, 'psi11', (0,20)),
                                  self.fits_statedef(data, 'chi6_1', (-180,-175), (-80,-60)),
                                  self.fits_statedef(data, 'phi9', (-85,-60)),
                                  self.fits_statedef(data, 'psi8', (-60,-30)),
                                  self.fits_statedef(data, 'phi10', (-110,-80)), 
                                  self.fits_statedef(data, 'phi12', (-165,-145)), 
                                  self.fits_statedef(data, 'psi28', (-55,-25)), 
                                  self.fits_statedef(data, 'psi29', (-55,-25)), 
                                  self.fits_statedef(data, 'psi30', (-55,-25)), 
                                  self.fits_statedef(data, 'psi31', (-55,-25))])

        in_state1 = multiple_and([self.fits_statedef(data, 'psi10', (-10, 15)),
                                  self.fits_statedef(data, 'phi11', (60,90)),
                                  self.fits_statedef(data, 'chi10_1', (-60,-40)),
                                  self.fits_statedef(data, 'psi6', (-40,-20)),
                                  self.fits_statedef(data, 'psi11', (10,30)),
                                  self.fits_statedef(data, 'chi6_1', (175, 180), (-180,-170), (-95,-75)),
                                  self.fits_statedef(data, 'phi9', (-85,-60)),
                                  self.fits_statedef(data, 'psi8', (-30,-10)),
                                  self.fits_statedef(data, 'phi10', (-140,-110)), 
                                  self.fits_statedef(data, 'phi12', (-165,-135)), 
                                  self.fits_statedef(data, 'psi28', (-55,-25)), 
                                  self.fits_statedef(data, 'psi29', (-55,-25)), 
                                  self.fits_statedef(data, 'psi30', (-55,-25)), 
                                  self.fits_statedef(data, 'psi31', (-55,-25))])

        in_state3 = multiple_and([self.fits_statedef(data, 'psi10', (140, 180)),
                                  self.fits_statedef(data, 'phi11', (-90,-70)),
                                  self.fits_statedef(data, 'chi10_1', (-75,-55)),
                                  self.fits_statedef(data, 'psi6', (-50,-20)),
                                  self.fits_statedef(data, 'psi11', (-40,40)),
                                  self.fits_statedef(data, 'chi6_1', (-180, -155), (-95,-75)),
                                  self.fits_statedef(data, 'phi9', (-135,-75)),
                                  self.fits_statedef(data, 'psi8', (-35,0)),
                                  self.fits_statedef(data, 'phi10', (-150,-80)),
                                  self.fits_statedef(data, 'phi12', (-180,-140), (-80, -55)), 
                                  self.fits_statedef(data, 'psi28', (-55,-25)), 
                                  self.fits_statedef(data, 'psi29', (-55,-25)), 
                                  self.fits_statedef(data, 'psi30', (-55,-25)), 
                                  self.fits_statedef(data, 'psi31', (-55,-25))])

        in_state2 = multiple_and([self.fits_statedef(data, 'psi10', (130,155)),
                                  self.fits_statedef(data, 'phi11', (-90,-65)),
                                  self.fits_statedef(data, 'chi10_1', (170,180), (-180,-165)),
                                  self.fits_statedef(data, 'psi6', (-55,-35)),
                                  self.fits_statedef(data, 'psi11', (-40,70)),
                                  self.fits_statedef(data, 'chi6_1', (165,180), (-180,-170)),
                                  self.fits_statedef(data, 'phi9', (-135,-75)),
                                  self.fits_statedef(data, 'psi8', (-35,0)),
                                  self.fits_statedef(data, 'phi10', (-90,-55)),
                                  self.fits_statedef(data, 'phi12', (-160,-140), (-80,-55)), 
                                  self.fits_statedef(data, 'psi28', (-55,-25)), 
                                  self.fits_statedef(data, 'psi29', (-55,-25)), 
                                  self.fits_statedef(data, 'psi30', (-55,-25)), 
                                  self.fits_statedef(data, 'psi31', (-55,-25))])

        # alpha helix 3 is unfolded.
        in_state4 = multiple_or([self.fits_statedef(data, 'psi28', (100, 180)),
                                 self.fits_statedef(data, 'psi29', (100, 180)),
                                 self.fits_statedef(data, 'psi30', (100, 180)),
                                 self.fits_statedef(data, 'psi31', (100, 180))])

        # if it is in state 4, it is not in another state!
        in_state0[in_state4] == False 
        in_state1[in_state4] == False 
        in_state2[in_state4] == False 
        in_state3[in_state4] == False 

        if multiple_and([in_state0, in_state1, in_state3, in_state4]).sum() != 0:
            raise ValueError
        output = numpy.ones(data.shape[0])*-1
        output[in_state0] = 0
        output[in_state1] = 1
        output[in_state2] = 2
        output[in_state3] = 3
        output[in_state4] = 4
        return output


    def classify(self, datadirpath):
        data = self.load_data(datadirpath) 

        anchorpoints = self.vector_classify(data)
        labels = numpy.ones(data.shape[0])*-1
        for i, val in enumerate(anchorpoints):
            if val > -1:
                labels[i] = val
            else:
                if i == 0:
                    labels[i] = -1
                else:
                    labels[i] = labels[i-1]
        return labels

def main():
    sc = StateClassifier()

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.xray.1/')
    #numpy.savetxt('no_smooth/ff14sb.xray.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.xray.2/')
    #numpy.savetxt('no_smooth/ff14sb.xray.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.xray.3/')
    #numpy.savetxt('no_smooth/ff14sb.xray.3', classifications)
    #
    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.nmr.1/')
    #numpy.savetxt('no_smooth/ff14sb.nmr.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.nmr.2/')
    #numpy.savetxt('no_smooth/ff14sb.nmr.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.nmr.3/')
    #numpy.savetxt('no_smooth/ff14sb.nmr.3', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KLP21D.1/')
    #numpy.savetxt('no_smooth/ff14sb.KLP21D.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KLP21D.2/')
    #numpy.savetxt('no_smooth/ff14sb.KLP21D.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KLP21D.3/')
    #numpy.savetxt('no_smooth/ff14sb.KLP21D.3', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KP21B.1/')
    #numpy.savetxt('no_smooth/ff14sb.KP21B.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KP21B.2/')
    #numpy.savetxt('no_smooth/ff14sb.KP21B.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KP21B.3/')
    #numpy.savetxt('no_smooth/ff14sb.KP21B.3', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.xray.1/')
    #numpy.savetxt('no_smooth/ff03w.xray.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.xray.2/')
    #numpy.savetxt('no_smooth/ff03w.xray.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.xray.3/')
    #numpy.savetxt('no_smooth/ff03w.xray.3', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.nmr.1/')
    #numpy.savetxt('no_smooth/ff03w.nmr.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.nmr.2/')
    #numpy.savetxt('no_smooth/ff03w.nmr.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.nmr.3/')
    #numpy.savetxt('no_smooth/ff03w.nmr.3', classifications)
    #
    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.KLP21D.1/')
    #numpy.savetxt('no_smooth/ff03w.KLP21D.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.KLP21D.2/')
    #numpy.savetxt('no_smooth/ff03w.KLP21D.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.KLP21D.3/')
    #numpy.savetxt('no_smooth/ff03w.KLP21D.3', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.KP21B.1/')
    #numpy.savetxt('no_smooth/ff03w.KP21B.1', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.KP21B.2/')
    #numpy.savetxt('no_smooth/ff03w.KP21B.2', classifications)

    #classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff03w.KP21B.3/')
    #numpy.savetxt('no_smooth/ff03w.KP21B.3', classifications)

    classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KP21B.ttet.1/')
    numpy.savetxt('no_smooth/ff14sb.KP21B.ttet.1', classifications)

    classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KP21B.ttet.2/')
    numpy.savetxt('no_smooth/ff14sb.KP21B.ttet.2', classifications)

    classifications = sc.classify('/mnt/NAS2/VILLIN/brute_force_analysis/ff14sb.KP21B.ttet.3/')
    numpy.savetxt('no_smooth/ff14sb.KP21B.ttet.3', classifications)

    
if __name__ == "__main__":
    main()
