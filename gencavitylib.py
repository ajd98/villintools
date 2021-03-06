#!/usr/bin/env python
import numpy
import argparse
'''
Generate a cavity.lib file for use with Voidoo*, based on an Amber parm7 
topology file.

*http://www.msg.ucsf.edu/local/programs/ono/manuals/voidoo_man.html

-----------
How to use:
  Call this tool via the command line, specifying the path to an Amber topology
  file as "--parmpath <topology>" and the path to an output file as 
  "--output <outfile>" (optional, default is cavity.lib.autogen).

  Alternatively, import the CavityLibGen object into a Python script, then 
  initialize the object as CavityLibGen(parmpath), where parmpath is a (str) 
  file path to the parm7 file.

  The cavity.lib file will be written to "cavity.lib.autogen". Once the script
  has completed, open the cavity.lib.autogen file and remove the "RESI" entries
  for residues that should NOT be included in the volume calculation.  For 
  example, you will typically want to remove "RESI WAT" (solvent) entries.
'''

class CavityLibGen(object):
    def __init__(self, parmpath, output='cavity.lib.autogen'):
        '''
        parmpath: path to Amber parm file
        '''
        self.parmpath = parmpath
        self.outpath = output
        self.isnanset = set()
        self._load()
        self.build_map()
        self.print_cavity_lib()

    def _load_atom_name(self):
        arr = []
        found_next_section = False

        # skip over the format line
        self.lineidx += 2
        line = self.lines[self.lineidx]

        linecount = 0
        while not found_next_section:
            linecount += 1
            split = [line[i:i+4] for i in range(0, len(line)-1, 4)]
            arr += split
            self.lineidx += 1
            line = self.lines[self.lineidx]
            if line.startswith('%'):
                found_next_section = True 

        return numpy.array(arr)


    def _load_until_next_section(self, dtype=None):
        arr = []
        found_next_section = False

        # skip over the format line
        self.lineidx += 2
        line = self.lines[self.lineidx]
        while not found_next_section:
            split = line.split()
            arr += split
            self.lineidx += 1
            line = self.lines[self.lineidx]
            if line.startswith('%'):
                found_next_section = True 

        if dtype is not None:
            return numpy.array(arr, dtype=dtype)
        else:
            return numpy.array(arr)
            
    def _load(self):
        parmfile = open(self.parmpath, 'r')
        self.lines = parmfile.readlines()
        parmfile.close()
        self.lineidx = 0
        while self.lineidx < len(self.lines):
            line = self.lines[self.lineidx]
            if line.startswith('%FLAG ATOM_TYPE_INDEX'):
                self.atom_type_index = self._load_until_next_section(dtype=int)
            elif line.startswith('%FLAG NONBONDED_PARM_INDEX'):
                self.nonbonded_parm_index = self._load_until_next_section(dtype=int)
            elif line.startswith('%FLAG LENNARD_JONES_ACOEF'):
                self.acoef = self._load_until_next_section(dtype=float)
            elif line.startswith('%FLAG LENNARD_JONES_BCOEF'):
                self.bcoef = self._load_until_next_section(dtype=float)
            elif line.startswith('%FLAG RESIDUE_LABEL'):
                self.residue_label = self._load_until_next_section()
            elif line.startswith('%FLAG ATOM_NAME'):
                self.atom_name = self._load_atom_name()
            elif line.startswith('%FLAG RESIDUE_POINTER'):
                self.residue_pointer = self._load_until_next_section(dtype=int)
            else: self.lineidx += 1
        self.ntypes = int(numpy.sqrt(self.nonbonded_parm_index.shape[0]))



    def get_residue_label(self,iatom):
        '''
        iatom: (int) the index of atom
        '''
        residx = 0

        if iatom < self.residue_pointer[-1]:
            for residx, respointer in enumerate(self.residue_pointer):
                if iatom < self.residue_pointer[residx+1]:
                    break
        else:
            residx = self.residue_pointer.shape[0]-1

        return self.residue_label[residx]

    def get_atom_name(self, iatom):
        '''
        iatom: (int) the index of the atom
        '''
        return self.atom_name[iatom]

    def get_nonbonded_parm_index(self, atomtypeindex1, atomtypeindex2):
        '''
        '''
        return self.nonbonded_parm_index[self.ntypes*(atomtypeindex1-1)+atomtypeindex2-1]


    def get_van_der_waals_radius(self, atomtypeindex):
        '''
         
        '''
        nonbonded_parm_index = self.get_nonbonded_parm_index(atomtypeindex,
                                                             atomtypeindex)
        if nonbonded_parm_index > 0:
            acoef = self.acoef[nonbonded_parm_index-1]
            bcoef = self.bcoef[nonbonded_parm_index-1]
            r = (2*acoef/bcoef)**(1./6)/2
        else:
            r = 0
        if numpy.isnan(r) and not atomtypeindex in self.isnanset:
            print("Radius is zero for atom type index: {:d}".format(atomtypeindex) )
            self.isnanset.add(atomtypeindex)
            r = 0
        return r

    def build_map(self):
        '''
        Build a map between a the pair (residue_label, atom_name) and the van 
        der Waals radius.
        '''
        print("length of ATOM_NAME: {:d}".format(self.atom_name.shape[0]))
        print("length of ATOM_TYPE_INDEX: {:d}".format(self.atom_type_index.shape[0]))
        self.map = dict()
        # iterate over every atom
        for iatom, atomtypeindex in enumerate(self.atom_type_index):
            reslabel = self.get_residue_label(iatom)
            atomname = self.get_atom_name(iatom)
            vdw_r = self.get_van_der_waals_radius(atomtypeindex)
            self.map[(reslabel, atomname)] = vdw_r

    def print_cavity_lib(self):
        outfile = open(self.outpath,'w+')
        lines_to_write = []
        resiset = set()
        for (reslabel, atomname), vdw_r in self.map.iteritems():
            atomname = atomname.strip()
            if len(atomname) == 1:
                atomname = " {:s}  ".format(atomname)
            elif len(atomname) == 2:
                atomname = " {:s} ".format(atomname)
            elif len(atomname) == 3:
                atomname = " {:s}".format(atomname)
            lines_to_write.append("SPAT '{:s}*{:s}' {:.03f}\n".format(reslabel, atomname, vdw_r)) 
            resiset.add(reslabel)

        # Sort the SPAT entries
        lines_to_write.sort()

        resilist = list(resiset)
        resilist.sort()

        # Add the RESI entries 
        for reslabel in resilist:
            lines_to_write.append("RESI '{:s}'\n".format(reslabel))

        # Write the lines to the output file.
        for line in lines_to_write:
            outfile.write(line)

        outfile.close()

class CavityLibGenTool(CavityLibGen):
    def __init__(self):
        self._parse_args()
        super(CavityLibGenTool, self).__init__(self.args.parmpath, 
                                               output=self.args.output)

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--parmpath', dest='parmpath', required=True,
                            help="The file path to the amber topology file "
                                 "(.parm7).")
        parser.add_argument('--output', dest='output', 
                            default='cavity.lib.autogen',
                            help="The output path for the cavity.lib file")
        self.args = parser.parse_args()
        

if __name__ == "__main__":
   CavityLibGenTool()
