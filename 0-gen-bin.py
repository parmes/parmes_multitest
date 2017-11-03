from shutil import copy
import fileinput
import subprocess
import os
path0 = os.path.dirname(os.path.realpath(__file__))

execfile (path0 + '/0-var.py')
execfile (path0 + '/0-var-local.py')

# save configuration files
copy (path0+'/../dynlb/Config.mak', path0+'/config/Config.mak.dynlb')
copy (path0+'/../parmec/Config.mak', path0+'/config/Config.mak.parmec')
copy (path0+'/../solfec/Config.mak', path0+'/config/Config.mak.solfec')

for var in variants:
  codes = ['dynlb', 'parmec', 'solfec']
  for code in codes: # compile codes
    print '***'
    print '*** compiling: %s variant: %s' % (code, var.name)
    print '***'
    process = subprocess.Popen('cd ../%s && make clean' % code, shell=True)
    process.wait()
    for line in fileinput.input('../%s/Config.mak' % code, inplace=True):
      nomatch = True
      eqsp = line.split('=')
      if len(eqsp) == 2:
	for key in var.variables:
	  if key == eqsp[0].strip():
	    nomatch = False
	    print key + '=' + var.variables[key]
      if nomatch: print line,
    make = 'make all' if code == 'solfec' else 'make'
    if len(var.modules) > 0: # load modules
      command = "bash -c 'module purge ;"
      for mod in var.modules:
        command += " module load %s ;" % mod
      command += " module list ; cd ../%s && %s'" % (code, make)
    else: command = 'cd ../%s && %s' % (code, make)

    print 'Running:', command
    process = subprocess.Popen(command, shell=True)
    process.wait()


  # copy executables
  copy (path0+'/../parmec/parmec4', path0+'/parmec/parmec4-' + var.name)
  copy (path0+'/../parmec/parmec8', path0+'/parmec/parmec8-' + var.name)
  copy (path0+'/../solfec/solfec', path0+'/solfec/solfec-' + var.name)
  copy (path0+'/../solfec/solfec-mpi', path0+'/solfec/solfec-mpi-' + var.name)

# restore configuration files
copy (path0+'/config/Config.mak.dynlb', path0+'/../dynlb/Config.mak')
copy (path0+'/config/Config.mak.parmec', path0+'/../parmec/Config.mak')
copy (path0+'/config/Config.mak.solfec', path0+'/../solfec/Config.mak')
