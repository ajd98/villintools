#!/usr/bin/env python
import numpy

chimap = {1: (0,1),
          2: (2,),
          3: (3,4),
          4: (5,6,7),
          5: (8,9),
          6: (10,11),
          7: (12,13,14,15),
          8: (),
          9: (16,),
          10: (17,18),
          11: (),
          12: (19,20,21),
          13: (22,),
          14: (23,24,25,26,27),
          15: (28,),
          16: (),
          17: (29,30),
          18: (),
          19: (31,32),
          20: (33,34),
          21: (35,36),
          22: (37,38),
          23: (39,40),
          24: (41,42,43,44),
          25: (45,46,47),
          26: (48,49,50),
          27: (51,52),
          28: (53,54),
          29: (55,56,57,58),
          30: (59,60,61,62),
          31: (63,64,65),
          32: (66,67,68,69),
          33: (),
          34: (70,71),
          35: (72,73)}
          #14: (23,24,25,26,27),

class EntropyCalculation(object):
    def __init__(self, statefiles, datafiles):
        self.statefiles = statefiles
        self.datafiles = datafiles
        self.nbin_list = [10,15,20,24,36]
        self.states = (0,1,2,3,4)
        self.calculate()

    def get_data(self, state, residue):
        '''
        Return chi angles for residue index ``residues``, for all frames of all
        simulations in state ``state``.

        ----------
        Parameters
        ----------
        state: (int) the index of the state
        residue: (int) the index of the residue (see chimap)

        -------
        Returns
        -------
        '''
        alldata = []
        for isim in range(len(self.statefiles)):
            states = self.load_states(isim)
            data = self.load_data(isim)
            print(data[states==state].shape)
            alldata.append(data[states==state])
        alldata = numpy.concatenate(alldata, axis=0)
        print(alldata.shape)
        return alldata[:,chimap[residue]]

    def load_data(self, isim):
        print("      Loading {:s}".format(self.datafiles[isim]))
        return numpy.load(self.datafiles[isim])[::1000]

    def load_states(self, isim):
        logp = numpy.load(self.statefiles[isim])
        p = numpy.exp(logp)
        p /= p.sum(axis=1)[:,numpy.newaxis]
        states = numpy.argmax(p, axis=1)
        states[numpy.all(p<0.95, axis=1)] = -1
        return states

    def get_bins(self, residue, nbins):
        '''
        Generate bin edges for passing to numpy.histogramdd.

        ----------
        Parameters
        ----------
        residue: (int) the index of the residue (see chimap)
        nbins: (int) the number of bins along each axis

        -------
        Returns
        -------
        bins: (list of numpy arrays)
            [ <bins for dimension 0>,
              <bins for dimension 1>,
              ...
              <bins for dimension d>]
        '''
        ndims = len(chimap[residue])
        bins = numpy.linspace(-180,180,nbins)
        return [bins for i in range(ndims)]

    def calculate_entropy(self, hist):
        '''
        Calculate the entropy based on ``hist``, we describes the counts of
        observations in various microstates (bins).

        ----------
        Parameters
        ----------
        hist: (numpy.ndarray) a multidimensional histogram.

        -------
        Returns
        -------
        The entropy (dimensionless), calculated as sum(p ln p)
        '''
        count = hist.sum()
        ravelled = numpy.require(hist.ravel(), dtype=float)/count
        plnp = numpy.multiply(ravelled,numpy.log(ravelled))
        return plnp[numpy.isfinite(plnp)].sum()

    def histogram(self, data, bins):
        return numpy.histogramdd(data, bins=bins, normed=False)[0]

    def calculate(self):
        self.output_arr = numpy.zeros((len(self.states), len(chimap), len(self.nbin_list)))
        for istate, state in enumerate(self.states):
            print("working on state {:d}".format(state))
            for iresidue, residue in enumerate(chimap.keys()):
                if len(chimap[residue]) > 0:
                    print("  residue {:d}".format(residue))
                    data = self.get_data(state, residue)
                    for i, nbins in enumerate(self.nbin_list):
                        print("    bin scheme {:d}".format(i))
                        bins = self.get_bins(residue, nbins)
                        hist = self.histogram(data, bins)
                        entropy = self.calculate_entropy(hist)
                        self.output_arr[istate, iresidue, i] = entropy
                numpy.save('entropy', self.output_arr)

def main():
    ff14sbstatefiles = ['/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.xray.1.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.xray.2.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.xray.3.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.nmr.1.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.nmr.2.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.nmr.3.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.KLP21D.1.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.KLP21D.2.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.KLP21D.3.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.KP21B.1.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.KP21B.2.npy',
                        '/gscratch3/lchong/ajd98/villin/dihedrals/ntoruskdc30/ff14sb.KP21B.3.npy']

    ff14sbdatafiles = ['/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.xray.1/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.xray.2/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.xray.3/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.nmr.1/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.nmr.2/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.nmr.3/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.KLP21D.1/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.KLP21D.2/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.KLP21D.3/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.KP21B.1/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.KP21B.2/chi.npy',
                       '/gscratch3/lchong/ajd98/villin/dihedrals/ff14sb.KP21B.3/chi.npy']
    
    EntropyCalculation(ff14sbstatefiles, ff14sbdatafiles)
     
if __name__ == "__main__":
    main()
