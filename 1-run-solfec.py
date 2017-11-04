from shutil import copy
import fileinput
import subprocess
import os

execfile ('0-var.py')
execfile ('0-var-athos.py')

class Job:
  def __init__ (self, name, command, nodes, ranks, taskspernode=24):
    self.name = name
    self.command = command
    self.nodes = nodes
    self.ranks = ranks
    self.taskspernode = taskspernode

jobs = [Job('array1S', 'mpirun solfec/solfec-mpi-%s ../solfec/examples/parallel-scaling/array-of-cubes.py -M 20 -N 2 -stop 0.1', 1, 24),
        Job('array2S', 'mpirun solfec/solfec-mpi-%s ../solfec/examples/parallel-scaling/array-of-cubes.py -M 20 -N 2 -stop 0.1', 2, 48),
	Job('drum1S', 'mpirun solfec/solfec-mpi-%s ../solfec/examples/parallel-scaling/rotating-drum.py -npar 8000 -stop 1.5 -step 1E-4', 1, 24),
	Job('drum2S', 'mpirun solfec/solfec-mpi-%s ../solfec/examples/parallel-scaling/rotating-drum.py -npar 8000 -stop 1.5 -step 1E-4', 2, 48)
	]

for var in variants:
  for job in jobs: # schedule jobs
    print '***'
    print '*** scheduling: %s variant: %s' % (job.name, var.name)
    print '***'
    copy ('run.sh.0', 'run.sh')
    for line in fileinput.input('run.sh', inplace=True):
      if '#SBATCH --ntasks-per-node=' in line:
	print '#SBATCH --ntasks-per-node=%d' % job.taskspernode
      elif '#SBATCH -n' in line:
        print '#SBATCH -n %d' % job.ranks
      elif '#SBATCH -N' in line:
        print '#SBATCH -N %d' % job.nodes
      elif 'module load' in line and len(var.modules) > 0:
        ln = 'module load'
        for mod in var.modules:
          ln += " %s" % mod
	print ln
      elif 'mpirun solfec-mpi' in line:
        print (job.command + ' -prfx %s') % (var.name, var.name)
      else: print line,

    #print 'sbatch -J %s-%s run.sh' % (job.name, var.name)
    #os.system('read -s -n 1 -p "Press any key to continue..."')
    #print
    process = subprocess.Popen('sbatch -J %s-%s run.sh' % (job.name, var.name), shell=True)
    process.wait()
