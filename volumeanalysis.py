#!/usr/bin/env python
import argparse
import gencavitylib
import numpy
import os
import subprocess
import tempfile

class VolumeAnalysis(object):
    expecttemplate = '''\
#!/usr/local/bin/expect
spawn /gscratch3/lchong/ajd98/apps/voidoo_linux/lx_voidoo
expect "Type of calculation (C/V/R/Q)         ? (C)"
send "V\r"
expect "Do you want extensive output          ? (N)"
send "\r"
expect "Library file ? (cavity.lib)"
send "%LIBRARYFILE%\r"
expect "PDB file name ? (in.pdb)"
send "%PDBFILE%\r"
expect "Primary grid spacing (A) ? (   1.000)"
send "\r"
expect "Probe radius (1.4 A for water) ? (   0.000) "
send "\r"
expect " Nr of volume-refinement cycles        ? (         10) "
send "30\r"
expect "Grid-shrink factor                    ? (   0.900) "
send "\r"
expect " Convergence criterion (A3)            ? (   0.100)"
send ".5\r"
expect " Convergence criterion (%)             ? (   0.100) "
send ".001\r"
expect "Create protein-surface plot file      ? (N) "
send "\r"
expect "***** VOIDOO ***** VOIDOO ***** VOIDOO ***** VOIDOO ***** VOIDOO ***** "
send "\r"
'''

    def __init__(self):
        self._parse_args()
        self.generate_cavity_lib()
        self.volumes = []
        self.go()

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--maindir', dest='maindir',
                            help='The main simulation directory '
                                 '(e.g., ff14sb.xray.1).',
                            required=True)
        parser.add_argument('--topology', dest='topologypath',
                            help='The path to the topology files',
                            required=True)
        parser.add_argument('--outdir', dest='outdirpath',
                            help='The path to the output directory.',
                            required=True)

        self.args = parser.parse_args()

    def get_simname(self):
        simname = self.args.maindir.split('/')[-1]
        return simname

    def generate_cavity_lib(self):
        self.cavitylibpath = os.path.join(self.args.outdirpath, 
                                          'cavity.lib.autogen')
        gencavitylib.CavityLibGen(self.args.topologypath, self.cavitylibpath)
        
        # Now read the file we just wrote, and remove the "RESI" entries for
        # residues that should not be included in the volume calculation
        with open(self.cavitylibpath,'r') as f:
            lines = f.readlines()
        newlines = []
        for line in lines:
            if ('WAT' in line) or ('Cl-' in line) or ('Cl' in line):
                pass
            elif 'nan' in line:
                newlines.append(line.replace('nan','0.000'))
            else:
                newlines.append(line) 

        # Write the filtered list back to the file.
        with open(self.cavitylibpath, 'w') as f:
            f.writelines(newlines)
        
    def go(self):
        for segid in range(1,10001):
            # write a cpptraj script to write out the frames as separate pdb files
            cpptrajscript = tempfile.NamedTemporaryFile()
            pdbfile = tempfile.NamedTemporaryFile()
            expectfile = tempfile.NamedTemporaryFile()

            cpptrajscript.write("parm {:s}\n".format(self.args.topologypath))
            if "ff14sb.xray.1" in self.args.maindir or "ff14sb.nmr.1" in self.args.maindir:
                cpptrajscript.write("trajin {:s}/{:04d}/{:04d}_cut.nc\n"\
                                    .format(self.args.maindir, segid, segid))  
            else:
                cpptrajscript.write("trajin {:s}/{:05d}/{:05d}_cut.nc\n"\
                                    .format(self.args.maindir, segid, segid))  
            cpptrajscript.write("strip :WAT,Cl,Cl-\n")
            cpptrajscript.write("trajout {:s}.pdb pdb multi nobox\n".format(pdbfile.name))
            cpptrajscript.write("go\n")
            cpptrajscript.file.flush()

            # Call cpptraj to write out all the pdb files.
            subprocess.Popen(['/ihome/lchong/ajd98/apps/amber14/bin/cpptraj', '-i', 
                              cpptrajscript.name], stdout=subprocess.PIPE).wait()
             
            
            # Now iterate over the 100 pdb files
            for tpid in range(1,101):
                expectcmd = self.expecttemplate
                expectcmd = expectcmd.replace('%LIBRARYFILE%',self.cavitylibpath)
                pdbpath = "{:s}.pdb.{:d}".format(pdbfile.name, tpid)
                expectcmd = expectcmd.replace('%PDBFILE%', pdbpath)
                expectfile.write(expectcmd)
                expectfile.flush()
                process = subprocess.Popen(['expect', expectfile.name], 
                                           stdout=subprocess.PIPE)
                process.wait()
                stdout, stderr = process.communicate()
                
                # Finally, parse the output from VOIDOO
                s = [line for line in stdout.split('\n') if ("Protein volume (A3)" in line)][-1]
                volume = float(s.split()[5][:-1])
                self.volumes.append(volume)
                
                # Reset the expect script (delete its contents)
                expectfile.seek(0)
                expectfile.file.truncate()
                # Delete the pdb file
                os.remove(pdbpath)
        outpath = os.path.join(self.args.outdirpath, 'volume')
        numpy.save(outpath, numpy.array(self.volumes))

        
      
if __name__ == '__main__':
    VolumeAnalysis() 
