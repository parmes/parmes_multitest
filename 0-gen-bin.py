from shutil import copy
from os import mkdir
import fileinput
import subprocess
import os

ZOLTANSRC = '/home/tk49770n/files/Zoltan_v3.83'
execfile ('0-var.py')
execfile ('0-var-athos.py')

# make directories
if not os.path.isdir('config'): mkdir ('config')
if not os.path.isdir('parmec'): mkdir ('parmec')
if not os.path.isdir('solfec'): mkdir ('solfec')

# save configuration files
copy ('../dynlb/Config.mak', 'config/Config.mak.dynlb')
copy ('../parmec/Config.mak', 'config/Config.mak.parmec')
copy ('../solfec/Config.mak', 'config/Config.mak.solfec')

for var in variants:
  if os.path.isfile('parmec/parmec4-%s' % var.name) and\
     os.path.isfile('parmec/parmec8-%s' % var.name) and\
     os.path.isfile('solfec/solfec-%s' % var.name) and\
     os.path.isfile('solfec/solfec-mpi-%s' % var.name):
     print '***'
     print '*** skipping existing variant: %s' % var.name
     print '***'
  else:
    codes = ['dynlb', 'parmec', 'solfec']
    for code in codes: # compile codes
      print '***'
      print '*** compiling %s variant: %s' % (code, var.name)
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
      if code == 'solfec' and var.variables['ZOLTAN'] == 'yes':
	zbuild = ZOLTANSRC + '/build_%s' % var.name
	zconfg = '../configure --prefix=%s --disable-zoltan-cppdriver --disable-tests --disable-examples' % zbuild
        if not os.path.isdir(zbuild):
	  print '***'
	  print '*** compiling ZOLTAN variant: %s' % var.name
	  print '***                  at path: %s' % zbuild
	  print '***'
	  mkdir (zbuild)
	  if len(var.modules) > 0: # load modules
	    command = "bash -c 'module purge ;"
	    for mod in var.modules:
	      command += " module load %s ;" % mod
	    command += " module list ; cd %s && %s && make && make install'" % (zbuild, zconfg)
	  else: command = 'cd ../%s && %s' % (code, make)
	process = subprocess.Popen(command, shell=True)
	process.wait()
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
    copy ('../parmec/parmec4', 'parmec/parmec4-' + var.name)
    copy ('../parmec/parmec8', 'parmec/parmec8-' + var.name)
    copy ('../solfec/solfec', 'solfec/solfec-' + var.name)
    copy ('../solfec/solfec-mpi', 'solfec/solfec-mpi-' + var.name)

# restore configuration files
copy ('config/Config.mak.dynlb', '../dynlb/Config.mak')
copy ('config/Config.mak.parmec', '../parmec/Config.mak')
copy ('config/Config.mak.solfec', '../solfec/Config.mak')
