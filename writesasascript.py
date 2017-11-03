#!/usr/bin/env python
'''
Calculate solvent accessible surface area of villin HP35 and backbone amide
nitrogen atoms for a specified trajectory using cpptraj.
'''
import argparse

class AnalysisWriter(object):
    def __init__(self):
        self._parse_args()
        self.write()

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--maindir', dest='maindir',
                            help='The main simulation directory '
                                 '(e.g., ff14sb.xray.1).',
                            required=True)
        parser.add_argument('--topology', dest='topologypath',
                            help='The path to the topology files',
                            required=True)
        parser.add_argument('--output', dest='outputpath',
                            help='The path to the cpptraj script that should be'
                                 ' written.',
                            required=True)

        self.args = parser.parse_args()

    def write(self):
        outfile = open(self.args.outputpath, 'w+') 
        outfile.write("parm {:s} [default]\n".format(self.args.topologypath))
        for i in range(1,10001):
            if "ff14sb.xray.1" in self.args.maindir or "ff14sb.nmr.1" in self.args.maindir:
                outfile.write("trajin {:s}/{:04d}/{:04d}_cut.nc\n".format(self.args.maindir,
                                                                          i, i))  
            else:
                outfile.write("trajin {:s}/{:05d}/{:05d}_cut.nc\n".format(self.args.maindir,
                                                                          i, i))  
        if 'ttet' in self.args.maindir:
            outfile.write("molsurf molsurf_all :1-36 out surf.dat\n")
            outfile.write("surf surf_all :1-36 out surf.dat\n")
        else:
            outfile.write("molsurf molsurf_all :1-35 out surf.dat\n")
            outfile.write("surf surf_all :1-35 out surf.dat\n")
        outfile.write("surf surf_33N :33@N out surf.dat\n")
        outfile.write("surf surf_34N :34@N out surf.dat\n")
        outfile.write("surf surf_35N :35@N out surf.dat\n")

        outfile.write("go\n")
        outfile.close()
      
if __name__ == '__main__':
    AnalysisWriter() 
